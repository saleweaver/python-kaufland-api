import httpx


class HttpxAsyncTransport:
    def __init__(self, *, timeout=None, proxies=None, verify=True):
        kwargs = {"timeout": timeout, "verify": verify}
        if proxies is not None:
            kwargs["proxies"] = proxies
        try:
            self._client = httpx.AsyncClient(**kwargs)
        except TypeError as exc:
            if "proxies" in kwargs:
                kwargs["proxy"] = kwargs.pop("proxies")
                self._client = httpx.AsyncClient(**kwargs)
            else:
                raise exc

    async def request(self, *, method, url, headers=None, content=None):
        return await self._client.request(method, url, headers=headers, content=content)

    async def close(self):
        await self._client.aclose()
