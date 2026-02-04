from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class ShippingGroups(Client):
    """ShippingGroups Kaufland API Client."""

    @kaufland_endpoint("/shipping-groups", method="GET")
    def get_shipping_groups(self, **kwargs) -> ApiResponse:
        """
        Get the list of your predefined shipping groups
        
        Get the list of your predefined shipping groups.
        
        Args:
        limit: int | optional (query) Desired size of result set
        offset: int | optional (query) Offset applied to result set
        storefront: Storefront | required (query) Parameter to select the affected storefront
        """
        return self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/shipping-groups/{}", method="GET")
    def get_shipping_group(self, id_shipping_group, **kwargs) -> ApiResponse:
        """
        Get a shipping group by ID
        
        Get a shipping group by <code>id_shipping_group</code>.
        
        Args:
        id_shipping_group: int | required (path)
        storefront: Storefront | required (query) Parameter to select the affected storefront
        """
        return self._request(fill_query_params(kwargs.pop('path'), id_shipping_group), params=kwargs, add_storefront=True)
