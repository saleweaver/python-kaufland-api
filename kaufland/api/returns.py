from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Returns(Client):
    """Returns Kaufland API Client."""

    @kaufland_endpoint("/returns", method="GET")
    def get_returns(self, **kwargs) -> ApiResponse:
        """
        Get a list of returns
        
        Get a list of returns.
        
        Args:
        storefront: Storefront | optional (query) Locale of storefront
        ts_created_from_iso: str | optional (query) Get only returns which were placed after this timestamp. Should be in YYYY-MM-ddTHH:mm:ssZ format
        ts_updated_from_iso: str | optional (query) Get only returns which were updated after this timestamp. Should be in YYYY-MM-ddTHH:mm:ssZ format
        tracking_code: str | optional (query) The tracking code of a particular return
        status: list[ReturnStatus] | optional (query) Get only returns which are in the given status
        fulfillment_type: list[FulfillmentType] | optional (query) Get only returns which are fulfilled by the given type. <br/> The value `fulfilled_by_kaufland` is **DEPRECATED**.
        sort: str | optional (query) Specify sorting
        limit: int | optional (query) Desired size of result set<br>max: 100, default: 30
        offset: int | optional (query) Offset applied to result set<br>default: 0
        """
        return self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/returns", method="POST")
    def initiate_return(self, **kwargs) -> ApiResponse:
        """
        Initialize a return
        
        Initialize a return for one or more order units. All order units must belong to the same order.<br>
        Valid values for `reason` can be found in the
        <a href="https://sellerapi.kaufland.com/?page=returns" target="_blank">documentation</a>.<br>
        `note` must be at least 5 and maximal 100 characters long.
        
        Args:
        body: list[InitializeReturnRequest] | required (body) Request body containing return data for one or more order units
        """
        body = kwargs.pop('body', None)
        return self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=False)

    @kaufland_endpoint("/returns/{}", method="GET")
    def get_return(self, id_return, **kwargs) -> ApiResponse:
        """
        Get a return by ID
        
        Get a return by <code>id_return</code>.
        
        Args:
        id_return: int | required (path) Return ID, unique across all returns
        embedded: list[ReturnEmbeddable] | optional (query) Additional data to be returned
        """
        return self._request(fill_query_params(kwargs.pop('path'), id_return), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/returns/{}", method="PUT")
    def update_return(self, id_return, **kwargs) -> ApiResponse:
        """
        Add one or more order units to an already existing return
        
        Add one or more order units to an already existing return. All order units must belong to the same order.
        
        Args:
        id_return: str | required (path) Return ID, unique across all returns
        body: list[UpdateReturnRequest] | required (body) Request body containing return data for one or more order units
        """
        body = kwargs.pop('body', None)
        return self._request(fill_query_params(kwargs.pop('path'), id_return), data=body, params=kwargs, add_storefront=False)
