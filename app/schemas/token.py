from datetime import datetime, time
from typing import Optional

from fastapi import File, UploadFile
from pydantic import BaseModel


class Assets(BaseModel):
    token_contect_id: str
    address: Optional[str] = None

class AssetsAdd(BaseModel):
    token_name : str
    token_short_name : str
    token_contect_id : str
    token_logo : str
    token_decimal : int
    token_network : str
    token_type : str

class AssetsNetwork(BaseModel):
    token_contect_id: str
    address: Optional[str] = None
    network: Optional[str] = None
