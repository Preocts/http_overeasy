from __future__ import annotations

import json
from typing import Any

from http_overeasy.response import Response
from urllib3.response import HTTPResponse


class ClientMocker:
    def __init__(self) -> None:
        """Creates a mock HTTP client for use in unit-tests"""
        self._urls: list[str] = []
        self._headers: list[dict[str, str]] = []
        self._responses: list[bytes] = []
        self._statuses: list[int] = []
        self._partial_url_allowed: list[bool] = []
        self.called = 0

    def is_empty(self) -> bool:
        """True when all added responses have been used"""
        return not any([self._urls, self._headers, self._responses, self._statuses])

    def add_response(
        self,
        response_body: dict[str, Any] | str | bytes,
        response_headers: dict[str, str],
        status: int,
        url: str,
        partial_url_allowed: bool = False,
    ) -> None:
        """
        Add response to mock. Replayed in order added (FIFO)

        Args:
            response_body: Expect response from call
            response_headers: Response Header dict
            status: Staus code of response
            url: URL must match that of the call
            partial_url_allow: If true, url is matched against .startswith()
        """
        self._urls.append(url)
        self._statuses.append(status)
        self._headers.append(response_headers)
        self._partial_url_allowed.append(partial_url_allowed)

        if isinstance(response_body, dict):
            response_body = json.dumps(response_body).encode()
        elif isinstance(response_body, str):
            response_body = response_body.encode()

        self._responses.append(response_body)

    def _check_call(self, *args: Any, **kwargs: Any) -> Response:
        """Check that url is expected, return response or None"""
        self.called += 1

        resp = Response(
            HTTPResponse(
                body=self._responses.pop(0),
                headers=self._headers.pop(0),
                status=self._statuses.pop(0),
            )
        )

        match_url = self._urls.pop(0)
        call_url = kwargs["url"] if "url" in kwargs else args[0]

        if self._partial_url_allowed.pop(0):
            url_found = match_url.startswith(call_url)
        else:
            url_found = match_url == call_url

        if url_found:
            return resp

        raise ValueError(f"URL match failed: '{match_url}' vs '{call_url}'")

    def get(self, *args: Any, **kwargs: Any) -> Response:
        """Mocks http_client method"""
        return self._check_call(*args, **kwargs)

    def put(self, *args: Any, **kwargs: Any) -> Response:
        """Mocks http_client method"""
        return self._check_call(*args, **kwargs)

    def post(self, *args: Any, **kwargs: Any) -> Response:
        """Mocks http_client method"""
        return self._check_call(*args, **kwargs)

    def patch(self, *args: Any, **kwargs: Any) -> Response:
        """Mocks http_client method"""
        return self._check_call(*args, **kwargs)

    def delete(self, *args: Any, **kwargs: Any) -> Response:
        """Mocks http_client method"""
        return self._check_call(*args, **kwargs)
