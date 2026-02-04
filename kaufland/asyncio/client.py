import logging

from ..base.ApiResponse import ApiResponse
from ..base.base_client import BaseClient
from ..base._core import prepare_request, parse_response, resolve_method
from ._transport_httpx import HttpxAsyncTransport

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Client(BaseClient):
    version = None

    def __init__(
        self,
        *,
        account="default",
        credentials=None,
        client_key=None,
        secret_key=None,
        user_agent=None,
        partner_client_key=None,
        partner_secret_key=None,
        signature_encoding=None,
        endpoint=None,
        storefront=None,
        proxies=None,
        verify=True,
        timeout=None,
        version=None,
        credential_providers=None,
    ):
        super().__init__(
            account=account,
            credentials=credentials,
            credential_providers=credential_providers,
            client_key=client_key,
            secret_key=secret_key,
            user_agent=user_agent,
            partner_client_key=partner_client_key,
            partner_secret_key=partner_secret_key,
            signature_encoding=signature_encoding,
            endpoint=endpoint,
            storefront=storefront,
            proxies=proxies,
            verify=verify,
            timeout=timeout,
            version=version,
        )

        self.version = version
        self._transport = HttpxAsyncTransport(
            timeout=timeout, proxies=proxies, verify=verify
        )

    async def _request(
        self,
        path: str,
        *,
        method: str | None = None,
        data: dict | str | bytes | None = None,
        params: dict | None = None,
        headers: dict | None = None,
        add_storefront: bool = True,
        res_no_data: bool = False,
        bulk: bool = False,
        wrap_list: bool = False,
    ) -> ApiResponse:
        method, params, data = resolve_method(params, data, method=method)
        self.method = method

        log.debug("HTTP Method: %s", method)
        log.debug("Request path: %s", path)
        log.debug("Request Params: %s", params)
        log.debug("Request Data: %s", data)
        request_headers = headers or self.headers
        log.debug("Request Headers: %s", request_headers)

        prepared = prepare_request(
            method=method,
            endpoint=self.endpoint,
            path=path,
            params=params,
            data=data,
            headers=request_headers,
            add_storefront=add_storefront,
            storefront=self.storefront,
            version=self.version,
            client_key=self.client_key,
            secret_key=self.secret_key,
            user_agent=self.user_agent,
            partner_client_key=self.partner_client_key,
            partner_secret_key=self.partner_secret_key,
            signature_encoding=self.signature_encoding,
        )

        log.debug("Making request to URL: %s", prepared["url"])
        res = await self._transport.request(**prepared)
        return self._check_response(res, res_no_data, bulk, wrap_list)

    def _check_response(
        self,
        res,
        res_no_data: bool = False,
        bulk: bool = False,
        wrap_list: bool = False,
    ) -> ApiResponse:
        response = parse_response(
            res,
            method=self.method,
            res_no_data=res_no_data,
            bulk=bulk,
            wrap_list=wrap_list,
        )
        log.debug("Response: %s", response)
        return response

    async def close(self):
        await self._transport.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.close()
