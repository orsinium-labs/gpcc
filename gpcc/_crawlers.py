"""
https://gpc-browser.gs1.org/
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import BinaryIO, Literal, TextIO

import aiohttp

from ._schemas import Categories, Category, Language, Publication


URL_LANGS = 'https://gpc-api.gs1.org/api/browser/language/all'
URL_PUBLICATIONS = 'https://gpc-api.gs1.org/api/browser/publication?languageId={lang}'
URL_FILE = 'https://gpc-api.gs1.org/api/blob/download/publication/{id}/{format}'
URL_FILE_2 = 'https://gpc-api.gs1.org/api/blob/dynamic/download/publication/{id}/{format}'
HEADERS = {'Referer': 'https://gpc-browser.gs1.org/'}


async def get_languages() -> list[Language]:
    """Fetch from the API list of info about all supported languages.
    """
    async with aiohttp.ClientSession() as session:
        resp = await session.get(URL_LANGS, headers=HEADERS)
        resp.raise_for_status()
        data = await resp.json()
    assert data['statusCode'] == 200
    assert data['isSuccess'] is True
    return [Language(**lang) for lang in data['result']]


async def get_language(language: str | int) -> Language | None:
    """Fetch from the API info about the given language.

    The language arg can be language name, code, id, or country code.
    """
    langs = await get_languages()

    if isinstance(language, int):
        for lang in langs:
            if lang.languageId == language:
                return lang
        return None

    language = language.lower()
    for lang in langs:
        if lang.countryCode.lower() == language:
            return lang
        if lang.culture.lower() == language:
            return lang
        if lang.languageCode.lower() == language:
            return lang
        if lang.languageName.lower() == language:
            return lang
    return None


async def get_publications(language: Language | int) -> list[Publication]:
    """Fetch from the API info about latest publications for the given language.
    """
    if isinstance(language, Language):
        language_id = language.languageId
    else:
        language_id = language
    url = URL_PUBLICATIONS.format(lang=language_id)
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url, headers=HEADERS)
        resp.raise_for_status()
        data = await resp.json()
    assert data['statusCode'] == 200
    assert data['isSuccess'] is True
    return [Publication(**lang) for lang in data['result']]


async def fetch_file(
    stream: BinaryIO,
    publication: Publication | int,
    format: Literal['json', 'xml', 'xlsx'] = 'json',
    chunk_size: int = 4 * 1024,
) -> None:
    """Fetch the publication file in the given format and write it into the stream.
    """
    if isinstance(publication, Publication):
        publication_id = publication.publicationId
    else:
        publication_id = publication
    url = URL_FILE.format(id=publication_id, format=format)
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url, headers=HEADERS)
        if resp.status == 404:
            url = URL_FILE_2.format(id=publication_id, format=format)
            resp = await session.get(url, headers=HEADERS)
        resp.raise_for_status()
        finished = False
        while not finished:
            chunk = await resp.content.read(chunk_size)
            stream.write(chunk)
            finished = not chunk


async def parse_json_file(stream: BinaryIO) -> Categories:
    """Given a steeam with a JSON file, parse it into Categories object.

    The JSON file can be fetched using `fetch_file`.
    """
    data = json.load(stream)
    return Categories(
        LanguageCode=data['LanguageCode'],
        DateUtc=data['DateUtc'],
        Schema=_parse_categories(data['Schema']),
    )


def _parse_categories(raw_cats: list[dict]) -> list[Category]:
    if not raw_cats:
        return []
    cats = []
    for raw_cat in raw_cats:
        raw_cat['Childs'] = _parse_categories(raw_cat['Childs'])
        cats.append(Category(**raw_cat))
    return cats


async def fetch_files(
    dir_path: Path,
    languages: list[Language],
    stdout: TextIO = sys.stdout,
) -> None:
    """Download the latest publication JSON file for every given language.

    The results will be saved in the given directory.
    """
    sem = asyncio.Semaphore(25)
    tasks = []
    dir_path.mkdir(exist_ok=True, parents=True)
    for lang in languages:
        tasks.append(_download(sem, dir_path, lang, stdout))
    await asyncio.gather(*tasks)


async def _download(
    sem: asyncio.Semaphore,
    dir_path: Path,
    lang: Language,
    stdout: TextIO,
) -> None:
    async with sem:
        publications = await get_publications(lang)
        publication = publications[0]
        path = dir_path / f'{lang.languageCode.lower()}-{publication.version}.json'
        with path.open('wb') as stream:
            print('⏳️ started: ', path.stem, file=stdout)
            try:
                for _ in range(40):
                    try:
                        await _fetch_with_retries(path, stdout, stream, publication)
                    except aiohttp.ClientResponseError:
                        continue
                    else:
                        break
            except Exception as exc:
                print('💥 failed:  ', path.stem, file=stdout)
                print('   ', exc)
            else:
                print('✅ finished:', path.stem, file=stdout)


async def _fetch_with_retries(path: Path, stdout: TextIO, *args) -> None:
    for _ in range(40):
        try:
            await fetch_file(*args)
        except aiohttp.ClientResponseError as exc:
            # if "too many attempts", sleep and try again
            if exc.status == 429:
                print('😴 paused:  ', path.stem, file=stdout)
                await asyncio.sleep(10)
                continue
            raise
        return
