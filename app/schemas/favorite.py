from datetime import datetime, time
from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel


class Favorite(BaseModel):
    user_hash_id: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None