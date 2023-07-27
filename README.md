# pygpc

Python library and CLI tool to fetch information from [GCP Browser](https://gpc-browser.gs1.org/).

This is a standardized classifier of products used across companies. The classification, however, cannot be inferred from the product barcode or even packaging. Companies use it only internally.

## Installation

```bash
python3 -m pip install pygpc
```

## CLI usage

```bash
# download latest JSONs for all languages
python3 -m pygpc

# download latest JSON for a specified language
python3 -m pygpc --lang nl

# download into a specified directory
python3 -m pygpc --output ./gpc-dump/
```

## Python usage

```python
import asyncio
import pygpc
from pathlib import Path

async def run():
    langs = await pygpc.get_languages()
    output = Path('gpc-dump')
    await pygpc.fetch_files(output, langs)

asyncio.run(run())
```
