from kaufland import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class OrderInvoices(Client):
    """OrderInvoices Kaufland API Client."""

    @kaufland_endpoint("/order-invoices", method="GET")
    def get_order_invoices(self, **kwargs) -> ApiResponse:
        """
        Get a list of order invoices

        Get a list of order invoices. The list contains invoices uploaded by the seller as well as invoices
        provided by Kaufland.de, i.e. those which fall under the deemed supplier model (DSM).

        Args:
        storefront: Storefront | optional (query) Locale of storefront
        ts_created_from_iso: str | optional (query) Get only order units which were placed after this timestamp. Should be in YYYY-MM-ddTHH:mm:ssZ format
        limit: int | optional (query) Desired size of result set<br>max: 100, default: 30
        offset: int | optional (query) Offset applied to result set<br>default: 0
        """
        return self._request(kwargs.pop("path"), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/order-invoices/{}", method="POST")
    def upload_order_invoice(self, id_order, **kwargs) -> ApiResponse:
        """
        Upload an order invoice to a given order

        Upload an order invoice to a given order.

        Args:
        id_order: str | required (path) Order ID, unique across all orders
        body: OrderInvoiceUploadRequest | required (body) Request body containing invoice related information and binary invoice data base64 encoded
        """
        body = kwargs.pop("body", None)
        return self._request(
            fill_query_params(kwargs.pop("path"), id_order),
            data=body,
            params=kwargs,
            add_storefront=False,
        )

    @kaufland_endpoint("/order-invoices/{}/{}", method="DELETE")
    def delete_order_invoice(self, id_order, id_invoice, **kwargs) -> ApiResponse:
        """
        Delete an order invoice by given order ID and invoice ID

        Delete an order invoice by <code>id_order</code> and <code>id_invoice</code>.

        Args:
        id_order: str | required (path) Order ID, unique across all orders
        id_invoice: LongInteger | required (path) Invoice ID, <b>not unique</b> across all invoices.
        """
        return self._request(
            fill_query_params(kwargs.pop("path"), id_order, id_invoice),
            params=kwargs,
            add_storefront=False,
        )

    @kaufland_endpoint("/order-invoices/{}/{}", method="GET")
    def get_order_invoice(self, id_order, id_invoice, **kwargs) -> ApiResponse:
        """
        Get an order invoice by order ID and invoice ID

        Get an order invoice by <code>id_order</code> and <code>id_invoice</code>.<br>
        Note: Invoice IDs are <b>not unique</b> across all invoices as there are two types of order invoices:
        <ul>
         <li>- Invoices uploaded by the seller</li>
         <li>- Invoices provided by Kaufland.de which fall under the deemed supplier model (DSM)</li>
        </ul>

        Args:
        id_order: str | required (path) Order ID, unique across all orders
        id_invoice: int | required (path) Invoice ID, <b>not unique</b> across all invoices.
        """
        return self._request(
            fill_query_params(kwargs.pop("path"), id_order, id_invoice),
            params=kwargs,
            add_storefront=False,
        )
