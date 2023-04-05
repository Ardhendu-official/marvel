from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.oprations.index import create_app_version, show_app, show_app_version
from app.schemas.index import Appps

apps = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@apps.get('/app/details', status_code=status.HTTP_200_OK)
def showBanner(db: Session = Depends(get_db)):
    return show_app(db)  

@apps.get('/app/version/details', status_code=status.HTTP_200_OK)
def showversion(db: Session = Depends(get_db)):
    return show_app_version(db)

@apps.post('/app/version/create', status_code=status.HTTP_200_OK)
def createversion(request: Appps, db: Session = Depends(get_db)):
    return create_app_version(request, db)