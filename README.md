# python-kaufland-api

Python wrapper for the Kaufland Marketplace Seller API. 
There are clients for both sync and async usage, all available endpoints are included.

This is the first commit, documentation will follow. Please refer to this README for usage for now, or create an issue.

## Install

[![Badge](https://img.shields.io/pypi/v/python-kaufland-api?style=for-the-badge)](https://pypi.org/project/python-kaufland-api/)

```bash
pip install python-kaufland-api
```

For development:

```bash
pip install -e '.[dev]'
```

## Authentication

Set credentials via environment variables or pass them into the client constructor:

- `KAUFLAND_CLIENT_KEY`
- `KAUFLAND_SECRET_KEY`
- `KAUFLAND_USER_AGENT`
- `KAUFLAND_STOREFRONT` (optional default)
- `KAUFLAND_PARTNER_CLIENT_KEY` (optional)
- `KAUFLAND_PARTNER_SECRET_KEY` (optional)
- `KAUFLAND_SIGNATURE_ENCODING` (`hex` default, `base64` optional)

## Sync Usage

```python
from kaufland import Client
from kaufland.api.products import Products

client = Client(
    client_key="...",
    secret_key="...",
    storefront="de",
)

products = Products(
    client_key="...",
    secret_key="...",
    storefront="de",
)

response = products.get_product(20574181, embedded=["category", "units"])
print(response.payload)
```

## Async Usage

```python
import asyncio
from kaufland.asyncio import Client
from kaufland.asyncio.api.products import Products

async def main():
    products = Products(
        client_key="...",
        secret_key="...",
        storefront="de",
    )

    response = await products.get_product(20574181)
    print(response.payload)
    await products.close()

asyncio.run(main())
```

## Generated Clients

Generated clients live under `kaufland.api` (sync) and `kaufland.asyncio.api` (async). Current client classes:

- `AssortmentCoverage`
- `Attributes`
- `Buybox`
- `Carriers`
- `Categories`
- `ImportFiles`
- `Info`
- `OrderInvoices`
- `OrderUnits`
- `Orders`
- `ProductData`
- `Products`
- `Reports`
- `ReturnUnits`
- `Returns`
- `Shipments`
- `ShippingGroups`
- `ShippingLabels`
- `Status`
- `Subscriptions`
- `Tickets`
- `Units`
- `VariantSuggestions`
- `Warehouses`

Regenerate clients from `swagger.json`:

```bash
uv run python tools/generate_clients.py
```

## Sponsorship

Support ongoing development: https://github.com/sponsors/saleweaver

## DISCLAIMER

We are not affiliated with kaufland