"""Fetch data from https://gpc-browser.gs1.org/.
"""
from ._crawlers import (
    fetch_file,
    get_language,
    get_languages,
    get_publications,
    parse_json_file,
)
from ._schemas import Language, Publication, Categories, Category

__version__ = '1.0.0'
__all__ = [
    'Categories',
    'Category',
    'fetch_file',
    'get_language',
    'get_languages',
    'get_publications',
    'Language',
    'parse_json_file',
    'Publication',
]
