import os

from .exceptions import MissingCredentialsException


class CredentialProvider:
    def __init__(self, account="default", credentials=None, credential_providers=None):
        self.account = account
        self.credentials = self._resolve(credentials, credential_providers)

    def _resolve(self, credentials, credential_providers):
        if credentials is None:
            credentials = {}

        if isinstance(credentials, dict) and self.account in credentials:
            credentials = credentials[self.account] or {}

        if not isinstance(credentials, dict):
            raise MissingCredentialsException("Credentials must be a dict")

        provided = {}
        if credential_providers:
            for provider in credential_providers:
                value = provider(account=self.account) if callable(provider) else None
                if value:
                    provided.update(value)

        env = {
            "client_key": os.environ.get("KAUFLAND_CLIENT_KEY"),
            "secret_key": os.environ.get("KAUFLAND_SECRET_KEY"),
            "user_agent": os.environ.get("KAUFLAND_USER_AGENT"),
            "partner_client_key": os.environ.get("KAUFLAND_PARTNER_CLIENT_KEY"),
            "partner_secret_key": os.environ.get("KAUFLAND_PARTNER_SECRET_KEY"),
        }

        merged = {**env, **provided, **credentials}
        if not merged.get("client_key") or not merged.get("secret_key"):
            raise MissingCredentialsException(
                "Missing Kaufland credentials. Set KAUFLAND_CLIENT_KEY and "
                "KAUFLAND_SECRET_KEY or pass credentials explicitly."
            )
        return merged
