# Tenji

[![PyPI](https://img.shields.io/pypi/v/tenji.svg)](https://pypi.org/project/tenji/)
[![Python versions](https://img.shields.io/pypi/pyversions/tenji.svg)](https://pypi.org/project/tenji/)
[![License](https://img.shields.io/pypi/l/tenji.svg)](https://github.com/Tenji-hin/tenji/blob/master/LICENSE)

Asynchronous Python client for scraping data from MyFigureCollection (MFC).

## Installation

```sh
pip install tenji
```

## Usage

The client holds an HTTP session, so use it as an async context manager (or call
`await client.close()` when you are done with it).

```python
import asyncio
from tenji import MfcClient

async def main():
    async with MfcClient() as client:
        profile = await client.get_profile("syntack")
        print(profile.status)

if __name__ == "__main__":
    asyncio.run(main())
```

Every model and enum you need is importable from the top-level package:

```python
from tenji import CollectionStatus, ItemCategory, MfcClient

async def main():
    async with MfcClient() as client:
        collection = await client.get_collection("syntack", CollectionStatus.Owned)
        for item in collection.items:
            if item.category is ItemCategory.Prepainted:
                print(item.id, item.name)
```

### Errors

Requests that do not return `200` raise `RequestException`; pages that cannot be
scraped raise `ParserException`. Both are importable from `tenji`.

### Authenticated Requests

The focus is on non-authenticated requests, but signing in is supported. Reuse
the returned `PHPSESSID` cookie to skip the login round trip next time:

```python
from tenji import MfcClient

async def main():
    async with MfcClient() as client:
        success, cookies = await client.login("username", "password")
        if success:
            session_id = cookies["PHPSESSID"].value

    # later, restore the session without logging in again
    async with MfcClient(session_id=session_id) as client:
        logged_in, username = await client.is_logged_in()
```

### Notes

* The client currently relies on an English locale.
* MFC has no public API, so this library scrapes HTML. Markup changes upstream
  can break parsing between releases.

## Development

```sh
pip install -e ".[test]"
pytest
```
