from kaufland.asyncio import Client
from kaufland.base import ApiResponse, kaufland_endpoint


class Info(Client):
    """Info Kaufland API Client."""

    @kaufland_endpoint("/info/locale", method="GET")
    async def get_all_locales(self, **kwargs) -> ApiResponse:
        """
        Get values for parameter 'locale'

        Get all available values for the parameter 'locale'. This parameter specifies the language of e.g. product data.
        """
        return await self._request(
            kwargs.pop("path"), params=kwargs, add_storefront=False
        )

    @kaufland_endpoint("/info/storefront", method="GET")
    async def get_all_storefronts(self, **kwargs) -> ApiResponse:
        """
        Get values for parameter 'storefront'

        Get current seller available values for the parameter 'storefront'. This parameter specifies the country of the store.
        Returns a list of storefronts the seller has created in the sellerportal regardless of storefront status.
        """
        return await self._request(
            kwargs.pop("path"), params=kwargs, add_storefront=False
        )

    @kaufland_endpoint("/info/vat-indicators", method="GET")
    async def get_vat_indicators(self, **kwargs) -> ApiResponse:
        """
        Get a list of Vat Indicators Mappings per Storefront

        This endpoint provides a mapping between vat_indicators and actually used vat rates per storefront. The response yields which vat_indicators is accepted on a given storefront.
        The vat_indicators can (optionally) be used when creating/updating offers.

        Args:
        storefront: Storefront | optional (query) Parameter to select the affected storefront
        """
        return await self._request(
            kwargs.pop("path"), params=kwargs, add_storefront=True
        )
