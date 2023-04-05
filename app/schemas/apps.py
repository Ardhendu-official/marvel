from datetime import date, datetime, time
from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel


class Appps(BaseModel):
    get_version_code : Optional[str] = None
    get_version_datelis : Optional[str] = None
    app_created_timestamp : Optional[date] = None