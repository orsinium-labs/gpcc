from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Language:
    countryCode: str                    # "HR"
    culture: str                        # "hr-HR"
    freeToDownload: bool                # true
    includeAttributeAndValues: bool     # false
    isActive: bool                      # true
    languageCode: str                   # "HR"
    languageId: int                     # 30
    languageName: str                   # "Croatian"
    lastUpdate: str                     # "2022-12-15T09:55:48.1502322"
    moContactEmail: str                 # "dsegovic@gs1hr.org"
    rightToLeft: bool                   # false
    showInBrowser: bool                 # true
    usePublicationBlobs: bool           # false


@dataclass(frozen=True)
class Publication:
    publicationId: int                  # 130
    languageId: int                     # 1
    publicationName: str                # "GPC as of May 2023"
    browser: bool                       # true
    isGDSN: bool                        # false
    publicationArchiveId: object        # null
    releaseNoteAttachment: str          # "..."
    publicationDate: str                # "2023-06-05T10:47:31.4022363"
    insertDate: str                     # "2023-06-05T10:47:31.4022363"
    lastUpdate: str                     # "2023-06-05T10:47:36.1976419"
    userId: str                         # "317544aa-4656-eb11-a812-0022481e215a"
    userName: str | None                # null
    version: str                        # "v20230605"
