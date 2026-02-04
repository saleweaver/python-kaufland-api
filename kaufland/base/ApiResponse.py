class ApiResponse:
    def __init__(self, payload=None, headers=None, status_code=None, raw=None):
        self.payload = payload
        self.headers = headers or {}
        self.status_code = status_code
        self.raw = raw

    @property
    def errors(self):
        if isinstance(self.payload, dict):
            return self.payload.get("errors") or self.payload.get("error")
        return None

    def __repr__(self):
        return (
            f"ApiResponse(status_code={self.status_code}, "
            f"payload_type={type(self.payload).__name__})"
        )
