from __future__ import annotations

import asyncio
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import NoReturn, TextIO

from ._crawlers import fetch_files, get_language, get_languages
from ._schemas import Language


async def main(argv: list[str], stdout: TextIO) -> int:
    parser = ArgumentParser()
    parser.add_argument('--lang')
    parser.add_argument('--output', type=Path, default=Path('gpc-dump'))
    args = parser.parse_args(argv)

    # collect languages
    langs: list[Language]
    if args.lang:
        lang_id: str | int
        if args.lang.isdigit():
            lang_id = int(args.lang)
        else:
            lang_id = args.lang
        lang = await get_language(lang_id)
        if lang is None:
            print('Unknown language', file=stdout)
            return 1
        langs = [lang]
    else:
        langs = await get_languages()

    # run tasks to download files
    await fetch_files(args.output, langs, stdout)
    return 0


def entrypoint() -> NoReturn:
    coro = main(argv=sys.argv[1:], stdout=sys.stdout)
    code = asyncio.run(coro)
    sys.exit(code)
