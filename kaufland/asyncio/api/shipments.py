from kaufland.asyncio import Client
from kaufland.base import ApiResponse, kaufland_endpoint


class Shipments(Client):
    """Shipments Kaufland API Client."""

    @kaufland_endpoint("/shipments", method="POST")
    async def add_shipment(self, **kwargs) -> ApiResponse:
        """
        Add a shipment to an order unit which is already marked as sent.

        Add a shipment to an order unit which is already marked as sent by providing a carrier code and a tracking number.<br>
        Valid values for `carrier_code` can be found in the
        <a href="https://sellerapi.kaufland.com/?page=order-files#carrier-codes" target="_blank">documentation</a>.

        Args:
        body: AddShipmentRequest | required (body) Request body containing information about a shipment related to an order unit
        """
        body = kwargs.pop("body", None)
        return await self._request(
            kwargs.pop("path"), data=body, params=kwargs, add_storefront=False
        )
