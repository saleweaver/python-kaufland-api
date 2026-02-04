import httpx


class HttpxAsyncTransport:
    def __init__(self, *, timeout=None, proxies=None, verify=True):
        self._client = httpx.AsyncClient(timeout=timeout, proxies=proxies, verify=verify)

    async def request(self, *, method, url, headers=None, content=None):
        return await self._client.request(method, url, headers=headers, content=content)

    async def close(self):
        await self._client.aclose()
