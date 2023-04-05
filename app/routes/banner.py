from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbToken
from app.oprations.index import (all_show_banner, banner_search,
                                 create_new_banner, show_banner)
from app.schemas.index import Assets, Banner

banner = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@banner.post('/banner/add', status_code=status.HTTP_201_CREATED)
def createBanner(request: Banner, db: Session = Depends(get_db)):
    return create_new_banner(request,db)  # type: ignore

@banner.get('/banner/show', status_code=status.HTTP_200_OK)
def AllshowBanner(db: Session = Depends(get_db)):
    return all_show_banner(db)  

@banner.get('/banner/search/{search}', status_code=status.HTTP_200_OK)
def searchBanner(search: str, db: Session = Depends(get_db)):
    return banner_search(search, db)  

@banner.get('/banner/show/{network}', status_code=status.HTTP_200_OK)
def showBanner(network: str, db: Session = Depends(get_db)):
    return show_banner(network, db)  