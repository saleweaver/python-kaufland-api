class KauflandException(Exception):
    """Base exception for the Kaufland API client."""


class MissingCredentialsException(KauflandException):
    """Raised when required API credentials are missing."""


class ApiException(KauflandException):
    """Raised when the API returns an error response."""

    def __init__(self, *, status_code=None, payload=None, headers=None, text=None):
        super().__init__(self._build_message(status_code, payload, text))
        self.status_code = status_code
        self.payload = payload
        self.headers = headers or {}
        self.text = text

    @staticmethod
    def _build_message(status_code, payload, text):
        if payload:
            return f"API error {status_code}: {payload}"
        if text:
            return f"API error {status_code}: {text}"
        return f"API error {status_code}"
