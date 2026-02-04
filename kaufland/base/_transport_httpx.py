import httpx


class HttpxTransport:
    def __init__(self, *, timeout=None, proxies=None, verify=True):
        kwargs = {"timeout": timeout, "verify": verify}
        if proxies is not None:
            kwargs["proxies"] = proxies
        try:
            self._client = httpx.Client(**kwargs)
        except TypeError as exc:
            if "proxies" in kwargs:
                kwargs["proxy"] = kwargs.pop("proxies")
                self._client = httpx.Client(**kwargs)
            else:
                raise exc

    def request(self, *, method, url, headers=None, content=None):
        return self._client.request(method, url, headers=headers, content=content)

    def close(self):
        self._client.close()
