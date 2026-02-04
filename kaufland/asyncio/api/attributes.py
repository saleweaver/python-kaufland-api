from kaufland.asyncio import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Attributes(Client):
    """Attributes Kaufland API Client."""

    @kaufland_endpoint("/attributes", method="GET")
    async def get_attribute_list(self, **kwargs) -> ApiResponse:
        """
        Get an attribute list
        
        Get a list of all available attributes for a specific language.
        
        Args:
        storefront: Storefront | required (query) Specifies the store by country
        limit: int | optional (query) Desired size of result set. Max: 100
        offset: int | optional (query) Offset applied to result set
        locale: ProductDataLocale | optional (query) Allows clients to consume the data in languages that are different from the storefront-default locale
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/attributes/by-name/{}", method="GET")
    async def get_attribute_by_name(self, name, **kwargs) -> ApiResponse:
        """
        Get attribute by name
        
        Get an attribute by its name.
        
        Args:
        name: str | required (path) The name of the attribute
        storefront: Storefront | required (query) Specifies the store by country
        locale: ProductDataLocale | optional (query) Allows clients to consume the data in languages that are different from the storefront-default locale
        """
        return await self._request(fill_query_params(kwargs.pop('path'), name), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/attributes/search", method="GET")
    async def get_attribute_list_by_search(self, **kwargs) -> ApiResponse:
        """
        Get attributes by search term
        
        Get a list of attributes by a search term.
        
        Args:
        storefront: Storefront | required (query) Specifies the store by country
        q: str | required (query) Search term for finding a specific attribute
        limit: int | optional (query) Desired size of result set. Max: 100
        offset: int | optional (query) Offset applied to result set
        locale: ProductDataLocale | optional (query) Allows clients to consume the data in languages that are different from the storefront-default locale
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/attributes/{}", method="GET")
    async def get_attribute(self, id_attribute, **kwargs) -> ApiResponse:
        """
        Get attribute by ID
        
        Get an attribute by <code>id_attribute</code>.
        
        Args:
        id_attribute: int | required (path) The ID of the attribute
        storefront: Storefront | required (query) Specifies the store by country
        locale: ProductDataLocale | optional (query) Allows clients to consume the data in languages that are different from the storefront-default locale
        """
        return await self._request(fill_query_params(kwargs.pop('path'), id_attribute), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/attributes/{}/shared-set", method="GET")
    async def get_shared_set_list_by_search_and_attribute_id(self, id_attribute, **kwargs) -> ApiResponse:
        """
        Get shared-set by search term and attribute id
        
        Get a list of shared-set for a given attribute id by a search term.
        
        Args:
        id_attribute: int | required (path) The ID of the attribute
        locale: ProductDataLocale | required (query) Allows clients to consume the data in languages that are different from the storefront-default locale
        q: str | optional (query) Search term for finding a specific shared set value
        limit: int | optional (query) Desired size of result set. Max: 100
        offset: int | optional (query) Offset applied to result set
        """
        return await self._request(fill_query_params(kwargs.pop('path'), id_attribute), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/attributes/{}/shared-set-values", method="GET")
    async def get_shared_set_csv_file_by_attribute_id(self, id_attribute, **kwargs) -> ApiResponse:
        """
        Get the URL of a CSV file containing the shared set values for a specific attribute ID
        
        Get the URL for a CSV file containing the shared set values for a specific attribute ID.
        This endpoint returns a signed URL that provides access to the CSV file, which includes all the shared set
        values associated with the specified attribute. The signed URL is valid for six days
        
        Args:
        id_attribute: int | required (path) The ID of the attribute
        locale: ProductDataLocale | required (query) Allows clients to consume the data in languages that are different from the storefront-default locale
        """
        return await self._request(fill_query_params(kwargs.pop('path'), id_attribute), params=kwargs, add_storefront=False)
