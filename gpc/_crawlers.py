"""
https://gpc-browser.gs1.org/
"""
from __future__ import annotations
from typing import BinaryIO, Literal
import aiohttp
from ._schemas import Language, Publication

URL_LANGS = 'https://gpc-api.gs1.org/api/browser/language/all'
URL_PUBLICATIONS = 'https://gpc-api.gs1.org/api/browser/publication?languageId={lang}'
URL_FILE = 'https://gpc-api.gs1.org/api/blob/download/publication/{id}/{format}'
HEADERS = {'Referer': 'https://gpc-browser.gs1.org/'}


async def get_languages() -> list[Language]:
    async with aiohttp.ClientSession() as session:
        resp = await session.get(URL_LANGS, headers=HEADERS)
        resp.raise_for_status()
        data = await resp.json()
    assert data['statusCode'] == 200
    assert data['isSuccess'] is True
    return [Language(**lang) for lang in data['result']]


async def get_language(language: str | int) -> Language | None:
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
    if isinstance(publication, Publication):
        publication_id = publication.publicationId
    else:
        publication_id = publication
    url = URL_FILE.format(id=publication_id, format=format)
    async with aiohttp.ClientSession() as session:
        resp = await session.get(url, headers=HEADERS)
        resp.raise_for_status()
        finished = False
        while not finished:
            chunk = await resp.content.read(chunk_size)
            stream.write(chunk)
            finished = not chunk
