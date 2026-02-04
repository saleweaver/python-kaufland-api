from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Orders(Client):
    """Orders Kaufland API Client."""

    @kaufland_endpoint("/orders", method="GET")
    def get_orders(self, **kwargs) -> ApiResponse:
        """
        Get a list of orders
        
        Get a list of orders.
        
        Args:
        storefront: Storefront | optional (query) Locale of storefront
        ts_created_from_iso: str | optional (query) Get only orders which were placed after this timestamp. Should be in YYYY-MM-ddTHH:mm:ssZ format
        ts_units_updated_from_iso: str | optional (query) Get only orders which units were updated after this timestamp. Should be in YYYY-MM-ddTHH:mm:ssZ format
        fulfillment_type: list[FulfillmentType] | optional (query) Get only orders which are fulfilled by the given type. <br/> The value `fulfilled_by_kaufland` is **DEPRECATED**.
        limit: int | optional (query) Desired size of result set<br>max: 100, default: 30
        offset: int | optional (query) Offset applied to result set<br>default: 0
        """
        return self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/orders/{}", method="GET")
    def get_order(self, id_order, **kwargs) -> ApiResponse:
        """
        Get an order by ID
        
        Get an order by <code>id_order</code>.
        
        Args:
        id_order: str | required (path) Order ID, unique across all orders
        embedded: list[OrderEmbeddable] | optional (query) Add 'order_invoices' to get order related invoices in the response.
        """
        return self._request(fill_query_params(kwargs.pop('path'), id_order), params=kwargs, add_storefront=False)
