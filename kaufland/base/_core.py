from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

from .ApiResponse import ApiResponse
from .exceptions import ApiException


def sign_request(
    method: str,
    uri: str,
    body: str,
    timestamp: int,
    secret_key: str,
    *,
    encoding: str = "hex",
) -> str:
    string = "\n".join([method, uri, body or "", str(timestamp)])
    digest = hmac.new(
        secret_key.encode("utf-8"), string.encode("utf-8"), hashlib.sha256
    ).digest()
    if encoding == "base64":
        return base64.b64encode(digest).decode("ascii")
    return digest.hex()


def _build_url(endpoint: str, path: str, params: dict | None) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        base = path
    else:
        base = endpoint.rstrip("/") + ("/" + path.lstrip("/"))

    if not params:
        return base

    query = urlencode(params, doseq=True)
    if "?" in base:
        return f"{base}&{query}"
    return f"{base}?{query}"


def _encode_body(data):
    if data is None:
        return "", None
    if isinstance(data, bytes):
        body_bytes = data
        body_str = data.decode("utf-8", errors="surrogateescape")
        return body_str, body_bytes
    if isinstance(data, str):
        body_bytes = data.encode("utf-8")
        return data, body_bytes
    body_str = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    return body_str, body_str.encode("utf-8")


def _header_value(headers, name):
    if not headers:
        return None
    name = name.lower()
    for key, value in headers.items():
        if key.lower() == name:
            return value
    return None


def resolve_method(params, data, method=None):
    if method:
        return method.upper(), params, data

    if isinstance(params, tuple) and len(params) == 2 and isinstance(params[0], str):
        return params[0].upper(), params[1], data

    if isinstance(data, tuple) and len(data) == 2 and isinstance(data[0], str):
        return data[0].upper(), params, data[1]

    if isinstance(params, dict) and "_method" in params:
        method = params.pop("_method")
        return str(method).upper(), params, data

    if isinstance(data, dict) and "_method" in data:
        method = data.pop("_method")
        return str(method).upper(), params, data

    return ("POST" if data is not None else "GET"), params, data


def prepare_request(
    *,
    method: str,
    endpoint: str,
    path: str,
    params: dict | None,
    data,
    headers: dict | None,
    add_storefront: bool,
    storefront: str | None,
    version: str | None,
    client_key: str,
    secret_key: str,
    user_agent: str,
    partner_client_key: str | None,
    partner_secret_key: str | None,
    signature_encoding: str,
):
    params = dict(params or {})
    if add_storefront and storefront and "storefront" not in params:
        params["storefront"] = storefront

    if version and "<version>" in path:
        path = path.replace("<version>", version)

    url = _build_url(endpoint, path, params)
    body_str, body_bytes = _encode_body(data)

    header_timestamp = _header_value(headers, "Shop-Timestamp")
    timestamp = int(header_timestamp) if header_timestamp else int(time.time())

    signature = sign_request(
        method, url, body_str, timestamp, secret_key, encoding=signature_encoding
    )

    request_headers = {
        "Accept": "application/json",
        "Shop-Client-Key": client_key,
        "Shop-Timestamp": str(timestamp),
        "Shop-Signature": signature,
        "User-Agent": user_agent,
    }
    if partner_client_key and partner_secret_key:
        partner_signature = sign_request(
            method,
            url,
            body_str,
            timestamp,
            partner_secret_key,
            encoding=signature_encoding,
        )
        request_headers["Shop-Partner-Client-Key"] = partner_client_key
        request_headers["Shop-Partner-Signature"] = partner_signature
    if body_bytes is not None:
        request_headers["Content-Type"] = "application/json"
    if headers:
        request_headers.update(headers)

    return {
        "method": method,
        "url": url,
        "headers": request_headers,
        "content": body_bytes,
    }


def parse_response(
    res,
    *,
    method: str,
    res_no_data: bool = False,
    bulk: bool = False,
    wrap_list: bool = False,
):
    status = res.status_code
    headers = dict(res.headers)
    text = res.text or ""

    payload = None
    if not res_no_data and status != 204:
        try:
            payload = res.json()
        except ValueError:
            payload = text

    if bulk and isinstance(payload, list):
        payload = {"responses": payload}

    if wrap_list and isinstance(payload, list):
        payload = {"payload": payload}

    if status >= 400:
        raise ApiException(
            status_code=status,
            payload=payload,
            headers=headers,
            text=text,
        )

    return ApiResponse(payload=payload, headers=headers, status_code=status, raw=text)
