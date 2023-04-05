import datetime
from datetime import datetime

from sqlalchemy import (BOOLEAN, Column, Date, DateTime, Float, Integer,
                        String, Text, Time, true)

from app.config.database import Base


class DbAppVersion(Base):
    __tablename__ = 'apps_version'
    app_id = Column(Integer, primary_key=True, autoincrement=True)  
    get_version_code = Column(String(255))
    get_version_datelis = Column(Text(4294000000))
    app_created_timestamp = Column(Date)