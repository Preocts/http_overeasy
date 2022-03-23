from __future__ import annotations

import json
import logging
from typing import Any
from urllib import parse

import urllib3
from http_overeasy.response import Response

RETRY_TOTAL = 3
RETRY_BACKOFF_FACTOR = 2
RETRY_RAISE_ON_STATUS = False
RETRY_RAISE_ON_REDIRECT = True
RETRY_STATUS_FORCELIST = [500, 502, 503, 504]
RETRY_ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


class HTTPClient:
    """Provides HTTPS connection pool and REST methods"""

    def __init__(
        self,
        *,
        headers: dict[str, str] | None = None,
        max_pool: int = 10,
    ) -> None:
        self.log = logging.getLogger(__name__)
        self.http = self._connection(max_pool)
        self.headers = self._format_headers(headers) if headers else None

    def _connection(self, max_pool: int) -> urllib3.PoolManager:
        """Returns HTTP pool manager with retries and backoff"""
        return urllib3.PoolManager(
            num_pools=max_pool,
            retries=urllib3.Retry(
                total=RETRY_TOTAL,
                backoff_factor=RETRY_BACKOFF_FACTOR,
                raise_on_status=RETRY_RAISE_ON_STATUS,
                raise_on_redirect=RETRY_RAISE_ON_REDIRECT,
                status_forcelist=RETRY_STATUS_FORCELIST,
                allowed_methods=RETRY_ALLOWED_METHODS,
            ),
        )

    def get(
        self,
        url: str,
        fields: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """
        GET method with Response model returned

        Args:
            url: HTTPS URL of target
            fields: {key:value} dict of fields to be translated to urlecoded string
            headers: Optional headers to use over global headers

        Returns:
            Response
        """
        return self._request_with_field("GET", url, fields, headers)

    def delete(
        self,
        url: str,
        fields: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """
        DELETE method with Response model returned

        Args:
            url: HTTPS URL of target
            fields: {key:value} dict of fields to be translated to urlecoded string
            headers: Optional headers to use over global headers

        Returns:
            Response
        """
        return self._request_with_field("DELETE", url, fields, headers)

    def post(
        self,
        url: str,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """
        POST method with Response model returned

        Args:
            url: HTTPS URL of target
            body: {key:value} dict of payload to be delivered
            headers: Optional headers to use over global headers
            urlencode: When true, body is sent as urlencoded string

        Returns:
            Response
        """
        return self._request_with_body("POST", url, body, headers)

    def put(
        self,
        url: str,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """
        PUT method with Response model returned

        Args:
            url: HTTPS URL of target
            body: {key:value} dict of payload to be delivered
            headers: Optional headers to use over global headers
            urlencode: When true, body is sent as urlencoded string

        Returns:
            Response
        """
        return self._request_with_body("PUT", url, body, headers)

    def patch(
        self,
        url: str,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """
        PATCH method with Response model returned

        Args:
            url: HTTPS URL of target
            body: {key:value} dict of payload to be delivered
            headers: Optional headers to use over global headers
            urlencode: When true, body is sent as urlencoded string

        Returns:
            Response
        """
        return self._request_with_body("PATCH", url, body, headers)

    def _request_with_body(
        self,
        method: str,
        url: str,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Internal: Handles POST, PUT, and PATCH"""
        headers = self._format_headers(headers) if headers is not None else self.headers

        if self._is_urlencoded(headers):
            request_body = parse.urlencode(body or {}, doseq=True)
        else:
            request_body = json.dumps(body)

        resp = Response(
            self.http.request(
                method=method.upper(),
                url=url,
                body=request_body,
                headers=headers,
            )
        )
        return resp

    def _request_with_field(
        self,
        method: str,
        url: str,
        fields: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Response:
        """Internal: Handles GET and DELETE"""
        headers = self._format_headers(headers) if headers is not None else self.headers

        resp = Response(
            self.http.request(
                method=method.upper(),
                url=url,
                fields=fields,
                headers=headers,
            )
        )
        return resp

    @staticmethod
    def _is_urlencoded(headers: dict[str, str] | None) -> bool:
        """Determine how to encode the body"""
        if headers is not None:
            return not headers.get("content-type", "") == "application/json"
        return False

    @staticmethod
    def _format_headers(headers: dict[str, str]) -> dict[str, str]:
        """Adjust all keys to lower-case"""
        return {key.lower(): value for key, value in headers.items()}
