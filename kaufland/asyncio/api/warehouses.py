from kaufland.asyncio import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Warehouses(Client):
    """Warehouses Kaufland API Client."""

    @kaufland_endpoint("/warehouses", method="GET")
    async def get_warehouses(self, **kwargs) -> ApiResponse:
        """
        Get a list of your Warehouses

        Get a list of your warehouses.

        Args:
        limit: int | optional (query) Desired size of result set
        offset: int | optional (query) Offset applied to result set
        """
        return await self._request(
            kwargs.pop("path"), params=kwargs, add_storefront=False
        )

    @kaufland_endpoint("/warehouses", method="POST")
    async def create_warehouse(self, **kwargs) -> ApiResponse:
        """
        Create a new Warehouse

        Create a new warehouse.

        Args:
        body: WarehouseBodyRequest | required (body) Information about the warehouse that will be generated
        """
        body = kwargs.pop("body", None)
        return await self._request(
            kwargs.pop("path"), data=body, params=kwargs, add_storefront=False
        )

    @kaufland_endpoint("/warehouses/{}", method="DELETE")
    async def delete_warehouse(self, id_warehouse, **kwargs) -> ApiResponse:
        """
        Delete a warehouse

        Delete a warehouse.

        Args:
        id_warehouse: int | required (path) Internal ID of Warehouse, unique across all Warehouses
        """
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_warehouse),
            params=kwargs,
            add_storefront=False,
        )

    @kaufland_endpoint("/warehouses/{}", method="GET")
    async def get_warehouse(self, id_warehouse, **kwargs) -> ApiResponse:
        """
        Get a warehouse by its ID

        Gets a warehouse by <code>id_warehouse</code>.

        Args:
        id_warehouse: int | required (path) Internal ID of Warehouse, unique across all Warehouses
        """
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_warehouse),
            params=kwargs,
            add_storefront=False,
        )

    @kaufland_endpoint("/warehouses/{}", method="PUT")
    async def update_warehouse(self, id_warehouse, **kwargs) -> ApiResponse:
        """
        Update a Warehouse

        Update a warehouse.

        Args:
        id_warehouse: int | required (path) Internal ID of Warehouse, unique across all Warehouses
        body: WarehouseBodyRequest | required (body) Update Object
        """
        body = kwargs.pop("body", None)
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_warehouse),
            data=body,
            params=kwargs,
            add_storefront=False,
        )
