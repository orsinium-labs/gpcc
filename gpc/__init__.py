"""Fetch data from https://gpc-browser.gs1.org/.
"""
from __future__ import annotations
from ._crawlers import get_languages, get_language, get_publications, fetch_file
from ._schemas import Language, Publication

__version__ = '1.0.0'
__all__ = [
    'fetch_file',
    'get_language',
    'get_languages',
    'get_publications',
    'Language',
    'Publication',
]
