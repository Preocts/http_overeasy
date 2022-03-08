import json
from typing import Any
from typing import Dict
from typing import Optional

from urllib3.response import HTTPResponse


class Response:
    def __init__(self, http_response: HTTPResponse) -> None:
        self.http_response = http_response
        self._body = self.http_response.data

    def has_success(self) -> bool:
        """determines if status code returned is 200-299"""
        return self.http_response.status in range(200, 300)

    def get_headers(self) -> Dict[str, Any]:
        """response headers"""
        return dict(self.http_response.headers)

    def get_body(self) -> Optional[str]:
        """utf-8 decoded response body"""
        return self._body.decode("utf-8") if self._body is not None else None

    def get_status(self) -> int:
        """status code of response"""
        return self.http_response.status

    def get_json(self) -> Optional[Dict[str, Any]]:
        """json body as a dict if response body is valid json, else None"""
        try:
            return json.loads(self.get_body() or "")
        except json.JSONDecodeError:
            return None
