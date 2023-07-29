# MyFigureCollection Scraper

Asyncronous scraping library for MyFigureCollection (MFC).

Still a work in progress, but the basic functionality is there.


## Usage

```python
import asyncio
from mfc import MfcClient

async def main():
    client = MfcClient()
    profile = await client.get_profile("syntack")
    print(profile.status)

if __name__ == "__main__":
    asyncio.run(main())
```

### Authenticated Requests

There is some session support but as of right now the goal is to focus on non-authenticated requests.