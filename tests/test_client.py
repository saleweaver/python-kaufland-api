import pytest

from kaufland import Client
from kaufland.asyncio import Client as AsyncClient
from kaufland.base.ApiResponse import ApiResponse
from kaufland.base.exceptions import ApiException
from kaufland.base._core import sign_request


class DummyTransport:
    def __init__(self, response):
        self.response = response
        self.last_request = None

    def request(self, **kwargs):
        self.last_request = kwargs
        return self.response

    def close(self):
        return None


class DummyAsyncTransport:
    def __init__(self, response):
        self.response = response
        self.last_request = None

    async def request(self, **kwargs):
        self.last_request = kwargs
        return self.response

    async def close(self):
        return None


class DummyResponse:
    def __init__(self, status_code=200, headers=None, json_data=None, text=""):
        self.status_code = status_code
        self.headers = headers or {}
        self._json_data = json_data
        self.text = text

    def json(self):
        return self._json_data


def test_client_request_builds_headers_and_url():
    response = DummyResponse(status_code=200, json_data={"ok": True})
    transport = DummyTransport(response)
    client = Client(
        client_key="ck",
        secret_key="sk",
        storefront="de",
        signature_encoding="hex",
    )
    client._transport = transport

    result = client._request(
        "/products/20574181/",
        params={"embedded": "category"},
    )

    assert isinstance(result, ApiResponse)
    req = transport.last_request
    assert req["method"] == "GET"
    assert "storefront=de" in req["url"]
    assert "embedded=category" in req["url"]
    headers = req["headers"]
    assert headers["Shop-Client-Key"] == "ck"
    assert headers["User-Agent"] == "saleweaver-python-kaufland-api"
    assert "Shop-Signature" in headers


def test_client_respects_custom_timestamp_header():
    response = DummyResponse(status_code=200, json_data={"ok": True})
    transport = DummyTransport(response)
    client = Client(
        client_key="ck",
        secret_key="sk",
        storefront="de",
        signature_encoding="hex",
    )
    client._transport = transport

    headers = {"Shop-Timestamp": "1411055926"}
    client._request(
        "/products/20574181/",
        params={"embedded": "category"},
        headers=headers,
    )

    req = transport.last_request
    expected = sign_request(
        "GET",
        req["url"],
        "",
        1411055926,
        "sk",
        encoding="hex",
    )
    assert req["headers"]["Shop-Signature"] == expected


def test_client_partner_headers():
    response = DummyResponse(status_code=200, json_data={"ok": True})
    transport = DummyTransport(response)
    client = Client(
        client_key="ck",
        secret_key="sk",
        partner_client_key="pck",
        partner_secret_key="psk",
    )
    client._transport = transport

    client._request("/products/20574181/")
    headers = transport.last_request["headers"]
    assert headers["Shop-Partner-Client-Key"] == "pck"
    assert "Shop-Partner-Signature" in headers


def test_client_error_raises_api_exception():
    response = DummyResponse(status_code=400, json_data={"error": "bad"})
    transport = DummyTransport(response)
    client = Client(client_key="ck", secret_key="sk")
    client._transport = transport

    with pytest.raises(ApiException):
        client._request("/products/20574181/")


@pytest.mark.anyio
async def test_async_client_request():
    response = DummyResponse(status_code=200, json_data={"ok": True})
    transport = DummyAsyncTransport(response)
    client = AsyncClient(client_key="ck", secret_key="sk", storefront="de")
    client._transport = transport

    result = await client._request("/products/20574181/")
    assert isinstance(result, ApiResponse)
    req = transport.last_request
    assert "storefront=de" in req["url"]
