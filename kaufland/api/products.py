from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Products(Client):
    """Products Kaufland API Client."""

    @kaufland_endpoint("/products/ean/{}", method="GET")
    def get_product_by_ean(self, ean, **kwargs) -> ApiResponse:
        """
        Get a product by EAN

        Get a product by EAN

        Args:
        ean: str | required (path) European Article Number with 13, 14 or 15 digits
        storefront: Storefront | required (query) Specifies the store by country
        embedded: list[ProductEmbeddable] | optional (query) Include related entities in the result (if both parameters "category" and "category_basics" are provided, only the parameter "category" is used)
        """
        return self._request(
            fill_query_params(kwargs.pop("path"), ean),
            params=kwargs,
            add_storefront=True,
        )

    @kaufland_endpoint("/products/search", method="GET")
    def get_product_list(self, **kwargs) -> ApiResponse:
        """
        Get a list of products by search term

        Get a list of products by search term

        Args:
        storefront: Storefront | required (query) Specifies the store by country
        q: str | required (query) Search term for finding a specific product
        limit: int | optional (query) Desired size of result set. Max: 100
        offset: int | optional (query) Offset applied to result set
        embedded: list[ProductEmbeddable] | optional (query) Include other entities in the results of the result list (if both parameters "category" and "category_basics" are provided, only the parameter "category" is used)
        """
        return self._request(kwargs.pop("path"), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/products/{}", method="GET")
    def get_product(self, id_product, **kwargs) -> ApiResponse:
        """
        Get product by ID

        Get a product by its <code>id_product</code>.

        Args:
        id_product: int | required (path) Kaufland internal id of the product
        storefront: Storefront | required (query) Specifies the store by country
        embedded: list[ProductEmbeddable] | optional (query) Include related entities in the result (if both parameters "category" and "category_basics" are provided, only the parameter "category" is used)
        """
        return self._request(
            fill_query_params(kwargs.pop("path"), id_product),
            params=kwargs,
            add_storefront=True,
        )
