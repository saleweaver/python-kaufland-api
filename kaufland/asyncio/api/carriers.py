from kaufland.asyncio import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Carriers(Client):
    """Carriers Kaufland API Client."""

    @kaufland_endpoint("/carriers", method="GET")
    async def get_carriers(self, **kwargs) -> ApiResponse:
        """
        Get a list of available carriers
        
        Get a list of available carriers.
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=False)
