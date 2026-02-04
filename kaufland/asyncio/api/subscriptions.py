from kaufland.asyncio import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Subscriptions(Client):
    """Subscriptions Kaufland API Client."""

    @kaufland_endpoint("/subscriptions", method="GET")
    async def get_subscriptions(self, **kwargs) -> ApiResponse:
        """
        Get a list of your push notification subscriptions
        
        Get a list of your push notification subscriptions.
        
        Args:
        storefront: Storefront | optional (query) Parameter to select the affected storefront
        event_name: SubscriptionEventName | optional (query) Event name
        limit: int | optional (query) Desired size of result set
        offset: int | optional (query) Offset applied to result set
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/subscriptions", method="POST")
    async def add_subscription(self, **kwargs) -> ApiResponse:
        """
        Subscribe for event
        
        Create a new push notification subscription for an event. Using this endpoint will result in a callback verification request being sent to the given callback_url. See the Push Notifications documentation page for more information on push notifications and callback verification.
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        body: CreateSubscriptionRequest | required (body)
        """
        body = kwargs.pop('body', None)
        return await self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=True)

    @kaufland_endpoint("/subscriptions/{}", method="DELETE")
    async def delete_subscription(self, id_subscription, **kwargs) -> ApiResponse:
        """
        Unsubscribe from event
        
        Deletes the specified push notification subscription from the database. To re-subscribe to the given event, you must use the add subscription endpoint.
        
        Args:
        id_subscription: LongInteger | required (path)
        """
        return await self._request(fill_query_params(kwargs.pop('path'), id_subscription), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/subscriptions/{}", method="GET")
    async def get_subscription(self, id_subscription, **kwargs) -> ApiResponse:
        """
        Get a push notification subscription by ID
        
        Get a push notification subscription by <code>id_subscription</code>.
        
        Args:
        id_subscription: LongInteger | required (path)
        """
        return await self._request(fill_query_params(kwargs.pop('path'), id_subscription), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/subscriptions/{}", method="PATCH")
    async def update_subscription(self, id_subscription, **kwargs) -> ApiResponse:
        """
        Update subscription
        
        Update the fields of a push notification subscription. You can set the is_active flag to false to stop receiving notications for the subscription's event, or to true to re-enable a disabled subscription. If you change the value of the callback_url, the new callback_url will immediately receive a verification request. See the Callback URL Verification section of the Push Notifications documentation for details on validation requests.
        
        Args:
        id_subscription: LongInteger | required (path)
        body: UpdateSubscriptionRequest | required (body)
        """
        body = kwargs.pop('body', None)
        return await self._request(fill_query_params(kwargs.pop('path'), id_subscription), data=body, params=kwargs, add_storefront=False)
