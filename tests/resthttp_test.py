import json
from typing import Any
from typing import Dict
from typing import Generator
from typing import Optional
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from http_overeasy import http_client as http_client
from http_overeasy.http_client import HTTPClient
from http_overeasy.response import Response
from urllib3.response import HTTPResponse

MAX_POOLS = 2
MOCK_HEADERS = {"Accept": "application/json"}


@pytest.fixture
def base_client() -> Generator[HTTPClient, None, None]:
    client = HTTPClient()
    yield client
    client.http.clear()


@pytest.fixture
def test_client() -> Generator[HTTPClient, None, None]:
    client = HTTPClient(max_pool=MAX_POOLS, headers=MOCK_HEADERS)
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


def test_custom_connection_pool_count(test_client: HTTPClient) -> None:
    assert test_client.http.pools._maxsize == MAX_POOLS


def test_global_headers_provided(test_client: HTTPClient) -> None:
    assert test_client.headers == MOCK_HEADERS


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
        ("https://google.com", {"test": "test01"}, MOCK_HEADERS),
        ("https://google.com", None, MOCK_HEADERS),
        ("https://google.com", {"test": "test01"}, None),
        ("", None, None),
    ),
)
def test_get_with_parameters(
    url: str,
    fields: Optional[Dict[str, Any]],
    headers: Optional[Dict[str, str]],
    patch_client: HTTPClient,
) -> None:
    result = patch_client.get(url, fields, headers)
    assert isinstance(result, Response)
    patch_client.http.request.assert_called_with(
        url=url,
        fields=fields,
        headers=headers,
        method="GET",
    )


@pytest.mark.parametrize(
    argnames=("url", "fields", "headers"),
    argvalues=(
        ("https://google.com", {"test": "test01"}, MOCK_HEADERS),
        ("https://google.com", None, MOCK_HEADERS),
        ("https://google.com", {"test": "test01"}, None),
        ("", None, None),
    ),
)
def test_delete_with_parameters(
    url: str,
    fields: Optional[Dict[str, Any]],
    headers: Optional[Dict[str, str]],
    patch_client: HTTPClient,
) -> None:
    result = patch_client.delete(url, fields, headers)
    assert isinstance(result, Response)
    patch_client.http.request.assert_called_with(
        url=url,
        fields=fields,
        headers=headers,
        method="DELETE",
    )


@pytest.mark.parametrize(
    argnames=("url", "body", "headers"),
    argvalues=(
        ("https://google.com", {"test": "test01"}, MOCK_HEADERS),
        ("https://google.com", None, MOCK_HEADERS),
        ("https://google.com", {"test": "test01"}, None),
        ("", None, None),
    ),
)
def test_post_with_parameters(
    url: str,
    body: Optional[Dict[str, Any]],
    headers: Optional[Dict[str, str]],
    patch_client: HTTPClient,
) -> None:
    result = patch_client.post(url, body, headers)
    assert isinstance(result, Response)
    patch_client.http.request.assert_called_with(
        url=url,
        body=json.dumps(body),
        headers=headers,
        method="POST",
    )


@pytest.mark.parametrize(
    argnames=("url", "body", "headers"),
    argvalues=(
        ("https://google.com", {"test": "test01"}, MOCK_HEADERS),
        ("https://google.com", None, MOCK_HEADERS),
        ("https://google.com", {"test": "test01"}, None),
        ("", None, None),
    ),
)
def test_put_with_parameters(
    url: str,
    body: Optional[Dict[str, Any]],
    headers: Optional[Dict[str, str]],
    patch_client: HTTPClient,
) -> None:
    result = patch_client.put(url, body, headers)
    assert isinstance(result, Response)
    patch_client.http.request.assert_called_with(
        url=url,
        body=json.dumps(body),
        headers=headers,
        method="PUT",
    )


@pytest.mark.parametrize(
    argnames=("url", "body", "headers"),
    argvalues=(
        ("https://google.com", {"test": "test01"}, MOCK_HEADERS),
        ("https://google.com", None, MOCK_HEADERS),
        ("https://google.com", {"test": "test01"}, None),
        ("", None, None),
    ),
)
def test_patch_with_parameters(
    url: str,
    body: Optional[Dict[str, Any]],
    headers: Optional[Dict[str, str]],
    patch_client: HTTPClient,
) -> None:
    result = patch_client.patch(url, body, headers)
    assert isinstance(result, Response)
    patch_client.http.request.assert_called_with(
        url=url,
        body=json.dumps(body),
        headers=headers,
        method="PATCH",
    )
