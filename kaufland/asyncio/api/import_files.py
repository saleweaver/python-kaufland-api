from kaufland.asyncio import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class ImportFiles(Client):
    """ImportFiles Kaufland API Client."""

    @kaufland_endpoint("/import-files/inventory-command", method="GET")
    async def get_inventory_command_import_files(self, **kwargs) -> ApiResponse:
        """
        Get a list of your inventory command import files
        
        Get a list of your inventory command import files.
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        status: ImportStatus | optional (query) File status filter
        ts_created_iso: str | optional (query)
        ts_updated_iso: str | optional (query)
        sort: ImportFilesSortBy | optional (query)
        limit: int | optional (query) Desired size of result set
        offset: int | optional (query) Offset applied to result set
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/import-files/inventory-command", method="POST")
    async def create_inventory_command_import_file(self, **kwargs) -> ApiResponse:
        """
        Add an INVENTORY_COMMAND file URL
        
        Saves an URL where a new import file is located. The file located at the URL will be downloaded and processed asynchronously and the contents imported.
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        body: ImportFileInventoryCommandPostRequest | required (body)
        """
        body = kwargs.pop('body', None)
        return await self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=True)

    @kaufland_endpoint("/import-files/inventory-command/{}", method="GET")
    async def get_inventory_command_import_file(self, id_import_file, **kwargs) -> ApiResponse:
        """
        Get an inventory command import file by ID
        
        Get an inventory command import file by its <code>id_import_file</code>.
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        id_import_file: int | required (path) Internal ID of Import File
        """
        return await self._request(fill_query_params(kwargs.pop('path'), id_import_file), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/import-files/inventory-feed", method="GET")
    async def get_inventory_feed_import_files(self, **kwargs) -> ApiResponse:
        """
        Get a list of your inventory feed import files
        
        Get a list of your inventory feed import files.
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        status: ImportStatus | optional (query) File status filter
        ts_created_iso: str | optional (query)
        ts_updated_iso: str | optional (query)
        sort: ImportFilesSortBy | optional (query)
        limit: int | optional (query) Desired size of result set
        offset: int | optional (query) Offset applied to result set
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/import-files/inventory-feed", method="POST")
    async def create_inventory_feed_import_file(self, **kwargs) -> ApiResponse:
        """
        Add an INVENTORY_FEED file URL
        
        Saves an URL where a new import file is located. The file located at the URL will be downloaded and processed asynchronously and the contents imported.
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        body: ImportFileInventoryFeedPostRequest | required (body)
        """
        body = kwargs.pop('body', None)
        return await self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=True)

    @kaufland_endpoint("/import-files/inventory-feed/{}", method="GET")
    async def get_inventory_feed_import_file(self, id_import_file, **kwargs) -> ApiResponse:
        """
        Get an inventory feed import file by ID
        
        Get an inventory feed import file by its <code>id_import_file</code>.
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        id_import_file: int | required (path) Internal ID of Import File
        """
        return await self._request(fill_query_params(kwargs.pop('path'), id_import_file), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/import-files/order-command", method="GET")
    async def get_order_command_import_files(self, **kwargs) -> ApiResponse:
        """
        Get a list of your order command import files
        
        Get a list of your order command import files.
        
        Args:
        status: ImportStatus | optional (query) File status filter
        ts_created_iso: str | optional (query)
        ts_updated_iso: str | optional (query)
        sort: ImportFilesSortBy | optional (query)
        limit: int | optional (query) Desired size of result set
        offset: int | optional (query) Offset applied to result set
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/import-files/order-command", method="POST")
    async def create_order_command_import_file(self, **kwargs) -> ApiResponse:
        """
        Add an ORDER_COMMAND file URL
        
        Saves an URL where a new import file is located. The file located at the URL will be downloaded and processed asynchronously and the contents imported.
        
        Args:
        body: ImportFileOrderCommandPostRequest | required (body)
        """
        body = kwargs.pop('body', None)
        return await self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=False)

    @kaufland_endpoint("/import-files/order-command/{}", method="GET")
    async def get_order_command_import_file(self, id_import_file, **kwargs) -> ApiResponse:
        """
        Get an order command import file by ID
        
        Get an order command import file by its <code>id_import_file</code>.
        
        Args:
        id_import_file: int | required (path) Internal ID of Import File
        """
        return await self._request(fill_query_params(kwargs.pop('path'), id_import_file), params=kwargs, add_storefront=False)
