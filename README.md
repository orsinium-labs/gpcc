# gpc

Python library and CLI tool to fetch information from [GCP Browser](https://gpc-browser.gs1.org/).

This is a standardized classifier of products used across companies. The classification, however, cannot be inferred from the product barcode or even packaging. Companies use it only internally.

## Installation

```bash
python3 -m pip install gpc
```

## CLI usage

```bash
# download latest JSONs for all languages
python3 -m gpc

# download latest JSON for a specified language
python3 -m gpc --lang nl

# download into a specified directory
python3 -m gpc --output ./gpc-dump/
```

## Python usage

```python
import asyncio
import gpc
from pathlib import Path

async def run():
    langs = await gpc.get_languages()
    output = Path('gpc-dump')
    await gpc.fetch_files(output, langs)

asyncio.run(run())
```
