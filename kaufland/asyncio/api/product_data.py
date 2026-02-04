from kaufland.asyncio import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class ProductData(Client):
    """ProductData Kaufland API Client."""

    @kaufland_endpoint("/product-data", method="PATCH")
    async def update_product_data(self, **kwargs) -> ApiResponse:
        """
        Update existing product data for an EAN
        
        Add product data for a specific product (this will overwrite already provided values).
        The API expects to receive each attribute key only once. If you send the same attribute key multiple times,
        only the last value will be used.
        For attributes that can have multiple values (for example: picture), you can send an array of values.
        
        Args:
        locale: Locale | required (query) The language code of the product data (ISO 3166-2)
        body: ProductDataObject | required (body) JSON contains ean and attributes. Attributes contain all attributes with values JSON can contain ean and attributes. Attributes contain all attributes with values
        """
        body = kwargs.pop('body', None)
        return await self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=False)

    @kaufland_endpoint("/product-data", method="PUT")
    async def create_product_data(self, **kwargs) -> ApiResponse:
        """
        Add new product data for an EAN or replace your existing one
        
        Add new product data for an EAN or replace your existing one.
        The API expects to receive each attribute key only once. If you send the same attribute key multiple times,
        only the last value will be used.
        For attributes that can have multiple values (for example: picture), you can send an array of values.
        
        Args:
        locale: Locale | required (query) The language code of the product data (ISO 3166-2)
        body: ProductDataObject | required (body) JSON contains ean and attributes. Attributes contain all attributes with values
        """
        body = kwargs.pop('body', None)
        return await self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=False)

    @kaufland_endpoint("/product-data/import-files", method="GET")
    async def get_product_data_file_list(self, **kwargs) -> ApiResponse:
        """
        Get import files
        
        Get a list of all your import files. You can narrow down the search using various parameters.
        
        Args:
        status: ProductDataImportFileStatus | optional (query) The status of your import
        ts_created: str | optional (query) Creation timestamp of the import file in ISO 8601
        ts_updated: str | optional (query) Update timestamp of the import file in ISO 8601
        sort: ProductDataImportFileSorting | optional (query) Select the field (time created or time updated) and the direction of sorting (ascending or descending)
        limit: int | optional (query) Desired size of result set. Max: 100
        offset: int | optional (query) Offset applied to result set
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/product-data/import-files", method="POST")
    async def create_product_data_file(self, **kwargs) -> ApiResponse:
        """
        Add an import file URL
        
        Saves an URL where a new import file is located.
        The file located at the URL will be downloaded and processed asynchronously and the contents imported.
        For the upload of product feed data there is a limit of 30 feeds per day, so please combine data for multiple products in one CSV file if possible.
        
        Args:
        body: ImportFileRequestBody | required (body) Json object with import file data
        """
        body = kwargs.pop('body', None)
        return await self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=False)

    @kaufland_endpoint("/product-data/import-files/{}", method="GET")
    async def get_product_data_file(self, id_import_file, **kwargs) -> ApiResponse:
        """
        Get import file by ID
        
        Get an import file by its ID.
        
        Args:
        id_import_file: int | required (path)
        """
        return await self._request(fill_query_params(kwargs.pop('path'), id_import_file), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/product-data/status/{}", method="GET")
    async def get_product_data_status(self, ean, **kwargs) -> ApiResponse:
        """
        Get the process status for your product data
        
        Get the process status for your provided product data via EAN.
        
        Args:
        ean: str | required (path) European Article Number with 13, 14 or 15 digits
        locale: Locale | required (query) The language code of the product data (ISO 3166-2)
        """
        return await self._request(fill_query_params(kwargs.pop('path'), ean), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/product-data/{}", method="DELETE")
    async def delete_product_data(self, ean, **kwargs) -> ApiResponse:
        """
        Delete your product data for an EAN
        
        Delete the product data that you provided for a specific product via its EAN.
        
        Args:
        ean: str | required (path) European Article Number with 13, 14 or 15 digits
        locale: Locale | required (query) The language code of the product data (ISO 3166-2)
        """
        return await self._request(fill_query_params(kwargs.pop('path'), ean), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/product-data/{}", method="GET")
    async def get_product_data(self, ean, **kwargs) -> ApiResponse:
        """
        Get your product data for an EAN
        
        Get the product data that you provided for a specific product via its EAN
        
        Args:
        ean: str | required (path) European Article Number with 13, 14 or 15 digits
        locale: Locale | required (query) The language code of the product data (ISO 3166-2)
        """
        return await self._request(fill_query_params(kwargs.pop('path'), ean), params=kwargs, add_storefront=False)
