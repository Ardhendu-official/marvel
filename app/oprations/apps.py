from datetime import datetime, timedelta

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbApps, DbAppVersion
from app.schemas.index import Appps

app = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def show_app(db: Session = Depends(get_db)):
    app_del = db.query(DbApps).order_by(DbApps.app_id.desc()).first()
    return app_del

def show_app_version(db: Session = Depends(get_db)):
    app_del = db.query(DbAppVersion).order_by(DbAppVersion.app_id.desc()).all()
    dll = []
    for dat in app_del:         # type: ignore  
        data = dat.get_version_datelis.split(",")
        # dll.append(dat)
        # date = dat.app_created_timestamp.strftime("%Y-%m-%d")
        dtt ={
            "get_version_datelis": data,
            "get_version_code": dat.get_version_code,
            "app_created_timestamp": dat.app_created_timestamp.strftime("%d-%m-%Y")
        }
        dll.append(dtt)

    return dll

def create_app_version(request: Appps, db: Session = Depends(get_db)):       # type: ignore   
    new_version = DbAppVersion(
        get_version_code = request.get_version_code,
        get_version_datelis = request.get_version_datelis,
        app_created_timestamp = request.app_created_timestamp
    )
    db.add(new_version)
    db.commit()
    banner = db.query(DbAppVersion).filter(DbAppVersion.app_id == new_version.app_id).first()
    return banner