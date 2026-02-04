
import pytest

from kaufland.base.credential_provider import CredentialProvider
from kaufland.base.exceptions import MissingCredentialsException


def test_credentials_from_env(monkeypatch):
    monkeypatch.setenv("KAUFLAND_CLIENT_KEY", "ck")
    monkeypatch.setenv("KAUFLAND_SECRET_KEY", "sk")
    monkeypatch.setenv("KAUFLAND_PARTNER_CLIENT_KEY", "pck")
    monkeypatch.setenv("KAUFLAND_PARTNER_SECRET_KEY", "psk")

    provider = CredentialProvider("default", credentials=None)
    assert provider.credentials["client_key"] == "ck"
    assert provider.credentials["secret_key"] == "sk"
    assert provider.credentials["partner_client_key"] == "pck"
    assert provider.credentials["partner_secret_key"] == "psk"


def test_credentials_from_account_dict():
    provider = CredentialProvider(
        "default",
        credentials={
            "default": {
                "client_key": "ck",
                "secret_key": "sk",
                "user_agent": "ua",
            }
        },
    )
    assert provider.credentials["client_key"] == "ck"
    assert provider.credentials["secret_key"] == "sk"


def test_missing_credentials_raises(monkeypatch):
    monkeypatch.delenv("KAUFLAND_CLIENT_KEY", raising=False)
    monkeypatch.delenv("KAUFLAND_SECRET_KEY", raising=False)
    with pytest.raises(MissingCredentialsException):
        CredentialProvider("default", credentials=None)
