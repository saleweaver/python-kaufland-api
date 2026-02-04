import base64
import hashlib
import hmac

import pytest

from kaufland.base._core import (
    parse_response,
    prepare_request,
    resolve_method,
    sign_request,
)
from kaufland.base.ApiResponse import ApiResponse
from kaufland.base.decorators import fill_query_params
from kaufland.base.exceptions import ApiException


class DummyResponse:
    def __init__(self, status_code=200, headers=None, text="", json_data=None, json_raises=False):
        self.status_code = status_code
        self.headers = headers or {}
        self.text = text
        self._json_data = json_data
        self._json_raises = json_raises

    def json(self):
        if self._json_raises:
            raise ValueError("not json")
        return self._json_data


def test_sign_request_hex_example():
    method = "POST"
    uri = "https://sellerapi.kaufland.com/v2/units/"
    body = ""
    timestamp = 1411055926
    secret = "a7d0cb1da1ddbc86c96ee5fedd341b7d8ebfbb2f5c83cfe0909f4e57f05dd403"
    expected = "da0b65f51c0716c1d3fa658b7eaf710583630a762a98c9af8e9b392bd9df2e2a"
    assert sign_request(method, uri, body, timestamp, secret) == expected


def test_sign_request_base64():
    method = "GET"
    uri = "https://sellerapi.kaufland.com/v2/products/20574181/"
    body = ""
    timestamp = 1411055926
    secret = "secret"
    digest = hmac.new(
        secret.encode("utf-8"),
        "\n".join([method, uri, body, str(timestamp)]).encode("utf-8"),
        hashlib.sha256,
    ).digest()
    expected = base64.b64encode(digest).decode("ascii")
    assert (
        sign_request(method, uri, body, timestamp, secret, encoding="base64") == expected
    )


def test_prepare_request_adds_storefront_and_partner_headers():
    prepared = prepare_request(
        method="POST",
        endpoint="https://sellerapi.kaufland.com/v2",
        path="/units/",
        params={"foo": "bar"},
        data={"a": 1},
        headers={"Shop-Timestamp": "1411055926"},
        add_storefront=True,
        storefront="de",
        version=None,
        client_key="ck",
        secret_key="sk",
        user_agent="ua",
        partner_client_key="pck",
        partner_secret_key="psk",
        signature_encoding="hex",
    )

    assert prepared["method"] == "POST"
    assert "storefront=de" in prepared["url"]
    assert "foo=bar" in prepared["url"]
    assert prepared["content"] == b"{\"a\":1}"
    headers = prepared["headers"]
    assert headers["Shop-Client-Key"] == "ck"
    assert headers["Shop-Timestamp"] == "1411055926"
    assert headers["Shop-Partner-Client-Key"] == "pck"
    assert headers["Shop-Partner-Signature"]
    assert headers["Content-Type"] == "application/json"


def test_prepare_request_no_body_no_content_type():
    prepared = prepare_request(
        method="GET",
        endpoint="https://sellerapi.kaufland.com/v2",
        path="/products/20574181/",
        params=None,
        data=None,
        headers={"Shop-Timestamp": "1411055926"},
        add_storefront=False,
        storefront=None,
        version=None,
        client_key="ck",
        secret_key="sk",
        user_agent="ua",
        partner_client_key=None,
        partner_secret_key=None,
        signature_encoding="hex",
    )
    assert "Content-Type" not in prepared["headers"]


def test_parse_response_json():
    res = DummyResponse(status_code=200, headers={"X": "1"}, json_data={"ok": True})
    parsed = parse_response(res, method="GET")
    assert isinstance(parsed, ApiResponse)
    assert parsed.payload == {"ok": True}
    assert parsed.headers["X"] == "1"


def test_parse_response_text_on_json_error():
    res = DummyResponse(status_code=200, headers={}, text="not json", json_raises=True)
    parsed = parse_response(res, method="GET")
    assert parsed.payload == "not json"


def test_parse_response_error_raises():
    res = DummyResponse(status_code=400, headers={}, json_data={"error": "bad"})
    with pytest.raises(ApiException) as exc:
        parse_response(res, method="GET")
    assert exc.value.status_code == 400
    assert exc.value.payload == {"error": "bad"}


def test_parse_response_wrap_list_and_bulk():
    res = DummyResponse(status_code=200, headers={}, json_data=[{"a": 1}])
    parsed = parse_response(res, method="GET", wrap_list=True)
    assert parsed.payload == {"payload": [{"a": 1}]}

    res2 = DummyResponse(status_code=200, headers={}, json_data=[{"a": 1}])
    parsed2 = parse_response(res2, method="GET", bulk=True)
    assert parsed2.payload == {"responses": [{"a": 1}]}


def test_fill_query_params():
    path = "/products/{id_product}/units/{}"
    result = fill_query_params(path, "123", id_product="456")
    assert result == "/products/456/units/123"


def test_resolve_method():
    method, params, data = resolve_method({"_method": "PATCH"}, None)
    assert method == "PATCH"
    assert params == {}

    method, params, data = resolve_method(("DELETE", {"a": 1}), None)
    assert method == "DELETE"
    assert params == {"a": 1}

    method, params, data = resolve_method(None, ("POST", {"b": 2}))
    assert method == "POST"
    assert data == {"b": 2}

    method, params, data = resolve_method(None, {"x": 1})
    assert method == "POST"
    assert data == {"x": 1}
