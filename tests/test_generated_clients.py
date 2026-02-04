import pytest

from kaufland.api.products import Products
from kaufland.api.shipping_labels import ShippingLabels
from kaufland.asyncio.api.products import Products as AsyncProducts


class DummyProducts(Products):
    def __init__(self):
        pass

    def _request(self, path, **kwargs):
        self.last = (path, kwargs)
        return "ok"


class DummyShipping(ShippingLabels):
    def __init__(self):
        pass

    def _request(self, path, **kwargs):
        self.last = (path, kwargs)
        return "ok"


class DummyAsyncProducts(AsyncProducts):
    def __init__(self):
        pass

    async def _request(self, path, **kwargs):
        self.last = (path, kwargs)
        return "ok"


def test_generated_products_path_params():
    client = DummyProducts()
    client.get_product(123, embedded="category")
    path, kwargs = client.last
    assert path == "/products/123"
    assert kwargs["params"]["embedded"] == "category"
    assert kwargs["add_storefront"] is True


def test_generated_post_body():
    client = DummyShipping()
    client.create_shipping_label(body={"ids_order_units": [1]})
    path, kwargs = client.last
    assert path == "/shipping-labels"
    assert kwargs["data"] == {"ids_order_units": [1]}
    assert kwargs["add_storefront"] is False


@pytest.mark.anyio
async def test_generated_async_products():
    client = DummyAsyncProducts()
    await client.get_product(456)
    path, kwargs = client.last
    assert path == "/products/456"
    assert kwargs["add_storefront"] is True
