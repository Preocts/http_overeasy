[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/http_overeasy/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/http_overeasy/main)
[![Python package](https://github.com/preocts/http_overeasy/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/preocts/http_overeasy/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/Preocts/http_overeasy/branch/main/graph/badge.svg?token=DLlntDhEnI)](https://codecov.io/gh/Preocts/http_overeasy)

# http_overeasy

Personal `urllib3` wrapper.

## Requirements

- [Python](https://python.org) >= 3.8
- [urllib3](https://pypi.org/project/urllib3/) >= 1.26.9

## Internal Links

- [Development Installation Guide](docs/development.md)

---

## Install from GitHub with `pip`

Replace `vX.X.X` with desired release version.

```bash
python -m pip install git+https://github.com/Preocts/http_overeasy.git@vX.X.X
```

---

## `HTTPClient` Object

This is the primary wrapper around `urllib3`. It provides quick REST methods for target URLs.  Headers can be defined at class initialization and/or in any given call.

Default behavior for payloads is to deliver them as `application/json`.

**Default Retry Policy**

```py
RETRY_TOTAL = 3
RETRY_BACKOFF_FACTOR = 2
RETRY_RAISE_ON_STATUS = False
RETRY_RAISE_ON_REDIRECT = True
RETRY_STATUS_FORCELIST = [500, 502, 503, 504]
RETRY_ALLOWED_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]
```

**Keyword Arguments**

- `headers` : `dict[str, str] | None` (default: `None`)
  - Define global headers that will be used for all requests unless alternative headers are provided in those requests
- `max_pool` : `int` (default: `10`)
  - Maximum number of pools for `urllib3.PoolManager` to allow

**Attributes**

- `http` : `urllib3.PoolManager`
  - Direct access, if needed, to `urllib3` object
- `headers` : `dict[str, str] | None`
  - Global headers applied to all requests unless otherwise provided in method call

**Methods**

  - `get(...)`
    - GET method with Response model returned
    - Args:
      - `url` : `str`
        - HTTPS URL of target
      - `fields` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of fields to be translated to urlecoded string
      - `headers` `dict[str, str] | None` (default: `None`)
        - Optional headers to use over global headers
    - Returns:
      - `Response`
  - `delete(...)`
    - DELETE method with Response model returned
    - Args:
      - `url` : `str`
        - HTTPS URL of target
      - `fields` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of fields to be translated to urlecoded string
      - `headers` `dict[str, str] | None` (default: `None`)
        - Optional headers to use over global headers
    - Returns:
      - `Response`
  - `post(...)`
    - POST method with Response model returned
    - Args:
      - `url` : `str`
        - HTTPS URL of target
      - `body` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of payload to be delivered
      - `headers` `dict[str, str] | None` (default: `None`)
        - Optional headers to use over global headers
    - Returns:
      - `Response`
  - `put(...)`
    - PUT method with Response model returned
    - Args:
      - `url` : `str`
        - HTTPS URL of target
      - `body` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of payload to be delivered
      - `headers` `dict[str, str] | None` (default: `None`)
        - Optional headers to use over global headers
    - Returns:
      - `Response`
  - `patch(...)`
    - PATCH method with Response model returned
    - Args:
      - `url` : `str`
        - HTTPS URL of target
      - `body` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of payload to be delivered
      - `headers` `dict[str, str] | None` (default: `None`)
        - Optional headers to use over global headers
    - Returns:
      - `Response`


## `Response` Object

All `HTTPResponses` are wrapped in a custom model that provides quick access to data.

**Attributes**

- `http_response` : `urllib3.response.HTTPResponse`
  - The original `HTTPResponse` object as returned by `urllib3`

**Methods**

- `has_success` : `bool`
  - Boolean mark of a response code of 200 to 299
- `get_body` : `str | None`
  - UTF-8 decoded response body
- `get_status` : `int`
  - Status code of response
- `get_json` : `dict[str, Any] | None`
  - JSON decoded dict of response body
  - Note: will be `None` if response is not valid JSON


## `ClientMocker` Object

Used to patch the `HTTPClient` in unit tests. Add responses which are returned when CRUD methods are called. Suggested to use `unittest.mock.patch.object` to patch use of `HTTPClient` in tests.

**Attributes**

- `called` : `int`
  - Number of times the mocker was called

**Methods**

- `is_empty` : `bool`
  - True when all added responses have been used
  - Note: Will be true if no responses have been added
- `add_response` : `None`
  - Add response to mock. Replayed in order added (FIFO)
  - Args:
    - response_body: Expect response from call
    - response_headers: Response Header dict
    - status: Staus code of response
    - url: URL must match that of the call
    - partial_url_allow: If true, url is matched against .startswith()
