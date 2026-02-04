from kaufland.asyncio import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Units(Client):
    """Units Kaufland API Client."""

    @kaufland_endpoint("/units", method="GET")
    async def get_units(self, **kwargs) -> ApiResponse:
        """
        Get a list of your units

        Get a list of your units. Note that there may a delay of up to several
        minutes between adding a new unit and when it will be available through this endpoint.

        Args:
        limit: int | optional (query) Desired size of result set, maximum is 100
        offset: int | optional (query) Offset applied to result set
        storefront: Storefront | required (query) Parameter to select the affected storefront
        id_offer: str | optional (query) Provided ID of your stock
        id_product: int | optional (query) Our internal id_product
        ean: str | optional (query) EAN, 13 or 14 digits
        embedded: list[UnitAndProductEmbeddedEnum] | optional (query)
        fulfillment_type: list[FulfillmentType] | optional (query) Get only units which are fulfilled by the given type. <br/> The value `fulfilled_by_kaufland` is **DEPRECATED**.
        """
        return await self._request(
            kwargs.pop("path"), params=kwargs, add_storefront=True
        )

    @kaufland_endpoint("/units", method="POST")
    async def create_unit(self, **kwargs) -> ApiResponse:
        """
        Add a unit

        Add a new unit for an existing product. You must specify either an <code>id_product</code>
        or an <code>ean</code> (or both), to identify the product to which the unit belongs.
        Please notice that you have to specify a listing price greater than zero.

        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        embedded: list[UnitEmbeddedEnum] | optional (query)
        body: UnitRequest | required (body) Information about the unit that will be generated
        """
        body = kwargs.pop("body", None)
        return await self._request(
            kwargs.pop("path"), data=body, params=kwargs, add_storefront=True
        )

    @kaufland_endpoint("/units/bulk", method="POST")
    async def bulk_update_units(self, **kwargs) -> ApiResponse:
        """
        Update some fields of a given set of units

        Update some fields of a given set of units. Please notice that you have to specify a
        listing price greater than zero.

        <b>Important:</b> There are a couple of rules to keep in mind when using this endpoint, failure to respect these rules will result in the failure of the entire request:
        <ol>
            <li>Your request <b>SHOULD NOT</b> have more than 150 units in the body, exceeding this limit will result in a 400 response and will fail the whole request.</li>
            <li>The request <b>SHOULD NOT</b> contain duplicate units, if duplicates are detected the whole request is rejected.</li>
        </ol>

        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        embedded: list[UnitEmbeddedEnum] | optional (query)
        body: list[UnitsBulkUpdateRequest] | required (body) Update Object
        """
        body = kwargs.pop("body", None)
        return await self._request(
            kwargs.pop("path"), data=body, params=kwargs, add_storefront=True
        )

    @kaufland_endpoint("/units/{}", method="DELETE")
    async def delete_unit(self, id_unit, **kwargs) -> ApiResponse:
        """
        Delete a unit

        Delete a unit.

        Args:
        id_unit: int | required (path) Internal ID of Unit, unique across all Units
        storefront: Storefront | required (query) Parameter to select the affected storefront
        """
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_unit),
            params=kwargs,
            add_storefront=True,
        )

    @kaufland_endpoint("/units/{}", method="GET")
    async def get_unit(self, id_unit, **kwargs) -> ApiResponse:
        """
        Get a unit by ID

        Get a unit by its <code>id_unit</code>

        Args:
        id_unit: int | required (path) Internal ID of Unit, unique across all Units
        storefront: Storefront | required (query) Parameter to select the affected storefront
        embedded: list[UnitAndProductEmbeddedEnum] | optional (query)
        """
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_unit),
            params=kwargs,
            add_storefront=True,
        )

    @kaufland_endpoint("/units/{}", method="PATCH")
    async def patch_unit(self, id_unit, **kwargs) -> ApiResponse:
        """
        Update some of the fields of a unit

        Update some of the fields of a unit. Please notice that you have to specify a
        listing price greater than zero.

        Args:
        id_unit: int | required (path) Internal ID of Unit, unique across all Units
        storefront: Storefront | required (query) Parameter to select the affected storefront
        embedded: list[UnitEmbeddedEnum] | optional (query)
        body: UnitPatchRequest | required (body) Update Object
        """
        body = kwargs.pop("body", None)
        return await self._request(
            fill_query_params(kwargs.pop("path"), id_unit),
            data=body,
            params=kwargs,
            add_storefront=True,
        )
