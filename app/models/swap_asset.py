import datetime
from datetime import datetime

from sqlalchemy import (BOOLEAN, Column, DateTime, Float, Integer, String,
                        Text, Time, true)

from app.config.database import Base


class DbSwapAsset(Base):
    __tablename__ = 'swap_asset'
    asset_id = Column(Integer, primary_key=True, autoincrement=True)  
    asset_network = Column(String(255))
    asset_symbol = Column(String(255))
    asset_image = Column(String(255))
    asset_name = Column(String(255))