from datetime import datetime
from typing import List

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbToken
from app.oprations.index import (all_swap_trans, create_swap,
                                 create_swap_asset, show_swap_curency,
                                 show_swap_curency_all, show_swap_estimated,
                                 show_swap_list, show_swap_minimal,
                                 show_swap_pair, show_swap_range,
                                 show_swap_trans, show_swap_trx,
                                 show_swap_usdt)
from app.schemas.index import Exchange, SwapAsset

swap = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@swap.get('/swap/pair/{asset}', status_code=status.HTTP_200_OK)
def showSwappair(asset: str, db: Session = Depends(get_db)):
    return show_swap_pair(asset, db)

@swap.get('/swap/trx', status_code=status.HTTP_200_OK)
def showSwapTrx(db: Session = Depends(get_db)):
    return show_swap_trx(db)          # type: ignore

@swap.get('/swap/usdt', status_code=status.HTTP_200_OK)
def showSwapUsdt(db: Session = Depends(get_db)):
    return show_swap_usdt(db)          # type: ignore

@swap.get('/swap/curency/{asset}', status_code=status.HTTP_200_OK)
def showSwapcurency(asset: str, db: Session = Depends(get_db)):
    return show_swap_curency(asset, db)

@swap.get('/swap/curency/all', status_code=status.HTTP_200_OK)
def showSwapcurencyAll(db: Session = Depends(get_db)):
    return show_swap_curency_all(db)

@swap.get('/swap/estimated/{currency_from}/{currency_to}/{amount}', status_code=status.HTTP_200_OK)
def showSwapEstimated(currency_from: str, currency_to: str, amount:str, db: Session = Depends(get_db)):
    return show_swap_estimated(currency_from, currency_to, amount, db)

@swap.get('/swap/minimal/{currency_from}/{currency_to}/{amount}', status_code=status.HTTP_200_OK)
def showSwapMinimal(currency_from: str, currency_to: str ,amount:str, db: Session = Depends(get_db)):
    return show_swap_minimal(currency_from, currency_to, amount, db)

@swap.get('/swap/range/{currency_from}/{currency_to}', status_code=status.HTTP_200_OK)
def showSwapRange(currency_from: str, currency_to: str, db: Session = Depends(get_db)):
    return show_swap_range(currency_from, currency_to, db)

@swap.post('/swap/create', status_code=status.HTTP_200_OK)
def CreateSwap(request: Exchange, db: Session = Depends(get_db)):
    return create_swap(request, db)

@swap.get('/swap/trans/{user_hash_id}/{user_address}', status_code=status.HTTP_200_OK)
def showSwapTrans(user_hash_id: str, user_address: str, db: Session = Depends(get_db)):
    return show_swap_trans(user_hash_id, user_address, db)

@swap.get('/swap/all/trans', status_code=status.HTTP_200_OK)
def allSwapTrans(db: Session = Depends(get_db)):
    return all_swap_trans(db)

@swap.post('/swap/asset/create', status_code=status.HTTP_200_OK)
def CreateSwapAsset(request: SwapAsset, db: Session = Depends(get_db)):
    return create_swap_asset(request, db)

@swap.get('/swap/list', status_code=status.HTTP_200_OK)
def showSwapList(db: Session = Depends(get_db)):
    return show_swap_list(db)          # type: ignore