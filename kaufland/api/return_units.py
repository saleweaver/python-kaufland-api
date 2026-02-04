from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class ReturnUnits(Client):
    """ReturnUnits Kaufland API Client."""

    @kaufland_endpoint("/return-units", method="GET")
    def get_return_units(self, **kwargs) -> ApiResponse:
        """
        Get a list of return units
        
        Get a list of return units.
        
        Args:
        storefront: Storefront | optional (query) Locale of storefront
        ts_created_from_iso: str | optional (query) Get only return units which were placed after this timestamp. Should be in YYYY-MM-ddTHH:mm:ssZ format
        status: list[ReturnUnitStatus] | optional (query) Get only return units which are in the given status
        fulfillment_type: list[FulfillmentType] | optional (query) Get only return units which are fulfilled by the given type.<br/> The value `fulfilled_by_kaufland` is **DEPRECATED**.
        sort: str | optional (query) Specify sorting
        limit: Integer | optional (query) Desired size of result set<br>max: 100, default: 30
        offset: Integer | optional (query) Offset applied to result set<br>default: 0
        """
        return self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/return-units/{}", method="GET")
    def get_return_unit(self, id_return_unit, **kwargs) -> ApiResponse:
        """
        Get a return unit by ID
        
        Get a return unit by <code>id_return_unit</code>.
        
        Args:
        id_return_unit: int | required (path) Return unit ID, unique across all return units
        embedded: list[ReturnUnitEmbeddable] | optional (query) Additional data to be returned
        """
        return self._request(fill_query_params(kwargs.pop('path'), id_return_unit), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/return-units/{}/accept", method="PATCH")
    def accept_return_unit(self, id_return_unit, **kwargs) -> ApiResponse:
        """
        Accept a return unit
        
        Mark a return unit as `return_accepted`.
        
        Args:
        id_return_unit: int | required (path) Return unit ID, unique across all return units
        """
        return self._request(fill_query_params(kwargs.pop('path'), id_return_unit), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/return-units/{}/clarify", method="PATCH")
    def clarify_return_unit(self, id_return_unit, **kwargs) -> ApiResponse:
        """
        Clarify a return unit
        
        Mark a return unit as `return_in_clarification` to indicate a problem with a return unit after it has been received.
        Will open a ticket addressing the customer with the given message.
        
        Args:
        id_return_unit: int | required (path) Return unit ID, unique across all return units
        body: ReturnUnitClarifyRequest | required (body) Request body containing message for clarifying return unit
        """
        body = kwargs.pop('body', None)
        return self._request(fill_query_params(kwargs.pop('path'), id_return_unit), data=body, params=kwargs, add_storefront=False)

    @kaufland_endpoint("/return-units/{}/reject", method="PATCH")
    def reject_return_unit(self, id_return_unit, **kwargs) -> ApiResponse:
        """
        Reject a return unit
        
        Mark a return unit as `return_rejected`. Will open a ticket addressing the customer with the given message.
        
        Args:
        id_return_unit: int | required (path) Return unit ID, unique across all return units
        body: ReturnUnitRejectRequest | required (body) Request body containing message for rejecting return unit
        """
        body = kwargs.pop('body', None)
        return self._request(fill_query_params(kwargs.pop('path'), id_return_unit), data=body, params=kwargs, add_storefront=False)

    @kaufland_endpoint("/return-units/{}/repair", method="PATCH")
    def repair_return_unit(self, id_return_unit, **kwargs) -> ApiResponse:
        """
        Repair a return unit
        
        Mark a return unit as `return_in_repair`.
        
        Args:
        id_return_unit: int | required (path) Return unit ID, unique across all return units
        """
        return self._request(fill_query_params(kwargs.pop('path'), id_return_unit), params=kwargs, add_storefront=False)
