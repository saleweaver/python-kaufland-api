from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Categories(Client):
    """Categories Kaufland API Client."""

    @kaufland_endpoint("/categories", method="GET")
    def get_categories_list(self, **kwargs) -> ApiResponse:
        """
        Get category list by search term

        Get a list of categories that contain a specific search term.

        Args:
        storefront: Storefront | required (query) Specifies the store by country
        q: str | optional (query) Search term for finding a specific category
        id_parent: int | optional (query) ID of parent category
        limit: int | optional (query) Desired size of result set. Max: 100
        offset: int | optional (query) Offset applied to result set
        locale: ProductDataLocale | optional (query) Allows clients to consume the data in languages that are different from the storefront-default locale
        """
        return self._request(kwargs.pop("path"), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/categories/decide", method="POST")
    def decide_category(self, **kwargs) -> ApiResponse:
        """
        Guess categories

        Guess potential categories for a product based on its product data. The first result is the category the product is most likely in.

        Args:
        storefront: Storefront | required (query) Specifies the store by country
        locale: ProductDataLocale | optional (query) Allows clients to consume the data in languages that are different from the storefront-default locale
        body: CategoryDecideRequestBody | required (body) Json object with product data
        """
        body = kwargs.pop("body", None)
        return self._request(
            kwargs.pop("path"), data=body, params=kwargs, add_storefront=True
        )

    @kaufland_endpoint("/categories/tree", method="GET")
    def get_category_tree(self, **kwargs) -> ApiResponse:
        """
        Get complete category tree

        Get a complete category tree with all categories and their relationships, fields and values.

        Args:
        storefront: Storefront | required (query) Specifies the store by country
        locale: ProductDataLocale | optional (query) Allows clients to consume the data in languages that are different from the storefront-default locale
        """
        return self._request(kwargs.pop("path"), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/categories/{}", method="GET")
    def get_category(self, id_category, **kwargs) -> ApiResponse:
        """
        Get category by ID

        Get a category by <code>id_category</code>.

        Args:
        id_category: int | required (path) The ID of the desired category
        storefront: Storefront | required (query) Specifies the store by country
        embedded: list[CategoryEmbeddable] | optional (query) Include other entities in the results of the result list
        locale: ProductDataLocale | optional (query) Allows clients to consume the data in languages that are different from the storefront-default locale
        """
        return self._request(
            fill_query_params(kwargs.pop("path"), id_category),
            params=kwargs,
            add_storefront=True,
        )
