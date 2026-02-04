from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class VariantSuggestions(Client):
    """VariantSuggestions Kaufland API Client."""

    @kaufland_endpoint("/variant-suggestions/feed", method="GET")
    def get_variant_suggestions_feed_list(self, **kwargs) -> ApiResponse:
        """
        Get import files

        Get a list of all your import files. You can narrow down the search using various parameters.

        Args:
        status: ProductCategoriesImportFileStatus | optional (query) The status of your import
        ts_created: str | optional (query) Creation timestamp of the import file in ISO 8601
        ts_updated: str | optional (query) Update timestamp of the import file in ISO 8601
        sort: ProductCategoriesImportFileSorting | optional (query) Select the field (time created or time updated) and the direction of sorting (ascending or descending)
        limit: int | optional (query) Desired size of result set. Max: 100
        offset: int | optional (query) Offset applied to result set
        """
        return self._request(kwargs.pop("path"), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/variant-suggestions/feed/upload-by-url", method="POST")
    def upload_variant_suggestion_file_by_url(self, **kwargs) -> ApiResponse:
        """
        Add an import file URL

        Saves an URL where a new import file is located.
        The file located at the URL will be downloaded and processed asynchronously and the contents imported.
        For the upload of product feed data there is a limit of 30 feeds per day, so please combine data for multiple products in one CSV file if possible.

        Args:
        body: ProductCategoriesImportFileRequestBody | required (body) Json object with import file data
        """
        body = kwargs.pop("body", None)
        return self._request(
            kwargs.pop("path"), data=body, params=kwargs, add_storefront=False
        )

    @kaufland_endpoint("/variant-suggestions/feed/{}", method="GET")
    def get_variant_suggestions_feed(self, id_import_file, **kwargs) -> ApiResponse:
        """
        Get import file by ID

        Get an import file by its ID.

        Args:
        id_import_file: int | required (path)
        """
        return self._request(
            fill_query_params(kwargs.pop("path"), id_import_file),
            params=kwargs,
            add_storefront=False,
        )
