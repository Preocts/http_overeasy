import json

import pytest
from http_overeasy.client_mocker import ClientMocker

MOCK_RESP = {"test": "test"}
MOCK_HEADER = {"header": "mock"}
MOCK_STATUS = 999
MOCK_URL = "https://github.com/Preocts/https_overeasy"


def test_is_empty() -> None:
    client = ClientMocker()

    result = client.is_empty()

    assert result is True


def test_is_not_empty() -> None:
    client = ClientMocker()
    client.add_response(MOCK_RESP, MOCK_HEADER, MOCK_STATUS, MOCK_URL)

    result = client.is_empty()

    assert result is False


@pytest.mark.parametrize(
    ("method",),
    (("get",), ("put",), ("patch",), ("post",), ("delete",)),
)
def test_add_response_dict_all_calls(method: str) -> None:
    # We can simplify here as all methods will return the same stored response
    client = ClientMocker()
    client.add_response(MOCK_RESP, MOCK_HEADER, MOCK_STATUS, MOCK_URL)

    result = getattr(client, method)(url=MOCK_URL)

    assert result.text == json.dumps(MOCK_RESP)
    assert result.status == MOCK_STATUS
    assert result.headers == MOCK_HEADER


def test_add_response_list() -> None:
    client = ClientMocker()
    resp = [MOCK_RESP for _ in range(10)]
    client.add_response(resp, MOCK_HEADER, MOCK_STATUS, MOCK_URL)

    result = client.get(MOCK_URL)

    assert result.json() == resp


def test_add_response_str() -> None:
    client = ClientMocker()
    resp = json.dumps(MOCK_RESP)
    client.add_response(resp, MOCK_HEADER, MOCK_STATUS, MOCK_URL)

    result = client.get(MOCK_URL)

    assert result.text == resp


def test_add_response_byte() -> None:
    client = ClientMocker()
    resp = json.dumps(MOCK_RESP).encode()
    client.add_response(resp, MOCK_HEADER, MOCK_STATUS, MOCK_URL)

    result = client.get(url=MOCK_URL)

    assert result.text == resp.decode()


def test_url_mismatch_positional() -> None:
    client = ClientMocker()
    client.add_response(MOCK_RESP, MOCK_HEADER, MOCK_STATUS, MOCK_URL)

    with pytest.raises(ValueError, match="URL match failed:"):
        client.get("https://github.com")


def test_url_match_partial() -> None:
    client = ClientMocker()
    client.add_response(MOCK_RESP, MOCK_HEADER, MOCK_STATUS, MOCK_URL, True)

    result = client.get(MOCK_URL[:10])

    assert result.headers == MOCK_HEADER
