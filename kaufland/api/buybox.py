from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Buybox(Client):
    """Buybox Kaufland API Client."""

    @kaufland_endpoint("/buybox", method="GET")
    def get_offers_rankings(self, **kwargs) -> ApiResponse:
        """
        Get a list of offers rankings for a product
        
        This endpoint retrieves the top-ranked offers for a specified product, with an optional limit parameter to
        specify the maximum number of offers (up to 10).
        
        Args:
        id_product: int | required (query) Our internal id_product
        limit: int | optional (query) Desired size of offsets set, maximum is 10
        storefront: Storefront | required (query) Parameter to select the affected storefront
        condition: BuyboxCondition | required (query) The condition of the offers
        """
        return self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)
