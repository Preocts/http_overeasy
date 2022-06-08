"""Model response object."""
from __future__ import annotations

import json
from typing import Any

from urllib3.response import HTTPResponse


class Response:
    def __init__(self, http_response: HTTPResponse) -> None:
        """Initialize response object."""
        self.http_response = http_response
        self._body = self.http_response.data

    @property
    def status(self) -> int:
        """Status code of response."""
        return self.http_response.status

    @property
    def text(self) -> str:
        """UTF-8 decoded response body."""
        return self._body.decode("utf-8") if self._body else ""

    @property
    def headers(self) -> dict[str, Any]:
        """Response headers."""
        return dict(self.http_response.headers)

    def has_success(self) -> bool:
        """Determine if status code returned is 200-299."""
        return self.http_response.status in range(200, 300)

    def json(self) -> dict[str, Any] | None:
        """JSON body as a dict if response body is valid json, else None."""
        return json.loads(self.text)
