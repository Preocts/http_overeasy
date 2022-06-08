from __future__ import annotations

from json import JSONDecodeError
from typing import Any
from typing import NamedTuple

import pytest
from http_overeasy.response import Response
from urllib3.response import HTTPResponse


RESP_HEADERS = {
    "Date": "Mon, 29, Jan 2022 12:00:00 GMT",
    "Server": "EggCarton v1 (endless)",
    "Content-Length": "0",
    "Content-Type": "application/json",
    "Connection": "closed",
}


class ResponseObj(NamedTuple):
    resp: Response
    status: int
    body: bytes | None
    has_success: bool
    is_json: bool


@pytest.fixture(
    params=[
        (200, b"{}", True, True),  # Empty Dict
        (200, b"", True, False),  # Empty String
        (200, None, True, False),  # None edge case
        (201, b'{"key": "value"}', True, True),  # JSON
        (202, b"Succes was found.", True, False),  # Not JSON
        (204, b'{"key": "value}', True, False),  # Invalid JSON
        (404, b"Not Found", False, False),  # Not JOSN
        (508, b'{"error": "error"', False, False),  # Invalid JSON
        (500, b'{"error": "error"}', False, True),  # JSON
    ],
)
def response_obj(request: Any) -> ResponseObj:
    status, body, has_success, is_json = request.param
    return ResponseObj(
        resp=Response(HTTPResponse(body=body, status=status, headers=RESP_HEADERS)),
        status=status,
        body=body,
        has_success=has_success,
        is_json=is_json,
    )


def test_get_headers(response_obj: ResponseObj) -> None:
    assert response_obj.resp.headers == RESP_HEADERS


def test_has_success(response_obj: ResponseObj) -> None:
    assert response_obj.resp.has_success() is response_obj.has_success


def test_body_capture(response_obj: ResponseObj) -> None:
    if response_obj.body is None:
        assert response_obj.resp.text == ""
    else:
        assert response_obj.resp.text == response_obj.body.decode("utf-8")


def test_get_status_code(response_obj: ResponseObj) -> None:
    assert response_obj.resp.status_code == response_obj.status


def test_get_json(response_obj: ResponseObj) -> None:
    if response_obj.is_json:
        assert isinstance(response_obj.resp.json(), dict)
    else:
        with pytest.raises(JSONDecodeError):
            response_obj.resp.json()
