from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Tickets(Client):
    """Tickets Kaufland API Client."""

    @kaufland_endpoint("/tickets", method="GET")
    def get_tickets(self, **kwargs) -> ApiResponse:
        """
        Get a list of tickets
        
        Get a list of tickets for given parameters.
        
        Args:
        sort: TicketsSort | optional (query) The sort direction
        limit: TicketListLimit | optional (query) Desired size of result set (default: 30)
        status: list[TicketStatus] | optional (query) The status of the ticket
        open_reason: list[TicketReason] | optional (query) The reason for this ticket.
        topic: list[TicketTopic] | optional (query) The topic of this ticket.
        id_buyer: Integer | optional (query) The buyer's internal id
        ts_created_from_iso: str | optional (query) Filter tickets by their creation timestamp in ISO 8601
        ts_updated_from_iso: str | optional (query) Filter tickets by their update timestamp in ISO 8601
        offset: TicketListOffset | optional (query) Offset applied to the result set (default: 0)
        storefront: list[Storefront] | optional (query) Identifier for the storefront the tickets should belong to
        fulfillment_type: list[FulfillmentType] | optional (query) Filter tickets by their fulfillment type. <br/> The value `fulfilled_by_kaufland` is **DEPRECATED**.
        """
        return self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/tickets", method="POST")
    def open_ticket(self, **kwargs) -> ApiResponse:
        """
        Open a ticket
        
        Open a ticket.
        
        Args:
        body: OpenTicketRequest | required (body)
        """
        body = kwargs.pop('body', None)
        return self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=False)

    @kaufland_endpoint("/tickets/messages", method="GET")
    def get_ticket_messages(self, **kwargs) -> ApiResponse:
        """
        Get a list of ticket messages
        
        Get a list of your ticket messages. If you want to get only ticket messages for a
        specific ticket, you should use the `/tickets/{id_ticket}/` endpoint and call it
        with `embedded=messages`.
        
        Args:
        limit: TicketMessageListLimit | optional (query) Desired size of result set (default: 30)
        sort: TicketMessagesSort | optional (query) The sort direction
        offset: TicketMessageListOffset | optional (query) Offset applied to result set (default: 0)
        ts_created_from_iso: str | optional (query) Filter ticket messages by their creation timestamp in iso 8601
        fulfillment_type: list[FulfillmentType] | optional (query) Filter tickets by their fulfillment type. <br/> The value `fulfilled_by_kaufland` is **DEPRECATED**.
        """
        return self._request(kwargs.pop('path'), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/tickets/{}", method="GET")
    def get_ticket(self, id_ticket, **kwargs) -> ApiResponse:
        """
        Get a ticket by ID
        
        Get a ticket given its `id_ticket`.
        
        Args:
        id_ticket: TicketID | required (path) The unique ID of a ticket
        embedded: list[TicketEmbeddable] | optional (query) A string of comma-separated values. Possible values: buyer, product, messages, order_units, files
        """
        return self._request(fill_query_params(kwargs.pop('path'), id_ticket), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/tickets/{}/close", method="PATCH")
    def close_ticket(self, id_ticket, **kwargs) -> ApiResponse:
        """
        Close a ticket by ID
        
        Close a ticket given its `id_ticket`.
        
        Args:
        id_ticket: TicketID | required (path) The unique ID of a ticket
        """
        return self._request(fill_query_params(kwargs.pop('path'), id_ticket), params=kwargs, add_storefront=False)

    @kaufland_endpoint("/tickets/{}/messages", method="POST")
    def create_ticket_message(self, id_ticket, **kwargs) -> ApiResponse:
        """
        Create a new message for the ticket
        
        Create a new message for the ticket.
        
        Args:
        id_ticket: TicketID | required (path) The unique ID of a ticket
        body: CreateTicketMessageRequest | required (body) Body params for the new message.
        """
        body = kwargs.pop('body', None)
        return self._request(fill_query_params(kwargs.pop('path'), id_ticket), data=body, params=kwargs, add_storefront=False)
