[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/http_overeasy/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/http_overeasy/main)
[![Python package](https://github.com/preocts/http_overeasy/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/preocts/http_overeasy/actions/workflows/python-tests.yml)

# http_overeasy

## Public Archive - 2022-10-02

Personal `urllib3` wrapper.

This is a lightweight library meant for prototyping. For more verbose
development options you should consider
[`httpx`](https://pypi.org/project/httpx/).

**Why?**

I work in many environments where I'm behind a VPN and certificate proxy. Common
libraries such as `requests` and `httpx` often need additional system setup such
as cert files and environment variables to allow them to work. They are also
just big. ~2.4 MB for `requests` and ~3.5 MB for `httpx` doesn't feel like much.
However, this lib weighs in at ~900 KB which on some of the systems I have to
use makes the difference.

That's what this library answers for me. It's a clean, simple wrapper around
`urllib3` for standard REST actions.  It has a data model for responses which
mimics `requests` and `httpx` response attributes for easier converting. It also
has a mocking object that allows me to stay fast even while writing tests.


## Requirements

- [Python](https://python.org) >= 3.7
- [urllib3](https://pypi.org/project/urllib3/) >= 1.26.9

---

## Install from GitHub with `pip`

Replace `vX.X.X` with desired release version.

```bash
python -m pip install git+https://github.com/Preocts/http_overeasy.git@vX.X.X
```

---

## Examples:

See: [Examples folder](examples/)

## `HTTPClient` Object

This is the primary wrapper around `urllib3`. It provides quick REST methods for
target URLs.  Headers can be defined at class initialization and/or in any given
call.

Default behavior for payloads is to deliver them as urlencoded strings.  This
behavior is overridden by `content-type` within the headers. If `json` is found
in the `content-type` then a json serialized payload is delivered.

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
  - Define global headers that will be used for all requests unless alternative
    headers are provided in those requests
- `max_pool` : `int` (default: `10`)
  - Maximum number of pools for `urllib3.PoolManager` to allow

**Attributes**

- `http` : `urllib3.PoolManager`
  - Direct access, if needed, to `urllib3` object
- `headers` : `dict[str, str] | None`
  - Global headers applied to all requests unless otherwise provided in method
    call

**Methods**

  - `get(...)`
    - GET method with Response model returned
    - Args:
      - `url` : `str`
        - HTTPS URL of target
    - Keyword Args:
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
    - Keyword Args:
      - `fields` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of fields to be translated to urlecoded string
      - `headers` `dict[str, str] | None` (default: `None`)
        - Optional headers to use over global headers
    - Returns:
      - `Response`
  - `post(...)`
    - POST method with Response model returned
    - NOTE: Only json or fields can be provided, not both.
    - Args:
      - `url` : `str`
        - HTTPS URL of target
    - Keyword Args:
      - `json` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of payload to be delivered
      - `fields` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of fields to be translated to urlecoded string
      - `headers` `dict[str, str] | None` (default: `None`)
        - Optional headers to use over global headers
    - Returns:
      - `Response`
  - `put(...)`
    - PUT method with Response model returned
    - NOTE: Only json or fields can be provided, not both.
    - Args:
      - `url` : `str`
        - HTTPS URL of target
    - Keyword Args:
      - `json` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of payload to be delivered
      - `fields` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of fields to be translated to urlecoded string
      - `headers` `dict[str, str] | None` (default: `None`)
        - Optional headers to use over global headers
    - Returns:
      - `Response`
  - `patch(...)`
    - PATCH method with Response model returned
    - NOTE: Only json or fields can be provided, not both.
    - Args:
      - `url` : `str`
        - HTTPS URL of target
    - Keyword Args:
      - `json` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of payload to be delivered
      - `fields` : `dict[str, Any] | None` (default: `None`)
        - {key:value} dict of fields to be translated to urlecoded string
      - `headers` `dict[str, str] | None` (default: `None`)
        - Optional headers to use over global headers
    - Returns:
      - `Response`


## `Response` Object

All `HTTPResponses` are wrapped in a custom model that provides quick access to
data.

**Attributes**

- `http_response` : `urllib3.response.HTTPResponse`
  - The original `HTTPResponse` object as returned by `urllib3`

**Properties**

- `status_code` : `int`
  - Status code of response
- `text` : `str`
  - UTF-8 decoded response body
- `headers: `dict[str, Any]`
  - Response headers

**Methods**

- `has_success` : `bool`
  - Boolean mark of a response code of 200 to 299
- `json` : `dict[str, Any] | None`
  - JSON decoded dict of response body


## `ClientMocker` Object

Used to patch the `HTTPClient` in unit tests. Add responses which are returned
when CRUD methods are called. Suggested to use `unittest.mock.patch.object` to
patch use of `HTTPClient` in tests.

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

---

## Local developer installation

It is **strongly** recommended to use a virtual environment
([`venv`](https://docs.python.org/3/library/venv.html)) when working with python
projects. Leveraging a `venv` will ensure the installed dependency files will
not impact other python projects or any system dependencies.

The following steps outline how to install this repo for local development. See
the [CONTRIBUTING.md](../CONTRIBUTING.md) file in the repo root for information
on contributing to the repo.

**Windows users**: Depending on your python install you will use `py` in place
of `python` to create the `venv`.

**Linux/Mac users**: Replace `python`, if needed, with the appropriate call to
the desired version while creating the `venv`. (e.g. `python3` or `python3.8`)

**All users**: Once inside an active `venv` all systems should allow the use of
`python` for command line instructions. This will ensure you are using the
`venv`'s python and not the system level python.

---

## Installation steps

Clone this repo and enter root directory of repo:

```bash
git clone https://github.com/Preocts/http_overeasy
cd http_overeasy
```

Create the `venv`:

```console
$ python -m venv venv
```

Activate the `venv`:

```console
# Linux/Mac
$ . venv/bin/activate

# Windows
$ venv\Scripts\activate
```

The command prompt should now have a `(venv)` prefix on it. `python` will now
call the version of the interpreter used to create the `venv`

Install editable library and development requirements:

```console
# Update pip and tools
$ python -m pip install --upgrade pip

# Install editable version of library
$ python -m pip install --editable .[dev]
```

Install pre-commit [(see below for details)](#pre-commit):

```console
$ pre-commit install
```

---

## Misc Steps

Run pre-commit on all files:

```console
$ pre-commit run --all-files
```

Run tests:

```console
$ tox [-r] [-e py3x]
```

Build dist:

```console
$ python -m pip install --upgrade build

$ python -m build
```

To deactivate (exit) the `venv`:

```console
$ deactivate
```
---

## Note on flake8:

`flake8` is included in the `requirements-dev.txt` of the project. However it
disagrees with `black`, the formatter of choice, on max-line-length and two
general linting errors. `.pre-commit-config.yaml` is already configured to
ignore these. `flake8` doesn't support `pyproject.toml` so be sure to add the
following to the editor of choice as needed.

```ini
--ignore=W503,E203
--max-line-length=88
```

---

## [pre-commit](https://pre-commit.com)

> A framework for managing and maintaining multi-language pre-commit hooks.

This repo is setup with a `.pre-commit-config.yaml` with the expectation that
any code submitted for review already passes all selected pre-commit checks.
`pre-commit` is installed with the development requirements and runs seemlessly
with `git` hooks.

---

## Makefile

This repo has a Makefile with some quality of life scripts if the system
supports `make`.  Please note there are no checks for an active `venv` in the
Makefile.

| PHONY             | Description                                                           |
| ----------------- | --------------------------------------------------------------------- |
| `init`            | Update pip to newest version                                          |
| `install`         | install the project                                                   |
| `install-test`    | install test requirements and project as editable install             |
| `install-dev`     | install development/test requirements and project as editable install |
| `build-dist`      | Build source distribution and wheel distribution                      |
| `clean-artifacts` | Deletes python/mypy artifacts, cache, and pyc files                   |
| `clean-tests`     | Deletes tox, coverage, and pytest artifacts                           |
| `clean-build`     | Deletes build artifacts                                               |
| `clean-all`       | Runs all clean scripts                                                |
