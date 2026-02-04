from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Status(Client):
    """Status Kaufland API Client."""

    @kaufland_endpoint("/status/ping", method="GET")
    def ping(self, **kwargs) -> ApiResponse:
        """
        Ping the Marketplace Seller API by Kaufland
        
        A simple method you can call that will return a constant value as long as everything is good.
        """
        return self._request(kwargs.pop('path'), params=kwargs, add_storefront=False)
