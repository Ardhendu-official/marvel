import json
import random
import secrets
import time
import uuid
from datetime import datetime, timedelta
from typing import List

import pytz
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbBanner
from app.schemas.index import Banner


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_new_banner(request: Banner, db: Session = Depends(get_db)):       # type: ignore   
    new_banner = DbBanner(
        name = request.name,
        Subtitle = request.Subtitle,
        image = request.image,
        url = request.url,
        network = request.network
    )
    db.add(new_banner)
    db.commit()
    banner = db.query(DbBanner).filter(DbBanner.banner_id == new_banner.banner_id).first()
    return banner

def all_show_banner(db: Session = Depends(get_db)):
    banner = db.query(DbBanner).all()
    return banner[:6]

def banner_search(search: str, db: Session = Depends(get_db)):
    banner = db.query(DbBanner).filter(DbBanner.name.like(f"%{search}%", escape="/")).all()
    return banner

def show_banner(network: str, db: Session = Depends(get_db)):
    banner = db.query(DbBanner).filter(DbBanner.network == network).all()
    return banner