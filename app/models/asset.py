import datetime
from datetime import datetime

from sqlalchemy import (BOOLEAN, Column, DateTime, Float, Integer, String,
                        Text, Time, true)

from app.config.database import Base


class DbAsset(Base):
    __tablename__ = 'asset'
    asset_id = Column(Integer, primary_key=True, autoincrement=True)  
    asset_name = Column(String(255))
    asset_abbr = Column(String(255))
