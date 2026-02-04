import os

from .credential_provider import CredentialProvider


class BaseClient:
    default_endpoint = "https://sellerapi.kaufland.com/v2"

    def __init__(
        self,
        *,
        account="default",
        credentials=None,
        credential_providers=None,
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
    ):
        if credentials is None:
            credentials = {}
        provided = {
            "client_key": client_key,
            "secret_key": secret_key,
            "user_agent": user_agent,
            "partner_client_key": partner_client_key,
            "partner_secret_key": partner_secret_key,
        }
        credentials = {**credentials, **{k: v for k, v in provided.items() if v is not None}}

        self.credentials = CredentialProvider(
            account,
            credentials,
            credential_providers=credential_providers,
        ).credentials

        self.client_key = self.credentials["client_key"]
        self.secret_key = self.credentials["secret_key"]
        self.partner_client_key = self.credentials.get("partner_client_key")
        self.partner_secret_key = self.credentials.get("partner_secret_key")
        self.user_agent = (
            user_agent
            or self.credentials.get("user_agent")
            or os.environ.get("KAUFLAND_USER_AGENT")
            or "kaufland-python"
        )

        self.endpoint = endpoint or os.environ.get(
            "KAUFLAND_API_ENDPOINT", self.default_endpoint
        )
        self.storefront = storefront or os.environ.get("KAUFLAND_STOREFRONT")
        self.signature_encoding = (
            signature_encoding
            or os.environ.get("KAUFLAND_SIGNATURE_ENCODING", "hex")
        ).lower()
        if self.signature_encoding not in {"hex", "base64"}:
            raise ValueError("signature_encoding must be 'hex' or 'base64'")
        self.proxies = proxies
        self.verify = verify
        self.timeout = timeout
        self.version = version

    def _check_version(self, path: str) -> str:
        if "<version>" not in path or not self.version:
            return path
        return path.replace("<version>", self.version)

    @property
    def headers(self):
        return {
            "Accept": "application/json",
            "Shop-Client-Key": self.client_key,
            "User-Agent": self.user_agent,
        }
