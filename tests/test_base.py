import pytest
import httpx

from kaufland.base.ApiResponse import ApiResponse
from kaufland.base.base_client import BaseClient
from kaufland.base.decorators import kaufland_endpoint
from kaufland.base._transport_httpx import HttpxTransport
from kaufland.asyncio._transport_httpx import HttpxAsyncTransport


def test_base_client_invalid_signature_encoding():
    with pytest.raises(ValueError):
        BaseClient(client_key="ck", secret_key="sk", signature_encoding="nope")


def test_api_response_errors_property():
    resp = ApiResponse(payload={"error": "bad"})
    assert resp.errors == "bad"
    resp = ApiResponse(payload={"errors": ["a"]})
    assert resp.errors == ["a"]


def test_kaufland_endpoint_decorator():
    @kaufland_endpoint("/products/{}", method="GET")
    def func(**kwargs):
        return kwargs

    result = func()
    assert result["path"] == "/products/{}"
    assert result["_method"] == "GET"


def test_httpx_transport():
    transport = HttpxTransport(timeout=1)
    assert isinstance(transport._client, httpx.Client)
    transport.close()


@pytest.mark.anyio
async def test_httpx_async_transport():
    transport = HttpxAsyncTransport(timeout=1)
    assert isinstance(transport._client, httpx.AsyncClient)
    await transport.close()
