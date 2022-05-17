from __future__ import annotations

import json
from typing import Any
from typing import Dict
from typing import Generator
from typing import Optional
from typing import Tuple
from unittest.mock import MagicMock
from unittest.mock import patch
from urllib import parse

import pytest
from http_overeasy import http_client as http_client
from http_overeasy.http_client import HTTPClient
from http_overeasy.response import Response
from urllib3.response import HTTPResponse

MAX_POOLS = 2
MOCK_HEADERS_JSON = {"content-type": "application/json"}
MOCK_HEADERS_PATCH_JSON = {"content-type": "application/json-patch+json"}
MOCK_HEADERS_URLE = {"content-type": "application/x-www-form-urlencoded"}


@pytest.fixture
def base_client() -> Generator[HTTPClient, None, None]:
    client = HTTPClient()
    yield client
    client.http.clear()


@pytest.fixture
def test_client() -> Generator[HTTPClient, None, None]:
    client = HTTPClient(max_pool=MAX_POOLS, headers=MOCK_HEADERS_JSON)
    yield client
    client.http.clear()


@pytest.fixture
def patch_client() -> Generator[HTTPClient, None, None]:
    client = HTTPClient()
    mock_resp = HTTPResponse(
        body=b'{"key": "value"}',
        status=200,
        headers={},
    )

    mock_request = MagicMock(return_value=mock_resp)
    with patch.object(client, "http", new=MagicMock(request=mock_request)):
        yield client
        client.http.clear()


@pytest.fixture(params=(["post", "patch", "put"]))
def send_fixtures(
    patch_client: HTTPClient,
    request: Any,
) -> Generator[Tuple[HTTPClient, str], None, None]:
    """Methods that send data to an API: POST, PATCH, PUT"""
    yield patch_client, request.param


@pytest.fixture(params=(["get", "delete"]))
def fetch_fixtures(
    patch_client: HTTPClient,
    request: Any,
) -> Generator[Tuple[HTTPClient, str], None, None]:
    """Methods that fetch data from an API: GET, DELETE"""
    yield patch_client, request.param


def test_custom_connection_pool_count(test_client: HTTPClient) -> None:
    assert test_client.http.pools._maxsize == MAX_POOLS


def test_global_headers_provided(test_client: HTTPClient) -> None:
    assert test_client.headers == MOCK_HEADERS_JSON


def test_empty_headers_on_init(base_client: HTTPClient) -> None:
    assert base_client.headers is None


def test_default_constants(base_client: HTTPClient) -> None:
    init_values = base_client.http.connection_pool_kw["retries"]
    assert init_values.total == http_client.RETRY_TOTAL
    assert init_values.backoff_factor == http_client.RETRY_BACKOFF_FACTOR
    assert init_values.raise_on_status == http_client.RETRY_RAISE_ON_STATUS
    assert init_values.raise_on_redirect == http_client.RETRY_RAISE_ON_REDIRECT
    assert init_values.status_forcelist == http_client.RETRY_STATUS_FORCELIST
    assert init_values.allowed_methods == http_client.RETRY_ALLOWED_METHODS


@pytest.mark.parametrize(
    argnames=("url", "fields", "headers"),
    argvalues=(
        ("https://google.com", {"test": "test01"}, MOCK_HEADERS_JSON),
        ("https://google.com", None, MOCK_HEADERS_URLE),
        ("https://google.com", {"test": "test01"}, None),
        ("", None, None),
    ),
)
def test_fetch_methods(
    url: str,
    fields: Optional[Dict[str, Any]],
    headers: Optional[Dict[str, str]],
    fetch_fixtures: Tuple[HTTPClient, str],
) -> None:
    patch_client, send_method = fetch_fixtures
    result = getattr(patch_client, send_method)(url, fields, headers)

    assert isinstance(result, Response)

    patch_client.http.request.assert_called_once()
    patch_client.http.request.assert_called_with(
        url=url,
        fields=fields,
        headers=headers,
        method=send_method.upper(),
    )


# NOTE: fixture is using content-type application/json by default
@pytest.mark.parametrize(
    argnames=("url", "body", "headers", "urlencode"),
    argvalues=(
        ("https://google.com", {"test": "test01"}, MOCK_HEADERS_JSON, False),
        ("https://google.com", None, MOCK_HEADERS_JSON, False),
        ("https://google.com", {"test": "test01"}, None, False),
        ("", None, None, False),
        ("https://google.com", {"test": "test01"}, MOCK_HEADERS_URLE, True),
        ("https://google.com", None, MOCK_HEADERS_URLE, True),
        ("https://google.com", {"test": "test01"}, None, False),
        ("", None, None, False),
    ),
)
def test_send_methods(
    url: str,
    body: Optional[Dict[str, Any]],
    headers: Optional[Dict[str, str]],
    urlencode: bool,
    send_fixtures: Tuple[HTTPClient, str],
) -> None:
    patch_client, send_method = send_fixtures
    result = getattr(patch_client, send_method)(url, body, headers)

    assert isinstance(result, Response)
    if urlencode:
        expected_body = parse.urlencode(body or {}, doseq=True)
    else:
        expected_body = json.dumps(body)

    patch_client.http.request.assert_called_once()
    patch_client.http.request.assert_called_with(
        url=url,
        body=expected_body,
        headers=headers,
        method=send_method.upper(),
    )


def test_use_global_headers_with_fields(patch_client: HTTPClient) -> None:
    patch_client.headers = MOCK_HEADERS_JSON
    patch_client._request_with_field("GET", "", None, None)
    patch_client.http.request.assert_called_with(
        url="",
        fields=None,
        headers=MOCK_HEADERS_JSON,
        method="GET",
    )


def test_use_global_headers_with_body(patch_client: HTTPClient) -> None:
    patch_client.headers = MOCK_HEADERS_URLE
    patch_client._request_with_field("POST", "", None, None)
    patch_client.http.request.assert_called_with(
        url="",
        fields=None,
        headers=MOCK_HEADERS_URLE,
        method="POST",
    )


@pytest.mark.parametrize(
    ("headers", "expected"),
    (
        ({"content-type": "application/x-www-form-urlencoded"}, True),
        ({}, True),
        ({"content-type": "application/json"}, False),
        ({"content-type": "application/json-patch+json"}, False),
        (None, False),
    ),
)
def test_is_urlencoded(headers: dict[str, str] | None, expected: bool) -> None:
    result = HTTPClient._is_urlencoded(headers)

    assert result is expected


@pytest.mark.parametrize(
    ("headers", "expected"),
    (
        (
            {"Content-Type": "application/x-www-form-urlencoded"},
            {"content-type": "application/x-www-form-urlencoded"},
        ),
        ({}, {}),
        ({"content-type": "applicatoin/json"}, {"content-type": "applicatoin/json"}),
    ),
)
def test_format_headers(headers: dict[str, str], expected: dict[str, str]) -> None:
    result = HTTPClient._format_headers(headers)

    assert result == expected
