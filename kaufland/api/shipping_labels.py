from kaufland import Client
from kaufland.base import ApiResponse, kaufland_endpoint


class ShippingLabels(Client):
    """ShippingLabels Kaufland API Client."""

    @kaufland_endpoint("/shipping-labels", method="POST")
    def create_shipping_label(self, **kwargs) -> ApiResponse:
        """
        Request and create a shipping label.

        You can read about Kaufland Shipment Solutions (KSS) <a href="/?page=kss" target="_blank">here</a>.

        This endpoint provides a temporary link to a PDF file that contains the shipping label.

        Please consider shipping restrictions that apply.

        `ids_order_units` is a list of order unit IDs that are to be shipped in the same package.

        `carriers` is a list of carriers you are able to use to ship the package. If you want to use a specific carrier, you can pass only the desired carrier.
        The carrier must be one of the following: `GLS`

        `package_measurements` are the properties of the package. The `weight` is in grams, the `width`, `height`, and `length` are in centimeters.

        If the response is successful, the response will contain the following properties:
        - `id` is the ID of the shipment label.
        - `tracking_number` is the tracking number of the shipment.
        - `carrier` is the carrier used to ship the package.
        - `download_url` is the URL to download the shipping label, the download url works for 7 days.

        If you are using the playground environment, the response will always return a dummy success response.

        Args:
        body: CreateShippingLabelRequest | required (body) Request body containing information about the specification of the shipment.
        """
        body = kwargs.pop("body", None)
        return self._request(
            kwargs.pop("path"), data=body, params=kwargs, add_storefront=False
        )
