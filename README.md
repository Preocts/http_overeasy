[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci
status](https://results.pre-commit.ci/badge/github/preocts/http_overeasy/main.svg)](https://results.pre-commit.ci/latest/github/preocts/http_overeasy/main)
[![Python
package](https://github.com/preocts/http_overeasy/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/preocts/http_overeasy/actions/workflows/python-tests.yml)

# http_overeasy

Personal `urllib3` wrapper.

## Requirements

- [Python](https://python.org) >= 3.8

## Internal Links

- [Development Installation Guide](docs/development.md)
- [Repo documentation](docs/)

---

## `Response` Object

All `HTTPResponses` are wrapped in a custom model that provides quick access to data.

### Attributes

- `http_response` : `urllib3.response.HTTPResponse`
  - The original `HTTPResponse` object as returned by `urllib3`

### Methods

- `has_success` : `bool`
  - Boolean mark of a response code of 200 to 299
- `get_body` : `Optional[str]`
  - UTF-8 decoded response body
- `get_status` : `int`
  - Status code of response
- `get_json` : `Optional[Dict[str, Any]]`
  - JSON decoded dict of response body
  - Note: will be `None` if response is not valid JSON
-
