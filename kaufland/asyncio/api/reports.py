from kaufland.asyncio import Client
from kaufland.base import ApiResponse, fill_query_params, kaufland_endpoint


class Reports(Client):
    """Reports Kaufland API Client."""

    @kaufland_endpoint("/reports", method="GET")
    async def get_reports(self, **kwargs) -> ApiResponse:
        """
        Get a list of your reports
        
        Returns the full meta-data for all of your reports. You can download any of the actual reports by requesting the file in the "url" property of one of the objects in the response, as long as the report is in the <code>done</code> state.
        
        Args:
        storefront: Storefront | optional (query) Parameter to select the affected storefront
        limit: int | optional (query) Desired size of result set
        offset: int | optional (query) Offset applied to result set
        sort: ReportsSorting | optional (query) Sorting of result set
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/reports/account-listing", method="POST")
    async def request_account_listing_report(self, **kwargs) -> ApiResponse:
        """
        Queue an inventory report
        
        Queues the generation of a CSV file that lists all of your items that are currently for sale on Kaufland Global Marketplace. You can use the generated file as the basis for an offers import file by downloading it and editing the fields, then reuploading it.
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/reports/bookings-new", method="POST")
    async def request_new_bookings_report(self, **kwargs) -> ApiResponse:
        """
        Queue a bookings report
        
        Queues the generation of a CSV file that lists all of your bookings on or after the given <code>date_from</code> timestamp and on or before the given <code>date_to</code> timestamp.
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        version: BookingsReportVersion | optional (query) Parameter to select the preferred version
        body: RequestBookingsReportRequest | required (body)
        """
        body = kwargs.pop('body', None)
        return await self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=True)

    @kaufland_endpoint("/reports/cancellations", method="POST")
    async def request_cancellations_report(self, **kwargs) -> ApiResponse:
        """
        Queue a cancellations report.
        
        Queues the generation of a CSV file that lists all orders in the <code>cancelled</code> state. The generated file includes the following fields for each cancelled order:
        <ul>
           <li><b>Datum der Stornierung:</b> The date of the cancellation</li>
           <li><b>Datum der Order:</b> The date of the order</li>
           <li><b>Grund der Stornierung:</b> The reason for cancelling</li>
           <li><b>EAN des Artikels:</b> The EAN of the item</li>
           <li><b>Hersteller des Artikels:</b> The manufacturer of the item</li>
           <li><b>Titel des Artikels:</b> The title (i.e. name) of the item</li>
        </ul>
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        cancellation_type: CancellationType | optional (query) Filter to select what cancellations are Considered (defaults to no filter applied)
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/reports/competitors-comparer", method="POST")
    async def request_competitors_comparer_report(self, **kwargs) -> ApiResponse:
        """
        Queue a competitors comparison report
        
        Queues the generation of a CSV file that contains a list of all of your listed items along with the cheapest price of each item on the kaufland.de site. The generated file includes the following fields for each item:
        <ul>
           <li><b>EAN:</b> The EAN of the item</li>
           <li><b>Offer_id:</b> The ID of your offer (i.e. unit)</li>
           <li><b>Titel:</b> The title (i.e. name) of the item</li>
           <li><b>Günstigster Preis neu:</b> The price of the cheapest new product listing for the item on kaufland.de in Eurocents</li>
           <li><b>Günstigster Preis gebraucht:</b> The price of the cheapest used product listing for the item on kaufland.de in Eurocents</li>
           <li><b>Ihr Preis:</b> Your price</li>
           <li><b>Differenz zu neu absolut:</b> The difference between your price and the cheapest new product price in Eurocents</li>
           <li><b>Differenz zu neu %:</b> The difference between your price and the cheapest new product price as a percentage</li>
           <li><b>Differenz zu gebraucht absolut:</b>The difference between your price and the cheapest used product price in Eurocents</li>
           <li><b>Differenz zu gebraucht %:</b> The difference between your price and the cheapest used product price as a percentage</li>
        </ul>
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/reports/eans-not-found", method="POST")
    async def request_eans_not_found_report(self, **kwargs) -> ApiResponse:
        """
        Queue an EANs not found report
        
        Queues the generation of a CSV file that lists all EANs of the seller, for that no or not enough product data was provided.
        The generated file includes the following fields for each EAN:
        <ul>
           <li><b>ean:</b> EAN of the offer or product</li>
           <li><b>reason:</b> Error reason</li>
        </ul>
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/reports/price-competitiveness", method="POST")
    async def request_price_competitiveness_report(self, **kwargs) -> ApiResponse:
        """
        Queue a price competitiveness report
        
        Queues the generation of a CSV file that contains a list of all of your listed items along with data regarding the competitiveness of your prices. Only data older than 24h is considered. The generated file includes the following fields for each item:
        <ul>
           <li><b>Storefront:</b> The storefront the item is listed on</li>
           <li><b>EAN:</b> The EAN of the item</li>
           <li><b>Item title:</b> The title (i.e. name) of the item</li>
           <li><b>Sales price:</b> The price at which you list the item on Kaufland, including any automatic adjustments made by our repricer tools, Smart Pricing and Smart Pricing Plus, as well as shipping costs.</li>
           <li><b>Gross price:</b> The price you have submitted, including shipping costs</li>
           <li><b>Minimum price:</b> The minimum price you have set, if provided, including shipping costs</li>
           <li><b>Competitive external price:</b> The lowest price found through comparison websites, including shipping costs</li>
           <li><b>Lowest price last 6 months excluding nov/dec:</b> The lowest price at which you have offered the item in the last 6 months. This excludes November and December</li>
           <li><b>Buybox price:</b> The price currently being offered by a seller to win the Buy Box on Kaufland</li>
           <li><b>Priority Score:</b> The relevance of the item in relation to views on Kaufland. A lower score indicates that the item is viewed more frequently</li>
        </ul>
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/reports/product-data-changes", method="POST")
    async def request_product_data_changes_report(self, **kwargs) -> ApiResponse:
        """
        Queue a product data changes report
        
        Queues the generation of a CSV file that lists the important changes on products, for that the seller has provided offers. The generated file includes the following fields for each product data change:
        <ul>
           <li><b>ean:</b> EAN of the product</li>
           <li><b>title:</b> The title of the product</li>
           <li><b>changed_attributes:</b> Title and ID of an attribute, which value was changed</li>
           <li><b>date_changed:</b> The date of a value change</li>
           <li><b>id_item:</b> Kaufland's Product ID</li>
        </ul>
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        """
        return await self._request(kwargs.pop('path'), params=kwargs, add_storefront=True)

    @kaufland_endpoint("/reports/product-data-import-file-errors", method="POST")
    async def request_product_data_import_file_errors_report(self, **kwargs) -> ApiResponse:
        """
        Queue a product data import file errors report
        
        Queues the generation of a CSV file that contains a list of errors, occured during import of product data file with id <code>id_import_file</code>. The generated file includes the following fields for each error:
        <ul>
           <li><b>ean:</b> The EAN of the item</li>
           <li><b>id_attribute:</b> The ID of the attribute</li>
           <li><b>status:</b> Status of error</li>
           <li><b>log_message:</b> Log message</li>
           <li><b>type_hook:</b> Type of the hook</li>
        </ul>
        
        Args:
        body: RequestProductDataImportFileErrorsReportRequest | required (body)
        """
        body = kwargs.pop('body', None)
        return await self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=False)

    @kaufland_endpoint("/reports/sales-new", method="POST")
    async def request_new_sales_report(self, **kwargs) -> ApiResponse:
        """
        Queue a sales report
        
        Queues the generation of a CSV file that contains a list of all of your sales on or after the given <code>date_from</code> timestamp and on or before the given <code>date_to</code> timestamp.
        
        Args:
        storefront: Storefront | required (query) Parameter to select the affected storefront
        body: RequestNewSalesReportRequest | required (body)
        """
        body = kwargs.pop('body', None)
        return await self._request(kwargs.pop('path'), data=body, params=kwargs, add_storefront=True)

    @kaufland_endpoint("/reports/{}", method="GET")
    async def get_report(self, id_report, **kwargs) -> ApiResponse:
        """
        Get meta-data for a single report by ID
        
        Returns the full meta-data for a single report, specified by ID. You can download the report itself by requesting the file in the "url" property of the response, as long as the report is in the <code>done</code> state. To get a list of the IDs of your reports, use the <code>/reports/seller/</code> endpoint.     * @summary Get meta-data for a single report by its ID.
        
        Args:
        id_report: LongInteger | required (path)
        """
        return await self._request(fill_query_params(kwargs.pop('path'), id_report), params=kwargs, add_storefront=False)
