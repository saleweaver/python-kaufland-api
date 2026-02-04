from kaufland.asyncio import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class AssortmentCoverage(Client):
    """AssortmentCoverage Kaufland API Client."""

    @kaufland_endpoint("/assortment-coverage/insights", method="GET")
    async def get_assortment_insight(self, **kwargs) -> ApiResponse:
        """
        Args:
        offset: int | optional (query) Offset applied to result set
        limit: int | optional (query) Desired size of result set
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=False)
