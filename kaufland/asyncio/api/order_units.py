from kaufland.asyncio import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class OrderUnits(Client):
    """OrderUnits Kaufland API Client."""

    @kaufland_endpoint("/order-units", method="GET")
    async def get_order_units(self, **kwargs) -> ApiResponse:
        """
        Get a list of order units

        Get a list of order units.

        Args:
        storefront: Storefront | optional (query) Locale of storefront
        id_offer: str | optional (query) Unique ID for offer(s)
        status: list[OrderUnitStatus] | optional (query) Get only order units which are in the given status
        ts_created_from_iso: str | optional (query) Get only order units which were placed after this timestamp. Should be in YYYY-MM-ddTHH:mm:ssZ format
        ts_updated_from_iso: str | optional (query) Get only order units which were updated after this timestamp. Should be in YYYY-MM-ddTHH:mm:ssZ format
        fulfillment_type: list[FulfillmentType] | optional (query) Get only order units which are fulfilled by the given type. <br/> The value `fulfilled_by_kaufland` is **DEPRECATED**.
        sort: str | optional (query) Specify sorting
        limit: int | optional (query) Desired size of result set<br>max: 100, default: 30
        offset: int | optional (query) Offset applied to result set<br>default: 0
        """
        return await self._request(
            kwargs.pop("path"), params=kwargs, add_storefront=True
        )

    @kaufland_endpoint("/order-units/{}", method="GET")
    async def get_order_unit(self, id_order_unit, **kwargs) -> ApiResponse:
        """
        Get an order unit by ID

        Get an order unit by <code>id_order_unit</code>.

        Args:
        id_order_unit: int | required (path) Order unit ID, unique across all order units
        embedded: list[OrderUnitEmbeddable] | optional (query) Additional data to be returned
        """
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_order_unit),
            params=kwargs,
            add_storefront=False,
        )

    @kaufland_endpoint("/order-units/{}/cancel", method="PATCH")
    async def cancel_order_unit(self, id_order_unit, **kwargs) -> ApiResponse:
        """
        Cancel an order unit

        Cancel an order unit. Valid values for `reason` can be found in the
        <a href="https://sellerapi.kaufland.com/?page=order-files#cancellation-reasons" target="_blank">documentation</a>.

        Args:
        id_order_unit: int | required (path) Order unit ID, unique across all order units
        body: OrderUnitCancelRequest | required (body) Reason of the cancellation
        """
        body = kwargs.pop("body", None)
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_order_unit),
            data=body,
            params=kwargs,
            add_storefront=False,
        )

    @kaufland_endpoint("/order-units/{}/fulfil", method="PATCH")
    async def fulfil_order_unit(self, id_order_unit, **kwargs) -> ApiResponse:
        """
        Mark an order unit to be in fulfillment

        Mark an order unit to be in fulfillment (It will update the order unit status to `need_to_be_sent`).

        Args:
        id_order_unit: int | required (path) Order unit ID, unique across all order units
        """
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_order_unit),
            params=kwargs,
            add_storefront=False,
        )

    @kaufland_endpoint("/order-units/{}/refund", method="PATCH")
    async def refund_order_unit(self, id_order_unit, **kwargs) -> ApiResponse:
        """
        Send a refund to a customer

        Send a refund to a customer for a particular order unit.<br>`amount` must be in Eurocents.<br>
        Allowed values for `reason` can be found in the
        <a href="https://sellerapi.kaufland.com/?page=orders#refunding-order-unit" target="_blank">documentation</a>.

        Args:
        id_order_unit: int | required (path) Order unit ID, unique across all order units
        body: OrderUnitRefundRequest | required (body) Request body containing amount and reason of the refund.
        """
        body = kwargs.pop("body", None)
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_order_unit),
            data=body,
            params=kwargs,
            add_storefront=False,
        )

    @kaufland_endpoint("/order-units/{}/send", method="PATCH")
    async def send_order_unit(self, id_order_unit, **kwargs) -> ApiResponse:
        """
        Mark an order unit as sent

        Mark an order unit as sent. Valid values for `carrier_code` can be found in the
        <a href="https://sellerapi.kaufland.com/?page=order-files#carrier-codes" target="_blank">documentation</a>.

        Args:
        id_order_unit: int | required (path) Order unit ID, unique across all order units
        body: OrderUnitSendRequest | required (body) Request body containing tracking number(s) and carrier code of the shipment(s)
        """
        body = kwargs.pop("body", None)
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_order_unit),
            data=body,
            params=kwargs,
            add_storefront=False,
        )
