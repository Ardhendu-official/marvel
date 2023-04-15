import json
import random
import string
import time
import uuid
from datetime import datetime
from typing import List, Optional

import pytz
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.functions.index import Hash, HashVerify
from app.models.index import (DbAdmin, DbAsset, DbFeesTransaction,
                              DbRefTransaction, DbToken, DbTrxTransaction,
                              DbUser)
from app.schemas.index import (ImportWallet, ImportWalletAll, User, UserNew,
                               WalletDetails, WalletDetailsAll, deleteWallet,
                               liveprice, passChange, passVarify, sendAirdrop,
                               sendAll, sendTokenAll, sendTron, updateWallet,
                               updateWalletAll)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_new_wallet(request: User, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
    url= "http://13.235.171.121:2352/api/v1/tron/account"
    response = requests.post(url)
    wallet_details = response.json()
    hash_id = 'AL'+uuid.uuid1().hex[:8]
    if user:
        new_user = DbUser(
            user_hash_id= request.user_hash_id,
            user_wallet_name = request.user_wallet_name,
            user_password = Hash.bcrypt(request.user_password),  # type: ignore
            user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
            user_privateKey = wallet_details["account"]["privateKey"], 
            user_mnemonic_key = wallet_details["phase"],               
            user_address = wallet_details["account"]["address"],       
            user_show = "true"
        )
        db.add(new_user)
        db.commit()
        details = db.query(DbUser).filter(DbUser.user_hash_id == new_user.user_hash_id).all()
    else:
        user = DbUser(
            user_hash_id= hash_id,
            user_wallet_name = request.user_wallet_name,
            user_password = Hash.bcrypt(request.user_password),  # type: ignore
            user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
            user_privateKey = wallet_details["account"]["privateKey"],   
            user_mnemonic_key = wallet_details["phase"],                  
            user_address = wallet_details["account"]["address"],         
            user_show = "true"
        )
        db.add(user)
        db.commit()
        details = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).all()
    return details

def create_wallet(request: UserNew, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
    # if request.user_network =='trx' or request.user_network =='eth' or request.user_network =='bnb' or request.user_network =='polygon' or request.user_network =='solana':
    if request.user_network =='trx' or request.user_network =='bnb':
        wallet_details = number_of_network_create(request.user_network)
    else:
        return {"msg": "something worng"}
    hash_id = 'MW'+uuid.uuid1().hex[:8]
    referral_code = generate_unique_number()
    if user:
        if request.user_network =='bnb':
            new_user = DbUser(
                user_hash_id= request.user_hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                user_privateKey = wallet_details["account"]["privateKey"],  # type: ignore
                user_mnemonic_key = wallet_details["phase"],               # type: ignore
                user_address = wallet_details["account"]["address"],       # type: ignore
                user_show = "true",
                user_network = wallet_details["network"],               # type: ignore
                user_referral_code = user.user_referral_code,          
                get_referral_id = request.get_referral_id
            )
            db.add(new_user)
            db.commit()
            details = db.query(DbUser).filter(DbUser.user_hash_id == new_user.user_hash_id).order_by(DbUser.user_id.desc()).first()
        else:
            new_user = DbUser(
                user_hash_id= request.user_hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                user_privateKey = wallet_details["account"]["privateKey"],  # type: ignore
                user_mnemonic_key = wallet_details["phase"],               # type: ignore
                user_address = wallet_details["account"]["address"],       # type: ignore
                user_show = "true",
                user_network = wallet_details["network"],               # type: ignore
                user_referral_code = user.user_referral_code,      
                get_referral_id = request.get_referral_id
            )
            db.add(new_user)
            db.commit()
            details = db.query(DbUser).filter(DbUser.user_hash_id == new_user.user_hash_id).order_by(DbUser.user_id.desc()).first()
    else:
        if request.user_network =='bnb':
            user = DbUser(
                user_hash_id= hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                user_privateKey = wallet_details["account"]["privateKey"],    # type: ignore
                user_mnemonic_key = wallet_details["phase"],                  # type: ignore
                user_address = wallet_details["account"]["address"],         # type: ignore
                user_show = "true",
                user_network = wallet_details["network"],               # type: ignore
                user_referral_code = referral_code,
                get_referral_id = request.get_referral_id
            )
            db.add(user)
            db.commit()
            details = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).order_by(DbUser.user_id.desc()).first()
        else:
            user = DbUser(
                user_hash_id= hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                user_privateKey = wallet_details["account"]["privateKey"],    # type: ignore
                user_mnemonic_key = wallet_details["phase"],                  # type: ignore
                user_address = wallet_details["account"]["address"],         # type: ignore
                user_show = "true",
                user_network = wallet_details["network"],               # type: ignore
                user_referral_code = referral_code,

            )
            db.add(user)
            db.commit()
            details = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).order_by(DbUser.user_id.desc()).first()
    return details

def import_wallet(request: ImportWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).all()
    mnemonic_key = ismnemonickey(request.m_key_or_p_key) 
    if mnemonic_key["status"] == True:
        url= "http://13.235.171.121:2352/api/v1/tron/wallet/import/phase"
        body = {"phase": request.m_key_or_p_key}
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
    else:
        url= "http://13.235.171.121:2352/api/v1/tron/wallet/import/private"
        body = {"pkey": request.m_key_or_p_key}
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
    for u_detalis in user:
        if u_detalis.user_address == wallet_details["address"]:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"address already added") 
        else:
            if mnemonic_key["status"] == True:
                url= "http://13.235.171.121:2352/api/v1/tron/wallet/import/phase"
                body = {"phase": request.m_key_or_p_key}
                headers = {'Content-type': 'application/json'}
                response = requests.post(url,json=body,headers=headers)
                wallet_details = response.json()
            else:
                url= "http://13.235.171.121:2352/api/v1/tron/wallet/import/private"
                body = {"pkey": request.m_key_or_p_key}
                headers = {'Content-type': 'application/json'}
                response = requests.post(url,json=body,headers=headers)
                wallet_details = response.json()
    hash_id = 'AL'+uuid.uuid1().hex[:8]
    if user:
        if wallet_details:    # type: ignore
            user = DbUser(
                user_hash_id=request.user_hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),  # type: ignore
                user_privateKey = wallet_details["privateKey"],
                user_mnemonic_key = request.m_key_or_p_key,
                user_address =  wallet_details["address"],
                user_show = "true",
                user_network = "tron"
            )
            db.add(user)
            db.commit()
            details_add = user = db.query(DbUser).filter(DbUser.user_id == user.user_id).first()  # type: ignore
    else:
        new_user = DbUser(
            user_hash_id=hash_id,
            user_wallet_name = request.user_wallet_name,
            user_password = Hash.bcrypt(request.user_password),  # type: ignore
            user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
            user_privateKey = wallet_details["privateKey"],   # type: ignore
            user_mnemonic_key = request.m_key_or_p_key, 
            user_address = wallet_details["address"],   # type: ignore
            user_show = "true",
            user_network = "tron"
        )
        db.add(new_user)
        db.commit()
        details_add = user = db.query(DbUser).filter(DbUser.user_id == new_user.user_id).first()
    return details_add                    # type: ignore
    
def import_eth_wallet(request: ImportWalletAll, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).all()
    if request.user_network == "eth":
        mnemonic_key = request.m_key_or_p_key.split()
        # return mnemonic_key
        if mnemonic_key.__len__() == 12:
            url= "http://13.235.171.121:2352/api/v1/eth/wallet/import/phase"
            body = {"mkey": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        else:
            url= "http://13.235.171.121:2352/api/v1/eth/wallet/import/private"
            body = {"pkey": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        for u_detalis in user:
            if u_detalis.user_address == wallet_details["address"] and u_detalis.user_network == "eth":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"address already added") 
            else:
                if mnemonic_key.__len__() == 12:
                    url= "http://13.235.171.121:2352/api/v1/eth/wallet/import/phase"
                    body = {"mkey": request.m_key_or_p_key}
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url,json=body,headers=headers)
                    wallet_details = response.json()
                else:
                    url= "http://13.235.171.121:2352/api/v1/eth/wallet/import/private"
                    body = {"pkey": request.m_key_or_p_key}
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url,json=body,headers=headers)
                    wallet_details = response.json()
        hash_id = 'AL'+uuid.uuid1().hex[:8]
        if user:
            if wallet_details:    # type: ignore
                user = DbUser(
                    user_hash_id=request.user_hash_id,
                    user_wallet_name = request.user_wallet_name,
                    user_password = Hash.bcrypt(request.user_password),  # type: ignore
                    user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),  # type: ignore
                    user_privateKey = wallet_details["privateKey"],
                    user_mnemonic_key = request.m_key_or_p_key,
                    user_address =  wallet_details["address"],
                    user_show = "true",
                    user_network = "eth"
                )
                db.add(user)
                db.commit()
                details_add = user = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).order_by(DbUser.user_id.desc()).first()  # type: ignore
        else:
            new_user = DbUser(
                user_hash_id=hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                user_privateKey = wallet_details["privateKey"],   # type: ignore
                user_mnemonic_key = request.m_key_or_p_key, 
                user_address = wallet_details["address"],   # type: ignore
                user_show = "true",
                user_network = "eth"
            )
            db.add(new_user)
            db.commit()
            details_add = user = db.query(DbUser).filter(DbUser.user_hash_id == new_user.user_hash_id).order_by(DbUser.user_id.desc()).first()
        return details_add                    # type: ignore
    if request.user_network == "bnb":
        mnemonic_key = request.m_key_or_p_key.split()
        # return mnemonic_key
        if mnemonic_key.__len__() == 12:
            url= "http://13.235.171.121:2352/api/v1/bnb/wallet/import/phase"
            body = {"mkey": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        else:
            url= "http://13.235.171.121:2352/api/v1/bnb/wallet/import/private"
            body = {"pkey": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        for u_detalis in user:
            if u_detalis.user_address == wallet_details["address"] and u_detalis.user_network == "bnb":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"address already added") 
            else:
                if mnemonic_key.__len__() == 12:
                    url= "http://13.235.171.121:2352/api/v1/bnb/wallet/import/phase"
                    body = {"mkey": request.m_key_or_p_key}
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url,json=body,headers=headers)
                    wallet_details = response.json()
                else:
                    url= "http://13.235.171.121:2352/api/v1/bnb/wallet/import/private"
                    body = {"pkey": request.m_key_or_p_key}
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url,json=body,headers=headers)
                    wallet_details = response.json()
        hash_id = 'MW'+uuid.uuid1().hex[:8]
        if user:
            if wallet_details:    # type: ignore
                user = DbUser(
                    user_hash_id=request.user_hash_id,
                    user_wallet_name = request.user_wallet_name,
                    user_password = Hash.bcrypt(request.user_password),  # type: ignore
                    user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),  # type: ignore
                    user_privateKey = wallet_details["privateKey"],
                    user_mnemonic_key = request.m_key_or_p_key,
                    user_address =  wallet_details["address"],
                    user_show = "true",
                    user_network = "bnb"
                )
                db.add(user)
                db.commit()
                details_add = user = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).order_by(DbUser.user_id.desc()).first()  # type: ignore
        else:
            new_user = DbUser(
                user_hash_id=hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                user_privateKey = wallet_details["privateKey"],   # type: ignore
                user_mnemonic_key = request.m_key_or_p_key, 
                user_address = wallet_details["address"],   # type: ignore
                user_show = "true",
                user_network = "bnb"
            )
            db.add(new_user)
            db.commit()
            details_add = user = db.query(DbUser).filter(DbUser.user_hash_id == new_user.user_hash_id).order_by(DbUser.user_id.desc()).first()
        return details_add                    # type: ignore
    elif request.user_network == "polygon":
        mnemonic_key = request.m_key_or_p_key.split()
        # return mnemonic_key
        if mnemonic_key.__len__() == 12:
            url= "http://13.235.171.121:2352/api/v1/polygon/wallet/import/phase"
            body = {"mkey": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        else:
            url= "http://13.235.171.121:2352/api/v1/polygon/wallet/import/private"
            body = {"pkey": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        for u_detalis in user:
            if u_detalis.user_address == wallet_details["address"] and u_detalis.user_network == "bnb":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"address already added") 
            else:
                if mnemonic_key.__len__() == 12:
                    url= "http://13.235.171.121:2352/api/v1/polygon/wallet/import/phase"
                    body = {"mkey": request.m_key_or_p_key}
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url,json=body,headers=headers)
                    wallet_details = response.json()
                else:
                    url= "http://13.235.171.121:2352/api/v1/polygon/wallet/import/private"
                    body = {"pkey": request.m_key_or_p_key}
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url,json=body,headers=headers)
                    wallet_details = response.json()
        hash_id = 'AL'+uuid.uuid1().hex[:8]
        if user:
            if wallet_details:    # type: ignore
                user = DbUser(
                    user_hash_id=request.user_hash_id,
                    user_wallet_name = request.user_wallet_name,
                    user_password = Hash.bcrypt(request.user_password),  # type: ignore
                    user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),  # type: ignore
                    user_privateKey = wallet_details["privateKey"],
                    user_mnemonic_key = request.m_key_or_p_key,
                    user_address =  wallet_details["address"],
                    user_show = "true",
                    user_network = "polygon"
                )
                db.add(user)
                db.commit()
                details_add = user = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).order_by(DbUser.user_id.desc()).first()  # type: ignore
        else:
            new_user = DbUser(
                user_hash_id=hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                user_privateKey = wallet_details["privateKey"],   # type: ignore
                user_mnemonic_key = request.m_key_or_p_key, 
                user_address = wallet_details["address"],   # type: ignore
                user_show = "true",
                user_network = "polygon"
            )
            db.add(new_user)
            db.commit()
            details_add = user = db.query(DbUser).filter(DbUser.user_hash_id == new_user.user_hash_id).order_by(DbUser.user_id.desc()).first()
        return details_add                    # type: ignore
    elif request.user_network == "solana":
        mnemonic_key = request.m_key_or_p_key.split()
        # return mnemonic_key
        if mnemonic_key.__len__() == 12:
            url= "http://13.235.171.121:2352/api/v1/solana/wallet/import/phase"
            body = {"mkey": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        else:
            url= "http://13.235.171.121:2352/api/v1/solana/wallet/import/private"
            body = {"pkey": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        for u_detalis in user:
            if u_detalis.user_address == wallet_details["address"] and u_detalis.user_network == "bnb":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"address already added") 
            else:
                if mnemonic_key.__len__() == 12:
                    url= "http://13.235.171.121:2352/api/v1/solana/wallet/import/phase"
                    body = {"mkey": request.m_key_or_p_key}
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url,json=body,headers=headers)
                    wallet_details = response.json()
                else:
                    url= "http://13.235.171.121:2352/api/v1/solana/wallet/import/private"
                    body = {"pkey": request.m_key_or_p_key}
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url,json=body,headers=headers)
                    wallet_details = response.json()
        hash_id = 'AL'+uuid.uuid1().hex[:8]
        if user:
            if wallet_details:    # type: ignore
                user = DbUser(
                    user_hash_id=request.user_hash_id,
                    user_wallet_name = request.user_wallet_name,
                    user_password = Hash.bcrypt(request.user_password),  # type: ignore
                    user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),  # type: ignore
                    user_privateKey = wallet_details["privateKey"],
                    user_mnemonic_key = request.m_key_or_p_key,
                    user_address =  wallet_details["address"],
                    user_show = "true",
                    user_network = "solana"
                )
                db.add(user)
                db.commit()
                details_add = user = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).order_by(DbUser.user_id.desc()).first()  # type: ignore
        else:
            new_user = DbUser(
                user_hash_id=hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                user_privateKey = wallet_details["privateKey"],   # type: ignore
                user_mnemonic_key = request.m_key_or_p_key, 
                user_address = wallet_details["address"],   # type: ignore
                user_show = "true",
                user_network = "solana"
            )
            db.add(new_user)
            db.commit()
            details_add = user = db.query(DbUser).filter(DbUser.user_hash_id == new_user.user_hash_id).order_by(DbUser.user_id.desc()).first()
        return details_add                    # type: ignore
    elif request.user_network == "trx":
        mnemonic_key = ismnemonickey(request.m_key_or_p_key) 
        if mnemonic_key["status"] == True:
            url= "http://13.235.171.121:2352/api/v1/tron/wallet/import/phase"
            body = {"phase": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        else:
            url= "http://13.235.171.121:2352/api/v1/tron/wallet/import/private"
            body = {"pkey": request.m_key_or_p_key}
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
        for u_detalis in user:
            if u_detalis.user_address == wallet_details["address"] and u_detalis.user_network == "trx":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"address already added") 
            else:
                if mnemonic_key["status"] == True:
                    url= "http://13.235.171.121:2352/api/v1/tron/wallet/import/phase"
                    body = {"phase": request.m_key_or_p_key}
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url,json=body,headers=headers)
                    wallet_details = response.json()
                else:
                    url= "http://13.235.171.121:2352/api/v1/tron/wallet/import/private"
                    body = {"pkey": request.m_key_or_p_key}
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url,json=body,headers=headers)
                    wallet_details = response.json()
        hash_id = 'MW'+uuid.uuid1().hex[:8]
        if user:
            if wallet_details:    # type: ignore
                user = DbUser(
                    user_hash_id=request.user_hash_id,
                    user_wallet_name = request.user_wallet_name,
                    user_password = Hash.bcrypt(request.user_password),  # type: ignore
                    user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),  # type: ignore
                    user_privateKey = wallet_details["privateKey"],
                    user_mnemonic_key = request.m_key_or_p_key,
                    user_address =  wallet_details["address"],
                    user_show = "true",
                    user_network = "trx", 
                    user_referral_code = user.user_referral_code,                       # type: ignore
                )
                db.add(user)
                db.commit()
                details_add = user = db.query(DbUser).filter(DbUser.user_hash_id == user.user_hash_id).order_by(DbUser.user_id.desc()).first()  # type: ignore
        else:
            referral_code = generate_unique_number()
            new_user = DbUser(
                user_hash_id=hash_id,
                user_wallet_name = request.user_wallet_name,
                user_password = Hash.bcrypt(request.user_password),  # type: ignore
                user_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
                user_privateKey = wallet_details["privateKey"],   # type: ignore
                user_mnemonic_key = request.m_key_or_p_key, 
                user_address = wallet_details["address"],   # type: ignore
                user_show = "true",
                user_network = "trx",
                user_referral_code = referral_code,          
                get_referral_id = request.get_referral_id
            )
            db.add(new_user)
            db.commit()
            details_add = user = db.query(DbUser).filter(DbUser.user_hash_id == new_user.user_hash_id).order_by(DbUser.user_id.desc()).first()
        return details_add                    # type: ignore
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"worng user network")

def details_wallet(request: WalletDetails, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
    url= "http://13.235.171.121:2352/api/v1/tron/wallet/details"
    body = {"address": request.user_address}           # type: ignore
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    data = []
    for value in wallet_details['tokens']:
        token_id = value['tokenAbbr']
        token = token_id.upper()
        if token == "AEL":
            price_details = {
                "asset_id_base": "AEL",
                "asset_id_quote": "USD",
                "rate": 2.00
            }
        else:
            apikey="3968BDD4-E8D6-4FC0-BE69-8E9D06C558A1"
            url_price= "https://rest.coinapi.io/v1/exchangerate/"+token+"/USD?apikey="+apikey
            res = requests.get(url_price)
            price_details = res.json()
            if 'rate' in price_details:
                price_details = {
                    "time": price_details['time'],
                    "asset_id_base": token,
                    "asset_id_quote": "USD",
                    "rate": price_details['rate']
                }
            else:
                price_details = {
                    "time": "2022-12-05T17:18:56.0000000Z",
                    "asset_id_base": token,
                    "asset_id_quote": "USD",
                    "rate": 1
                }
        data.append(price_details)
    return [wallet_details, data]

def details_wallet_bal(request: ImportWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_hash_id == request.user_hash_id).first()
    url= "http://13.235.171.121:2352/api/v1/tron/wallet/balance"
    body = {"address": request.user_address}           # type: ignore
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    data = []
    for amount in wallet_details['details']:                   
        bal = int(amount['balance']) / 10** amount['tokenDecimal']
        value = {
            "address": request.user_address,            # type: ignore
            "token": amount['tokenAbbr'],
            "token_amount": bal                               
        }
        data.append(value)
    return data

def show_user_wallet(hash_id: str , db: Session = Depends(get_db)):
    # user = db.query(DbUser).filter(DbUser.user_hash_id == hash_id).all()
    user = db.query(DbUser).filter(and_(DbUser.user_hash_id == hash_id, DbUser.user_show == "true")).all()
    data = []
    if user:
        for u_detalis in user:
            url= "http://13.235.171.121:2352/api/v1/tron/wallet/details"
            body = {"address": u_detalis.user_address}           # type: ignore
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
            balance = wallet_details["balance"] + wallet_details["totalFrozen"]
            dtl = {
                "user_privateKey": u_detalis.user_privateKey,
                "user_mnemonic_key": u_detalis.user_mnemonic_key,
                "user_wallet_name": u_detalis.user_wallet_name,
                "user_hash_id": u_detalis.user_hash_id,
                "user_address": u_detalis.user_address,
                "user_registration_date_time": u_detalis.user_registration_date_time,
                "token_balance": balance/1000000, 
                "user_show": u_detalis.user_show
            }
            data.append(dtl)
        return data
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user not found")

def send_trx(request: sendTron, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.from_account, DbUser.user_hash_id == request.user_hash_id)).first()
    if user and request.amount >= 10000:
        url= 'http://13.235.171.121:2352/api/v1/tron/wallet/send'
        body = {"from_account": request.from_account,
                "to_account": request.to_account,
                "amount": request.amount,
                "privateKey": user.user_privateKey                    # type: ignore
            }
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
        amount = wallet_details['transaction']['raw_data']['contract'][0]['parameter']['value']['amount']
        new_trans = DbTrxTransaction(
                transaction_tx_id = wallet_details['txid'],
                transaction_amount = amount/1000000,
                trans_from_account = request.from_account,
                trans_to_account = request.to_account,
                trans_user_id = request.user_hash_id,
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta')),
            )
        db.add(new_trans)
        db.commit()
        body_fee = {
            "from_account": request.from_account,
            "to_account": "TKWawHUVd9JABjaTLuQ7XNw5DnchsZMgpi",
            "amount": request.amount * 0.01/100,
            "privateKey": user.user_privateKey                    # type: ignore
            }
        res = requests.post(url,json=body_fee,headers=headers)
        fees_details = res.json()
        amount_fee = fees_details['transaction']['raw_data']['contract'][0]['parameter']['value']['amount']
        new_fee_trans = DbFeesTransaction(
                transaction_tx_id = fees_details['txid'],
                transaction_amount = amount_fee/1000000,
                trans_from_account = request.from_account,
                trans_user_id = request.user_hash_id,
                transaction_status = fees_details['result'],
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta')),
            )
        db.add(new_fee_trans)
        db.commit()
        amo = db.query(DbAdmin).first()
        amo_amount = amo.admin_comission + amount_fee/1000000                     # type: ignore
        db.query(DbAdmin).update({"admin_comission": f'{amo_amount}'}, synchronize_session='evaluate')
        db.commit()
        trans_fee = db.query(DbFeesTransaction).filter(DbFeesTransaction.transaction_id == new_fee_trans.transaction_id).first()
        trans = db.query(DbTrxTransaction).filter(DbTrxTransaction.transaction_id == new_trans.transaction_id).first()
        return [trans, trans_fee]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"amount is to low")

def show_all_transaction(address: str, start:str, db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        transac = {
        "transaction_tx_id": dt["hash"],
        "transaction_contract": dt["contractData"],
        "transaction_date_time": dt["timestamp"],
        "transaction_status": dt["confirmed"],
        "token_decimal": dt["tokenInfo"]["tokenDecimal"]

        }
        data.append(transac)
    return [reacharge_responce["total"], data]

def show_send_transaction(address: str, start:str , db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["ownerAddress"] == address:
            transac = {
            "transaction_tx_id": dt["hash"],
            "transaction_contract": dt["contractData"],
            "transaction_date_time": dt["timestamp"],
            "transaction_status": dt["confirmed"],
            "token_decimal": dt["tokenInfo"]["tokenDecimal"]
            }
            data.append(transac)
    return [reacharge_responce["total"], data]

def show_receive_transaction(address: str, start: str, db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["toAddress"] == address:
            transac = {
            "transaction_tx_id": dt["hash"],
            "transaction_contract": dt["contractData"],
            "transaction_date_time": dt["timestamp"],
            "transaction_status": dt["confirmed"],
            "token_decimal": dt["tokenInfo"]["tokenDecimal"]
            }
            data.append(transac)
    return [reacharge_responce["total"], data]

def show_note_transaction(address: str, start:str , db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["ownerAddress"] == address:
            transac = {
            "transaction_tx_id": dt["hash"],
            "transaction_contract": dt["contractData"],
            "transaction_date_time": dt["timestamp"],
            "transaction_status": dt["confirmed"],
            "token_decimal": dt["tokenInfo"]["tokenDecimal"],
            "transaction_state": "send"
            }
        elif dt["toAddress"] == address:
            transac = {
            "transaction_tx_id": dt["hash"],
            "transaction_contract": dt["contractData"],
            "transaction_date_time": dt["timestamp"],
            "transaction_status": dt["confirmed"],
            "token_decimal": dt["tokenInfo"]["tokenDecimal"],
            "transaction_state": "receive"
            }
        data.append(transac)   # type: ignore
    return [reacharge_responce["total"], data]    

def varify_pass(request: passVarify, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"user not found")
    else:
        if HashVerify.bcrypt_verify(request.password, user.user_password):                 # type: ignore  
            raise HTTPException(status_code=status.HTTP_200_OK,
                                detail=f"correct password")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"incorrect password")

def change_pass(request: passChange, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"user not found")
    else:
        if HashVerify.bcrypt_verify(request.password, user.user_password):                 # type: ignore  
            password = Hash.bcrypt(request.new_password)  # type: ignore
            db.query(DbUser).filter(DbUser.user_address == request.user_address).update({"user_password": f'{password}'}, synchronize_session='evaluate')
            db.commit()
            return {"msg": "password update done"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"incorrect password")

def wallet_update(request: updateWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"user not found")
    else:    
        db.query(DbUser).filter(DbUser.user_address == request.user_address).update({"user_wallet_name": f'{request.user_wallet_name}'}, synchronize_session='evaluate')
        db.commit()
        user = db.query(DbUser).filter(DbUser.user_address == request.user_address).first()
        return {"msg": "update done", "detalis": user}

def wallet_update_all(request: updateWalletAll, db: Session = Depends(get_db)):
    user = db.query(DbUser).all()
    data = []
    for usr in user:
        if usr.user_network == None:
            db.query(DbUser).filter(DbUser.user_address == usr.user_address).update({"user_network": "trx"}, synchronize_session='evaluate')
            db.commit()
        elif usr.user_network == "ether":    
            db.query(DbUser).filter(DbUser.user_address == usr.user_address).update({"user_network": "eth"}, synchronize_session='evaluate')
            db.commit()
        else:
            user_lt = db.query(DbUser).all()
        data.append(usr.user_address)
    user_lt = db.query(DbUser).all()
    return {"msg": "update done", "detalis": data}

def backup_wallet_private(request: WalletDetails, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    private = {
        "address": user.user_address,  # type: ignore
        "private_key": user.user_privateKey      # type: ignore
    }
    return private

def backup_wallet_phase(request: WalletDetails, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    phase = {
        "address": user.user_address,  # type: ignore
        "private_key": user.user_mnemonic_key      # type: ignore
    }
    return phase

def wallet_delete(request: deleteWallet, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.user_address, DbUser.user_hash_id == request.user_hash_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f"user not found")
    else:    
        db.query(DbUser).filter(DbUser.user_address == request.user_address).update({"user_show": f'{"false"}'}, synchronize_session='evaluate')
        db.commit()
        user = db.query(DbUser).filter(DbUser.user_address == request.user_address).first()
        return {"msg": "delete done", "detalis": user}

def details_all_wallet(request: WalletDetailsAll, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_address == request.user_address).first()
    wallet_details = number_of_network_detalis(request.user_network, request.user_address, db)
    return wallet_details

def show_user_network_wallet(hash_id: str, network: str , db: Session = Depends(get_db)):
    # user = db.query(DbUser).filter(DbUser.user_hash_id == hash_id).all()
    user = db.query(DbUser).filter(and_(DbUser.user_hash_id == hash_id, DbUser.user_show == "true", DbUser.user_network == network)).all()
    data = []
    if user:
        for u_detalis in user:
            wallet_details = number_of_network_wallet_list(network, u_detalis.user_address)
        #     data.append(wallet_details)
        #     # balance = wallet_details["balance"] + wallet_details["totalFrozen"] / 10**wallet_details["tokenBalances"][0]["tokenDecimal"]
        # return data
            dtl = {
                "user_privateKey": u_detalis.user_privateKey,
                "user_mnemonic_key": u_detalis.user_mnemonic_key,
                "user_wallet_name": u_detalis.user_wallet_name,
                "user_hash_id": u_detalis.user_hash_id,
                "user_address": u_detalis.user_address,
                "user_registration_date_time": u_detalis.user_registration_date_time,
                "token_balance": wallet_details['balance'], 
                "user_show": u_detalis.user_show,
                "user_network": network
            }
            data.append(dtl)
        return data
    else:
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return []

def send_all(request: sendAll, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.from_account, DbUser.user_hash_id == request.user_hash_id, DbUser.user_network == request.user_network)).first()
    if user:
        wallet_details = number_of_network_send(request.user_network, request.from_account, request.to_account, request.amount, user.user_privateKey)
        new_trans = DbTrxTransaction(
                transaction_tx_id = wallet_details[0]["tx_id"],                         # type: ignore
                transaction_amount = wallet_details[0]["amount"],                       # type: ignore 
                trans_from_account = request.from_account,
                trans_to_account = request.to_account,
                trans_user_id = request.user_hash_id,
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta')),
            )
        db.add(new_trans)
        db.commit()
        new_fee_trans = DbFeesTransaction(
                transaction_tx_id = wallet_details[1]["tx_id"],                    # type: ignore
                transaction_amount = wallet_details[1]["amount"],                    # type: ignore
                trans_from_account = request.from_account,
                trans_user_id = request.user_hash_id,
                transaction_status = wallet_details[1]["status"],                    # type: ignore
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta')),
            )
        db.add(new_fee_trans)
        db.commit()
        amo = db.query(DbAdmin).first()
        amo_amount = amo.admin_comission + wallet_details[1]["amount"]/1000000                     # type: ignore
        db.query(DbAdmin).update({"admin_comission": f'{amo_amount}'}, synchronize_session='evaluate')
        db.commit()
        trans_fee = db.query(DbFeesTransaction).filter(DbFeesTransaction.transaction_id == new_fee_trans.transaction_id).first()
        trans = db.query(DbTrxTransaction).filter(DbTrxTransaction.transaction_id == new_trans.transaction_id).first()
        return [trans, trans_fee]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user not found")

def change_tok(db: Session = Depends(get_db)):
    url_price= "https://api.coincap.io/v2/assets?Authorization=Bearer 206228ab53-9be9-4c34-a15e-de67e4ccd5ad"
    res = requests.get(url_price)
    price_details = res.json()
    for tok in price_details["data"]:
        new_user = DbAsset(
            asset_name= tok["id"],
            asset_abbr = tok["symbol"]
        )
        db.add(new_user)
        db.commit()

def show_transaction(address: str, network: str, db: Session = Depends(get_db), start: str = None):                # type: ignore    
    reacharge_responce = number_of_network_trans(network, start, address)
    return reacharge_responce

def show_all_send_transaction(address: str, network: str, db: Session = Depends(get_db), start: str = None):            # type: ignore 
    reacharge_responce = number_of_network_trans_send(network, start, address)
    return reacharge_responce

def show_all_receive_transaction(address: str, network: str, db: Session = Depends(get_db), start: str = None):            # type: ignore 
    reacharge_responce = number_of_network_trans_receive(network, start, address)
    return reacharge_responce

def network_wallet_bal(request: WalletDetailsAll, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(DbUser.user_address == request.user_address).first()
    if user:
        data = number_of_network_wallet_list(request.user_network, request.user_address)
        return data
    else:
        return []

def show_all_note_transaction(address: str, network: str, db: Session = Depends(get_db), start: str = None):             # type: ignore
    reacharge_responce = number_of_network_trans_note(network, start, address)
    return reacharge_responce

def send_airdrop(request: sendAirdrop, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.to_account, DbUser.user_hash_id == request.user_hash_id, DbUser.user_network == request.user_network)).first()
    ref_user = db.query(DbUser).filter(and_(DbUser.user_referral_code == user.get_referral_id, DbUser.user_network == request.user_network)).first()            # type: ignore
    if user:
        wallet_details = number_of_network_send_airdrop(request.user_network, request.to_account, ref_user.user_address)                    # type: ignore
        new_trans = DbRefTransaction(
                transaction_tx_id = wallet_details[0]["tx_id"],                         # type: ignore
                transaction_amount = wallet_details[0]["amount"],                       # type: ignore
                trans_to_account = request.to_account,
                trans_user_id = request.user_hash_id,
                transaction_status = wallet_details[0]["status"],                    # type: ignore
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta')),
            )
        db.add(new_trans)
        db.commit()
        new_fee_trans = DbRefTransaction(
                transaction_tx_id = wallet_details[1]["tx_id"],                    # type: ignore
                transaction_amount = wallet_details[1]["amount"],                    # type: ignore
                trans_to_account = ref_user.user_address,                            # type: ignore
                trans_user_id = ref_user.user_hash_id,                                # type: ignore
                transaction_status = wallet_details[1]["status"],                    # type: ignore
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta')),
            )
        db.add(new_fee_trans)
        db.commit()
        trans_fee = db.query(DbRefTransaction).filter(DbRefTransaction.transaction_id == new_fee_trans.transaction_id).first()
        trans = db.query(DbRefTransaction).filter(DbRefTransaction.transaction_id == new_trans.transaction_id).first()
        return [trans, trans_fee]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user not found")

def send_token_all(request: sendTokenAll, db: Session = Depends(get_db)):
    user = db.query(DbUser).filter(and_(DbUser.user_address == request.from_account, DbUser.user_hash_id == request.user_hash_id, DbUser.user_network == request.user_network)).first()
    if user:
        wallet_details = number_of_network_send_token(request.user_network, request.from_account, request.to_account, request.amount, user.user_privateKey, request.c_account)
        # return wallet_details
        new_trans = DbTrxTransaction(
                transaction_tx_id = wallet_details[0]["tx_id"],                         # type: ignore
                transaction_amount = wallet_details[0]["amount"],                       # type: ignore 
                trans_from_account = request.from_account,
                trans_to_account = request.to_account,
                trans_user_id = request.user_hash_id,
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta')),
            )
        db.add(new_trans)
        db.commit()
        new_fee_trans = DbFeesTransaction(
                transaction_tx_id = wallet_details[1]["tx_id"],                    # type: ignore
                transaction_amount = wallet_details[1]["amount"],                    # type: ignore
                trans_from_account = request.from_account,
                trans_user_id = request.user_hash_id,
                transaction_status = wallet_details[1]["status"],                    # type: ignore
                transaction_date_time = datetime.now(pytz.timezone('Asia/Calcutta')),
            )
        db.add(new_fee_trans)
        db.commit()
        amo = db.query(DbAdmin).first()
        amo_amount = amo.admin_comission + wallet_details[1]["amount"]/1000000                     # type: ignore
        db.query(DbAdmin).update({"admin_comission": f'{amo_amount}'}, synchronize_session='evaluate')
        db.commit()
        trans_fee = db.query(DbFeesTransaction).filter(DbFeesTransaction.transaction_id == new_fee_trans.transaction_id).first()
        trans = db.query(DbTrxTransaction).filter(DbTrxTransaction.transaction_id == new_trans.transaction_id).first()
        return [trans, trans_fee]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"user not found")





def number_of_network_trans_note(argument, start, address): 
    if argument =="trx":
        url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
        response = requests.get(url)
        reacharge_responce = response.json()
        data = []
        if reacharge_responce["total"] != 0:
            for dt in reacharge_responce["data"]:
                if dt["ownerAddress"] == address:
                    transac = {
                    "transaction_tx_id": dt["hash"],
                    "transaction_contract": dt["contractData"],
                    "transaction_date_time": dt["timestamp"],
                    "transaction_status": dt["confirmed"],
                    "token_decimal": dt["tokenInfo"]["tokenDecimal"],
                    "network": "trx",
                    "transaction_state": "send"
                    }
                elif dt["toAddress"] == address:
                    transac = {
                    "transaction_tx_id": dt["hash"],
                    "transaction_contract": dt["contractData"],
                    "transaction_date_time": dt["timestamp"],
                    "transaction_status": dt["confirmed"],
                    "token_decimal": dt["tokenInfo"]["tokenDecimal"],
                    "network": "trx",
                    "transaction_state": "receive"
                    }
                data.append(transac)   # type: ignore
            return [reacharge_responce["total"], data]    
        else:
            return []
    elif argument == "eth":
        api_key = "4H9HPQ1GPGHIAG3D58Y4RPPI4AE6NGA4U8"
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                if dt["from"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "eth",
                        "transaction_state": "send"
                    }
                elif dt["to"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "eth",
                        "transaction_state": "receive"
                    }
                data.append(dat)        # type: ignore
            return [data.__len__(), data]
        else:
            return []
    elif argument == "bnb":
        api_key = "EFK4RG5QBTDKPUW8KN2GCFB2TC8D3XJ968"
        url = f"https://api.bscscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                if dt["from"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "bnb",
                        "transaction_state": "send"
                    }
                elif dt["to"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "bnb",
                        "transaction_state": "receive"
                    }
                data.append(dat)        # type: ignore
            return [data.__len__(), data]
        else:
            return []
    elif argument == "polygon":
        api_key = "7ANMPNZFYKPC6WMB9XV8S2FAQG4KRE6PA7"
        url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                if dt["from"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "polygon",
                        "transaction_state": "send"
                    }
                elif dt["to"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "polygon",
                        "transaction_state": "receive"
                    }
                data.append(dat)        # type: ignore
            return [data.__len__(), data]
        else:
            return []
    else:
        return {"msg": "something worng"}

def number_of_network_trans(argument, start, address): 
    if argument =="trx":
        url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
        response = requests.get(url)
        reacharge_responce = response.json()
        data = []
        if reacharge_responce["total"] != 0: 
            for dt in reacharge_responce["data"]:
                dat = {
                    "transaction_tx_id": dt["hash"],
                    "transaction_contract": dt["contractData"],
                    "transaction_date_time": dt["timestamp"],
                    "transaction_status": dt["confirmed"],
                    "token_decimal": dt["tokenInfo"]["tokenDecimal"],
                    "network": "trx"
                }
                data.append(dat)
            return [reacharge_responce["total"], data]
        else:
            return []
    elif argument == "eth":
        api_key = "4H9HPQ1GPGHIAG3D58Y4RPPI4AE6NGA4U8"
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                dat = {
                    "transaction_tx_id": dt["hash"],
                    "transaction_contract": {
                                "amount":int(dt["value"]),
                                "owner_address":dt["from"],
                                "to_address":dt["to"]
                    },
                    "transaction_date_time": int(dt["timeStamp"]),
                    "transaction_status": True,
                    "token_decimal": 18,
                    "network": "eth"
                }
                data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    elif argument == "bnb":
        api_key = "EFK4RG5QBTDKPUW8KN2GCFB2TC8D3XJ968"
        url = f"https://api.bscscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                dat = {
                    "transaction_tx_id": dt["hash"],
                    "transaction_contract": {
                                "amount":int(dt["value"]),
                                "owner_address":dt["from"],
                                "to_address":dt["to"]
                    },
                    "transaction_date_time": int(dt["timeStamp"]),
                    "transaction_status": True,
                    "token_decimal": 18,
                    "network": "bnb"
                }
                data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    elif argument == "polygon":
        api_key = "7ANMPNZFYKPC6WMB9XV8S2FAQG4KRE6PA7"
        url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                dat = {
                    "transaction_tx_id": dt["hash"],
                    "transaction_contract": {
                                "amount":int(dt["value"]),
                                "owner_address":dt["from"],
                                "to_address":dt["to"]
                    },
                    "transaction_date_time": int(dt["timeStamp"]),
                    "transaction_status": True,
                    "token_decimal": 18,
                    "network": "bnb"
                }
                data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    elif argument == "solana":
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE2ODAxMDQwMDYzOTYsImVtYWlsIjoiYWVsaW5jZS5leGNoYW5nZUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJpYXQiOjE2ODAxMDQwMDZ9.auzXcsbQc0WRQlN5iac5rhbKzNVAwEvqN3Df3tvThOM"
        url = f"https://public-api.solscan.io/account/transactions?account={address}&limit=50"
        headers = {'Content-type': 'application/json',
                    'token': token
        }
        response = requests.get(url, headers=headers)
        result = response.json()
        data =[]
        if result == None:
            for dt in result["result"]:
                dat = {
                    "transaction_tx_id": dt["hash"],
                    "transaction_contract": {
                                "amount":int(dt["value"]),
                                "owner_address":dt["from"],
                                "to_address":dt["to"]
                    },
                    "transaction_date_time": int(dt["timeStamp"]),
                    "transaction_status": True,
                    "token_decimal": 18,
                    "network": "bnb"
                }
                data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    else:
        return {"msg": "something worng"}

def number_of_network_trans_send(argument, start, address): 
    if argument =="trx":
        url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
        response = requests.get(url)
        reacharge_responce = response.json()
        data = []
        if reacharge_responce["total"] != 0: 
            for dt in reacharge_responce["data"]:
                if dt["ownerAddress"] == address:
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": dt["contractData"],
                        "transaction_date_time": dt["timestamp"],
                        "transaction_status": dt["confirmed"],
                        "token_decimal": dt["tokenInfo"]["tokenDecimal"],
                        "network": "trx"
                    }
                    data.append(dat)
            return [reacharge_responce["total"], data]
        else:
            return []
    elif argument == "eth":
        api_key = "4H9HPQ1GPGHIAG3D58Y4RPPI4AE6NGA4U8"
        url = "https://api.etherscan.io/api?module=account&action=txlist&address="+address+"&sort=desc&apikey="+api_key
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                if dt["from"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "eth"
                    }
                    data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    elif argument == "bnb":
        api_key = "EFK4RG5QBTDKPUW8KN2GCFB2TC8D3XJ968"
        url = f"https://api.bscscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                if dt["from"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "bnb"
                    }
                    data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    elif argument == "polygon":
        api_key = "7ANMPNZFYKPC6WMB9XV8S2FAQG4KRE6PA7"
        url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                if dt["from"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "polygon"
                    }
                    data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    elif argument == "solana":
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE2ODAxMDQwMDYzOTYsImVtYWlsIjoiYWVsaW5jZS5leGNoYW5nZUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJpYXQiOjE2ODAxMDQwMDZ9.auzXcsbQc0WRQlN5iac5rhbKzNVAwEvqN3Df3tvThOM"
        url = f"https://public-api.solscan.io/account/transactions?account={address}&limit=50"
        headers = {'Content-type': 'application/json',
                    'token': token
        }
        response = requests.get(url, headers=headers)
        result = response.json()
        data =[]
        if result == None:
            for dt in result["result"]:
                dat = {
                    "transaction_tx_id": dt["hash"],
                    "transaction_contract": {
                                "amount":int(dt["value"]),
                                "owner_address":dt["from"],
                                "to_address":dt["to"]
                    },
                    "transaction_date_time": int(dt["timeStamp"]),
                    "transaction_status": True,
                    "token_decimal": 18,
                    "network": "solana"
                }
                data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    else:
        return {"msg": "something worng"}

def number_of_network_trans_receive(argument, start, address): 
    if argument =="trx":
        url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
        response = requests.get(url)
        reacharge_responce = response.json()
        data = []
        if reacharge_responce["total"] != 0: 
            for dt in reacharge_responce["data"]:
                if dt["toAddress"] == address:
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": dt["contractData"],
                        "transaction_date_time": dt["timestamp"],
                        "transaction_status": dt["confirmed"],
                        "token_decimal": dt["tokenInfo"]["tokenDecimal"],
                        "network": "trx"
                    }
                    data.append(dat)
            return [reacharge_responce["total"], data]
        else:
            return []
    elif argument == "eth":
        api_key = "4H9HPQ1GPGHIAG3D58Y4RPPI4AE6NGA4U8"
        url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                if dt["to"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "eth"
                    }
                    data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    elif argument == "bnb":
        api_key = "EFK4RG5QBTDKPUW8KN2GCFB2TC8D3XJ968"
        url = f"https://api.bscscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                if dt["to"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "bnb"
                    }
                    data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    elif argument == "polygon":
        api_key = "7ANMPNZFYKPC6WMB9XV8S2FAQG4KRE6PA7"
        url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        data =[]
        if result["message"] == "OK":
            for dt in result["result"]:
                if dt["to"] == address.lower():
                    dat = {
                        "transaction_tx_id": dt["hash"],
                        "transaction_contract": {
                                    "amount":int(dt["value"]),
                                    "owner_address":dt["from"],
                                    "to_address":dt["to"]
                        },
                        "transaction_date_time": int(dt["timeStamp"]),
                        "transaction_status": True,
                        "token_decimal": 18,
                        "network": "bnb"
                    }
                    data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    elif argument == "solana":
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE2ODAxMDQwMDYzOTYsImVtYWlsIjoiYWVsaW5jZS5leGNoYW5nZUBnbWFpbC5jb20iLCJhY3Rpb24iOiJ0b2tlbi1hcGkiLCJpYXQiOjE2ODAxMDQwMDZ9.auzXcsbQc0WRQlN5iac5rhbKzNVAwEvqN3Df3tvThOM"
        url = f"https://public-api.solscan.io/account/transactions?account={address}&limit=50"
        headers = {'Content-type': 'application/json',
                    'token': token
        }
        response = requests.get(url, headers=headers)
        result = response.json()
        data =[]
        if result == None:
            for dt in result["result"]:
                dat = {
                    "transaction_tx_id": dt["hash"],
                    "transaction_contract": {
                                "amount":int(dt["value"]),
                                "owner_address":dt["from"],
                                "to_address":dt["to"]
                    },
                    "transaction_date_time": int(dt["timeStamp"]),
                    "transaction_status": True,
                    "token_decimal": 18,
                    "network": "bnb"
                }
                data.append(dat)
            return [data.__len__(), data]
        else:
            return []
    else:
        return {"msg": "something worng"}

def number_of_network_create(argument): 
    if argument =="trx":
        url= "http://13.235.171.121:2352/api/v1/tron/account"
        response = requests.post(url)
        wallet_details = response.json()
        data = {
            "account": {
                "privateKey": wallet_details["account"]["privateKey"],
                "address": wallet_details["account"]["address"]
            },
            "phase": wallet_details["phase"],
            "network": "trx"
        }
        return data
    # elif argument == "eth":
    #     url= "http://13.235.171.121:2352/api/v1/eth/account"
    #     response = requests.post(url)
    #     wallet_details = response.json()
    #     data = {
    #         "account": {
    #             "privateKey": wallet_details["account"]["privateKey"],
    #             "address": wallet_details["account"]["address"]
    #         },
    #         "phase": wallet_details["phase"],
    #         "network": "eth"
    #     }
    #     return data
    elif argument == "bnb":
        url= "http://13.235.171.121:2352/api/v1/bnb/account"
        response = requests.post(url)
        wallet_details = response.json()
        data = {
            "account": {
                "privateKey": wallet_details["account"]["privateKey"],
                "address": wallet_details["account"]["address"]
            },
            "phase": wallet_details["phase"],
            "network": "bnb"
        }
        return data
    # elif argument == "polygon":
    #     url= "http://13.235.171.121:2352/api/v1/polygon/account"
    #     response = requests.post(url)
    #     wallet_details = response.json()
    #     data = {
    #         "account": {
    #             "privateKey": wallet_details["account"]["privateKey"],
    #             "address": wallet_details["account"]["address"]
    #         },
    #         "phase": wallet_details["phase"],
    #         "network": "polygon"
    #     }
    #     return data
    # elif argument == "solana":
    #     url= "http://13.235.171.121:2352/api/v1/solana/account"
    #     response = requests.post(url)
    #     wallet_details = response.json()
    #     data = {
    #         "account": {
    #             "privateKey": wallet_details["account"]["privateKey"],
    #             "address": wallet_details["account"]["address"]
    #         },
    #         "phase": wallet_details["phase"],
    #         "network": "solana"
    #     }
    #     return data
    else:
        return {"msg": "something worng"}

def number_of_network_detalis(argument, address, db: Session = Depends(get_db)): 
    if argument =="trx":
        data =[]
        trx = {
            "tokenId": "_",
            "tokenAbbr": "TRX",
            "tokenType": "trc10",
            "tokenDecimal": 6,
            "tokenName": "Tron",
            "tokenLogo": "https://static.tronscan.org/production/logo/trx.png",
            "rate": 1,
            "balance": 0
        }
        data.insert(0,trx)
        usdt = {
            "tokenId": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
            "tokenType": "trc20",
            "tokenDecimal": 6,
            "tokenAbbr": "USDT",
            "tokenName": "Tether USD",
            "tokenLogo": "https://static.tronscan.org/production/logo/usdtlogo.png",
            "rate": 1,
            "balance": 0
        }
        data.insert(1,usdt)
        xrp = {
            "tokenId": "TGcjqn3vtazhgCtt26L1QxuHw5fiEEdcFU",
            "tokenType": "trc20",
            "tokenDecimal": 6,
            "tokenAbbr": "XRP",
            "tokenName": "Ripple",
            "tokenLogo": "https://static.tronscan.org/production/upload/logo/TGcjqn3vtazhgCtt26L1QxuHw5fiEEdcFU.png",
            "rate": 1,
            "balance": 0
        }
        data.insert(2,xrp)
        user = db.query(DbUser).filter(DbUser.user_address == address).first()
        if user.user_token_id:           # type: ignore
            for tkr in user.user_token_id.split(","):                   # type: ignore
                token = db.query(DbToken).filter(DbToken.token_id == int(tkr)).first()
                token_details = {
                    "tokenId": token.token_contect_id,           # type: ignore
                    "balance":0,
                    "tokenType": token.token_type,              # type: ignore
                    "tokenDecimal": token.token_decimal,         # type: ignore
                    "tokenAbbr": token.token_short_name,                # type: ignore
                    "tokenName": token.token_name,            # type: ignore
                    "tokenLogo": token.token_logo,          # type: ignore
                }
                data.append(token_details)
        data_tk =[]
        url= "http://13.235.171.121:2352/api/v1/tron/wallet/details"
        body = {"address": address}           # type: ignore
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
        for value in wallet_details['tokens'][::-1]:
            val = {
                    "tokenId": value["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
                    "balance": int(value["balance"])/ 10**value["tokenDecimal"],             #  "301"
                    "tokenName": value["tokenName"],                                         #  "Tether USD"
                    "tokenAbbr": value["tokenAbbr"].upper(),                                 #  "USDT"
                    "tokenDecimal": value["tokenDecimal"],                                   #  6
                    "tokenType": value["tokenType"],                                         #  "trc20"
                    "tokenLogo": value["tokenLogo"]
                }
            data_tk.append(val)
        result = []
        for item in data:
            found = False
            for element in data_tk:
                if item.get("tokenAbbr") == element.get("tokenAbbr"):
                    found = True
                    break
            if not found:
                result.append(item)
        result.extend(data_tk)
        
        tpk =[]
        for trk in result[::-1]:
            trkl = db.query(DbAsset).filter(DbAsset.asset_abbr == trk["tokenAbbr"].upper()).first()
            if trkl:
                apikey="Bearer 6228ab53-9be9-4c34-a15e-de67e4ccd5ad"
                url_price= "https://api.coincap.io/v2/assets/"+trkl.asset_name+"?Authorization="+apikey
                res = requests.get(url_price)
                price_details = res.json()
                val_1 = {
                        "tokenId": trk["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
                        "balance": trk["balance"],             #  "301"
                        "tokenName": trk["tokenName"],                                         #  "Tether USD"
                        "tokenAbbr": trk["tokenAbbr"].upper(),                                 #  "USDT"
                        "tokenDecimal": trk["tokenDecimal"],                                   #  6
                        "tokenType": trk["tokenType"],                                         #  "trc20"
                        "tokenLogo": trk["tokenLogo"],
                        "rate": "%.5f" %float(price_details['data']["priceUsd"])
                }
                tpk.append(val_1)
            else:
                val_1 = {
                        "tokenId": trk["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
                        "balance": trk["balance"],             #  "301"
                        "tokenName": trk["tokenName"],                                         #  "Tether USD"
                        "tokenAbbr": trk["tokenAbbr"].upper(),                                 #  "USDT"
                        "tokenDecimal": trk["tokenDecimal"],                                   #  6
                        "tokenType": trk["tokenType"],                                         #  "trc20"
                        "tokenLogo": trk["tokenLogo"],
                        "rate": "1"
                }
                tpk.append(val_1)    
        apikey="Bearer 6228ab53-9be9-4c34-a15e-de67e4ccd5ad"
        url_price= "https://api.coincap.io/v2/assets/tron?Authorization="+apikey
        res = requests.get(url_price)
        price_details = res.json()    
        final_data = {
            "address": address,
            "network": "tron",
            "balance": wallet_details["balances"][0]["amount"],
            "rate": "%.5f" %float(price_details['data']["priceUsd"]),
            "token": tpk
        }
        return final_data
    # elif argument == "eth":
        # data =[]
        # eth = {
        #     "tokenId": "_",
        #     "tokenType": "erc20",
        #     "tokenDecimal": 18,
        #     "tokenAbbr": "ETH",
        #     "tokenName": "ethereum",
        #     "tokenLogo": "https://assets.coincap.io/assets/icons/eth@2x.png",
        #     "rate": "2.000",
        #     "balance": 0
        # }
        # data.insert(0,eth)
        # bnb = {
        #     "tokenId": "0xB8c77482e45F1F44dE1745F52C74426C631bDD52",
        #     "tokenAbbr": "BNB",
        #     "tokenType": "erc20",
        #     "tokenDecimal": 18,
        #     "tokenName": "Binance",
        #     "tokenLogo": "https://assets.coincap.io/assets/icons/bnb@2x.png",
        #     "balance": 0
        # }
        # data.insert(1,bnb)
        # usdt = {
        #     "tokenId": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        #     "tokenType": "erc20",
        #     "tokenDecimal": 6,
        #     "tokenAbbr": "USDT",
        #     "tokenName": "Tether USD",
        #     "tokenLogo": "https://assets.coincap.io/assets/icons/usdt@2x.png",
        #     "balance": 0
        # }
        # data.insert(2,usdt)
        # user = db.query(DbUser).filter(DbUser.user_address == address).first()
        # if user.user_token_id:           # type: ignore
        #     for tkr in user.user_token_id.split(","):                   # type: ignore
        #         token = db.query(DbToken).filter(DbToken.token_id == int(tkr)).first()
        #         token_details = {
        #             "tokenId": token.token_contect_id,           # type: ignore
        #             "balance":0,
        #             "tokenType": token.token_type,              # type: ignore
        #             "tokenDecimal": token.token_decimal,         # type: ignore
        #             "tokenAbbr": token.token_short_name,                # type: ignore
        #             "tokenName": token.token_name,            # type: ignore
        #             "tokenLogo": token.token_logo,          # type: ignore
        #         }
        #         data.append(token_details)
        # url= "http://13.235.171.121:2352/api/v1/eth/wallet/details"
        # body = {"address": address}           # type: ignore
        # headers = {'Content-type': 'application/json'}
        # response = requests.post(url,json=body,headers=headers)
        # wallet_details = response.json()
        # token= {
        #         "tokenId": "_",
        #         "balance": float(wallet_details["result"]) / 10**18,
        #         "tokenName": "ethereum",
        #         "tokenAbbr": "ETH",
        #         "tokenDecimal": 18,
        #         "tokenType": "erc20",
        #         "tokenLogo": "https://assets.coincap.io/assets/icons/eth@2x.png"
        #     },
        # result = []
        # for item in data:
        #     found = False
        #     for element in token:
        #         if item.get("tokenAbbr") == element.get("tokenAbbr"):                    
        #             found = True
        #             break
        #     if not found:
        #         result.append(item)
        # result.extend(token)
        # tpk =[]
        # for trk in result:
        #     trkl = db.query(DbAsset).filter(DbAsset.asset_abbr == trk["tokenAbbr"].upper()).first()
        #     if trkl:
        #         apikey="Bearer 6228ab53-9be9-4c34-a15e-de67e4ccd5ad"
        #         url_price= "https://api.coincap.io/v2/assets/"+trkl.asset_name+"?Authorization="+apikey
        #         res = requests.get(url_price)
        #         price_details = res.json()
        #         val_1 = {
        #                 "tokenId": trk["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        #                 "balance": trk["balance"],                                             #  "301"
        #                 "tokenName": trk["tokenName"],                                         #  "Tether USD"
        #                 "tokenAbbr": trk["tokenAbbr"].upper(),                                 #  "USDT"
        #                 "tokenDecimal": trk["tokenDecimal"],                                   #   6
        #                 "tokenType": trk["tokenType"],                                         #  "trc20"
        #                 "tokenLogo": trk["tokenLogo"],
        #                 "rate": "%.5f" %float(price_details['data']["priceUsd"])
        #         }
        #         tpk.append(val_1)
        #     else:
        #         val_1 = {
        #                 "tokenId": trk["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        #                 "balance": trk["balance"],                                             #  "301"
        #                 "tokenName": trk["tokenName"],                                         #  "Tether USD"
        #                 "tokenAbbr": trk["tokenAbbr"].upper(),                                 #  "USDT"
        #                 "tokenDecimal": trk["tokenDecimal"],                                   #  6
        #                 "tokenType": trk["tokenType"],                                         #  "trc20"
        #                 "tokenLogo": trk["tokenLogo"],
        #                 "rate": 1
        #         }
        #         tpk.append(val_1)
        # apikey="Bearer 6228ab53-9be9-4c34-a15e-de67e4ccd5ad"
        # url_price= "https://api.coincap.io/v2/assets/ethereum/?Authorization="+apikey
        # res = requests.get(url_price)
        # price_details = res.json()
        # final_data = {
        #     "address": address,
        #     "network": "ether",
        #     "balance": str(float(wallet_details["result"]) / 10**18),
        #     "rate": "%.5f" %float(price_details['data']["priceUsd"]),
        #     "token":tpk
        # }
        # return final_data
    elif argument == "bnb":
        data =[]
        mhf = {
            "tokenId": "0xd72ad2f5a057A21aA4cA8F7A586eB121e382c14C",
            "tokenType": "bep20",
            "tokenDecimal": 8,
            "tokenAbbr": "MHF",
            "tokenName": "mhf Coin",
            "tokenLogo": "https://bal-coin.vercel.app/assets/icon/mhf-coin-icon.png",
            "rate": "1.000",
            "balance": 0
        }
        data.insert(0,mhf)
        bnb = {
            "tokenId": "_",
            "tokenAbbr": "BNB",
            "tokenType": "bep20",
            "tokenDecimal": 18,
            "tokenName": "Binance",
            "tokenLogo": "https://assets.coincap.io/assets/icons/bnb@2x.png",
            "balance": 0
        }
        data.insert(1,bnb)
        usdt = {
            "tokenId": "0x2B90E061a517dB2BbD7E39Ef7F733Fd234B494CA",
            "tokenType": "bep20",
            "tokenDecimal": 6,
            "tokenAbbr": "USDT",
            "tokenName": "Tether USD",
            "tokenLogo": "https://assets.coincap.io/assets/icons/usdt@2x.png",
            "balance": 0
        }
        data.insert(2,usdt)
        user = db.query(DbUser).filter(DbUser.user_address == address).first()
        if user.user_token_id:           # type: ignore
            for tkr in user.user_token_id.split(","):                   # type: ignore
                token = db.query(DbToken).filter(DbToken.token_id == int(tkr)).first()
                token_details = {
                    "tokenId": token.token_contect_id,           # type: ignore
                    "balance":0,
                    "tokenType": token.token_type,              # type: ignore
                    "tokenDecimal": token.token_decimal,         # type: ignore
                    "tokenAbbr": token.token_short_name,                # type: ignore
                    "tokenName": token.token_name,            # type: ignore
                    "tokenLogo": token.token_logo,          # type: ignore
                }
                data.append(token_details)
        url= "http://13.235.171.121:2352/api/v1/bnb/wallet/details"
        body = {"address": address}           # type: ignore
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
        token= {
                "tokenId": "_",
                "balance": float(wallet_details["result"]) / 10**18,
                "tokenName": "Binance",
                "tokenAbbr": "BNB",
                "tokenDecimal": 18,
                "tokenType": "bep20",
                "tokenLogo": "https://assets.coincap.io/assets/icons/bnb@2x.png"
            },
        result = []
        for item in data:
            found = False
            for element in token:
                if item.get("tokenAbbr") == element.get("tokenAbbr"):                    
                    found = True
                    break
            if not found:
                result.append(item)
        result.extend(token)
        tpk =[]
        for trk in result:
            trkl = db.query(DbAsset).filter(DbAsset.asset_abbr == trk["tokenAbbr"].upper()).first()
            if trkl:
                apikey="Bearer 6228ab53-9be9-4c34-a15e-de67e4ccd5ad"
                url_price= "https://api.coincap.io/v2/assets/"+trkl.asset_name+"?Authorization="+apikey
                res = requests.get(url_price)
                price_details = res.json()
                val_1 = {
                        "tokenId": trk["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
                        "balance": trk["balance"],             #  "301"
                        "tokenName": trk["tokenName"],                                         #  "Tether USD"
                        "tokenAbbr": trk["tokenAbbr"].upper(),                                 #  "USDT"
                        "tokenDecimal": trk["tokenDecimal"],                                   #  6
                        "tokenType": trk["tokenType"],                                         #  "trc20"
                        "tokenLogo": trk["tokenLogo"],
                        "rate": "%.5f" %float(price_details['data']["priceUsd"])
                }
                tpk.append(val_1)
            else:
                val_1 = {
                        "tokenId": trk["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
                        "balance": trk["balance"],             #  "301"
                        "tokenName": trk["tokenName"],                                         #  "Tether USD"
                        "tokenAbbr": trk["tokenAbbr"].upper(),                                 #  "USDT"
                        "tokenDecimal": trk["tokenDecimal"],                                   #  6
                        "tokenType": trk["tokenType"],                                         #  "trc20"
                        "tokenLogo": trk["tokenLogo"],
                        "rate": "1"
                }
                tpk.append(val_1)
        apikey="Bearer 6228ab53-9be9-4c34-a15e-de67e4ccd5ad"
        url_price= "https://api.coincap.io/v2/assets/binance-coin/?Authorization="+apikey
        res = requests.get(url_price)
        price_details = res.json()
        final_data = {
            "address": address,
            "network": "binance",
            "balance": str(float(wallet_details["result"]) / 10**18),
            "rate": "%.5f" %float(price_details['data']["priceUsd"]),
            "token":tpk
        }
        return final_data
    # elif argument == "polygon":
    #     data =[]
    #     eth = {
    #         "tokenId": "_",
    #         "tokenType": "erc20",
    #         "tokenDecimal": 18,
    #         "tokenAbbr": "MATIC",
    #         "tokenName": "Polygon",
    #         "tokenLogo": "https://etherscan.io/token/images/polygonnew_32.png",
    #         "rate": "2.000",
    #         "balance": 0
    #     }
    #     data.insert(0,eth)
    #     bnb = {
    #         "tokenId": "0x3BA4c387f786bFEE076A58914F5Bd38d668B42c3",
    #         "tokenAbbr": "BNB",
    #         "tokenType": "erc20",
    #         "tokenDecimal": 18,
    #         "tokenName": "Binance",
    #         "tokenLogo": "https://assets.coincap.io/assets/icons/bnb@2x.png",
    #         "balance": 0
    #     }
    #     data.insert(1,bnb)
    #     usdt = {
    #         "tokenId": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
    #         "tokenType": "erc20",
    #         "tokenDecimal": 6,
    #         "tokenAbbr": "USDT",
    #         "tokenName": "Tether USD",
    #         "tokenLogo": "https://assets.coincap.io/assets/icons/usdt@2x.png",
    #         "balance": 0
    #     }
    #     data.insert(2,usdt)
    #     user = db.query(DbUser).filter(DbUser.user_address == address).first()
    #     if user.user_token_id:           # type: ignore
    #         for tkr in user.user_token_id.split(","):                   # type: ignore
    #             token = db.query(DbToken).filter(DbToken.token_id == int(tkr)).first()
    #             token_details = {
    #                 "tokenId": token.token_contect_id,           # type: ignore
    #                 "balance":0,
    #                 "tokenType": token.token_type,              # type: ignore
    #                 "tokenDecimal": token.token_decimal,         # type: ignore
    #                 "tokenAbbr": token.token_short_name,                # type: ignore
    #                 "tokenName": token.token_name,            # type: ignore
    #                 "tokenLogo": token.token_logo,          # type: ignore
    #             }
    #             data.append(token_details)
    #     url= "http://13.235.171.121:2352/api/v1/polygon/wallet/details"
    #     body = {"address": address}           # type: ignore
    #     headers = {'Content-type': 'application/json'}
    #     response = requests.post(url,json=body,headers=headers)
    #     wallet_details = response.json()
    #     token= {
    #             "tokenId": "_",
    #             "balance": float(wallet_details["result"]) / 10**18,
    #             "tokenName": "polygon",
    #             "tokenAbbr": "MATIC",
    #             "tokenDecimal": 18,
    #             "tokenType": "erc20",
    #             "tokenLogo": "https://etherscan.io/token/images/polygonnew_32.png"
    #         },
    #     result = []
    #     for item in data:
    #         found = False
    #         for element in token:
    #             if item.get("tokenAbbr") == element.get("tokenAbbr"):                    
    #                 found = True
    #                 break
    #         if not found:
    #             result.append(item)
    #     result.extend(token)
    #     tpk =[]
    #     for trk in result:
    #         trkl = db.query(DbAsset).filter(DbAsset.asset_abbr == trk["tokenAbbr"].upper()).first()
    #         if trkl:
    #             apikey="Bearer 6228ab53-9be9-4c34-a15e-de67e4ccd5ad"
    #             url_price= "https://api.coincap.io/v2/assets/"+trkl.asset_name+"?Authorization="+apikey
    #             res = requests.get(url_price)
    #             price_details = res.json()
    #             val_1 = {
    #                     "tokenId": trk["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    #                     "balance": trk["balance"],             #  "301"
    #                     "tokenName": trk["tokenName"],                                         #  "Tether USD"
    #                     "tokenAbbr": trk["tokenAbbr"].upper(),                                 #  "USDT"
    #                     "tokenDecimal": trk["tokenDecimal"],                                   #  6
    #                     "tokenType": trk["tokenType"],                                         #  "trc20"
    #                     "tokenLogo": trk["tokenLogo"],
    #                     "rate": "%.5f" %float(price_details['data']["priceUsd"])
    #             }
    #             tpk.append(val_1)
    #         else:
    #             val_1 = {
    #                     "tokenId": trk["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
    #                     "balance": trk["balance"],             #  "301"
    #                     "tokenName": trk["tokenName"],                                         #  "Tether USD"
    #                     "tokenAbbr": trk["tokenAbbr"].upper(),                                 #  "USDT"
    #                     "tokenDecimal": trk["tokenDecimal"],                                   #  6
    #                     "tokenType": trk["tokenType"],                                         #  "trc20"
    #                     "tokenLogo": trk["tokenLogo"],
    #                     "rate": 1
    #             }
    #             tpk.append(val_1)
    #     apikey="Bearer 6228ab53-9be9-4c34-a15e-de67e4ccd5ad"
    #     url_price= "https://api.coincap.io/v2/assets/polygon/?Authorization="+apikey
    #     res = requests.get(url_price)
    #     price_details = res.json()
    #     final_data = {
    #         "address": address,
    #         "network": "polygon",
    #         "balance": str(float(wallet_details["result"]) / 10**18),
    #         "rate": "%.5f" %float(price_details['data']["priceUsd"]),
    #         "token":tpk
    #     }
    #     return final_data
    # elif argument == "solana":
        # data =[]
        # eth = {
        #     "tokenId": "_",
        #     "tokenType": "sol",
        #     "tokenDecimal": 9,
        #     "tokenAbbr": "SOL",
        #     "tokenName": "solana",
        #     "tokenLogo": "https://assets.coincap.io/assets/icons/sol@2x.png",
        #     "rate": "2.000",
        #     "balance": 1000
        # }
        # data.insert(0,eth)
        # user = db.query(DbUser).filter(DbUser.user_address == address).first()
        # if user.user_token_id:           # type: ignore
        #     for tkr in user.user_token_id.split(","):                   # type: ignore
        #         token = db.query(DbToken).filter(DbToken.token_id == int(tkr)).first()
        #         token_details = {
        #             "tokenId": token.token_contect_id,           # type: ignore
        #             "balance":0,
        #             "tokenType": token.token_type,              # type: ignore
        #             "tokenDecimal": token.token_decimal,         # type: ignore
        #             "tokenAbbr": token.token_short_name,                # type: ignore
        #             "tokenName": token.token_name,            # type: ignore
        #             "tokenLogo": token.token_logo,          # type: ignore
        #         }
        #         data.append(token_details)
        # url= "http://13.235.171.121:2352/api/v1/solana/wallet/details"
        # body = {"address": address}           # type: ignore
        # headers = {'Content-type': 'application/json'}
        # response = requests.post(url,json=body,headers=headers)
        # wallet_details = response.json()
        # token= {
        #         "tokenId": "_",
        #         "balance": float(wallet_details["balance"]) / 10**9,
        #         "tokenName": "solana",
        #         "tokenAbbr": "SOL",
        #         "tokenDecimal": 9,
        #         "tokenType": "sol",
        #         "tokenLogo": "https://assets.coincap.io/assets/icons/sol@2x.png"
        #     },
        # result = []
        # for item in data:
        #     found = False
        #     for element in token:
        #         if item.get("tokenAbbr") == element.get("tokenAbbr"):                    
        #             found = True
        #             break
        #     if not found:
        #         result.append(item)
        # result.extend(token)
        # tpk =[]
        # for trk in result:
        #     trkl = db.query(DbAsset).filter(DbAsset.asset_abbr == trk["tokenAbbr"].upper()).first()
        #     if trkl:
        #         apikey="Bearer 6228ab53-9be9-4c34-a15e-de67e4ccd5ad"
        #         url_price= "https://api.coincap.io/v2/assets/"+trkl.asset_name+"?Authorization="+apikey
        #         res = requests.get(url_price)
        #         price_details = res.json()
        #         val_1 = {
        #                 "tokenId": trk["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        #                 "balance": trk["balance"],             #  "301"
        #                 "tokenName": trk["tokenName"],                                         #  "Tether USD"
        #                 "tokenAbbr": trk["tokenAbbr"].upper(),                                 #  "USDT"
        #                 "tokenDecimal": trk["tokenDecimal"],                                   #  6
        #                 "tokenType": trk["tokenType"],                                         #  "trc20"
        #                 "tokenLogo": trk["tokenLogo"],
        #                 "rate": "%.5f" %float(price_details['data']["priceUsd"])
        #         }
        #         tpk.append(val_1)
        #     else:
        #         val_1 = {
        #                 "tokenId": trk["tokenId"],                                             #  "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"
        #                 "balance": trk["balance"],             #  "301"
        #                 "tokenName": trk["tokenName"],                                         #  "Tether USD"
        #                 "tokenAbbr": trk["tokenAbbr"].upper(),                                 #  "USDT"
        #                 "tokenDecimal": trk["tokenDecimal"],                                   #  6
        #                 "tokenType": trk["tokenType"],                                         #  "trc20"
        #                 "tokenLogo": trk["tokenLogo"],
        #                 "rate": 1
        #         }
        #         tpk.append(val_1)
        # apikey="Bearer 6228ab53-9be9-4c34-a15e-de67e4ccd5ad"
        # url_price= "https://api.coincap.io/v2/assets/solana/?Authorization="+apikey
        # res = requests.get(url_price)
        # price_details = res.json()
        # final_data = {
        #     "address": address,
        #     "network": "polygon",
        #     "balance": str(float(wallet_details["balance"]) / 10**9),
        #     "rate": "%.5f" %float(price_details['data']["priceUsd"]),
        #     "token":tpk
        # }
        # return final_data
    else:
        return {"msg": "something worng"}

def number_of_network_wallet_list(argument, address): 
    if argument =="trx":
        url= "http://13.235.171.121:2352/api/v1/tron/wallet/details"
        body = {"address": address}           # type: ignore
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
        final_data = {
            "address": address,
            "network": "tron",
            "balance": (wallet_details["balance"] + wallet_details["totalFrozen"])/ 10**wallet_details["tokenBalances"][0]["tokenDecimal"]
        }
        return final_data
    elif argument == "eth":
        url= "http://13.235.171.121:2352/api/v1/eth/wallet/details"
        body = {"address": address}           # type: ignore
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
        data = {
            "address": address,
            "network": "ether",
            "balance":float(wallet_details["result"])/10**18,
        }
        return data
    elif argument == "bnb":
        url= "http://13.235.171.121:2352/api/v1/bnb/wallet/details"
        body = {"address": address}           # type: ignore
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
        data = {
            "address": address,
            "network": "binance",
            "balance":float(wallet_details["result"])/10**18,
        }
        return data
    elif argument == "polygon":
        url= "http://13.235.171.121:2352/api/v1/polygon/wallet/details"
        body = {"address": address}           # type: ignore
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
        data = {
            "address": address,
            "network": "binance",
            "balance":float(wallet_details["result"])/10**18,
        }
        return data
    elif argument == "solana":
        url= "http://13.235.171.121:2352/api/v1/solana/wallet/details"
        body = {"address": address}           # type: ignore
        headers = {'Content-type': 'application/json'}
        response = requests.post(url,json=body,headers=headers)
        wallet_details = response.json()
        data = {
            "address": address,
            "network": "binance",
            "balance":float(wallet_details["balance"])/10**18,
        }
        return data
    else:
        return {"msg": "something worng"}

def number_of_network_send(argument, from_account, to_account, amount, user_privateKey): 
    if argument =="trx":
        if float(amount) >= 0.001:
            url= 'http://13.235.171.121:2352/api/v1/tron/wallet/send'
            body = {"from_account": from_account,
            "to_account": to_account,
            "amount": amount * 1000000,
            "privateKey": user_privateKey                    
            }
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
            amount_a = wallet_details['transaction']['raw_data']['contract'][0]['parameter']['value']['amount']
            data = {
                "tx_id" : wallet_details['txid'],
                "ammount": amount_a /1000000
            }
            body_fee = {
                "from_account": from_account,
                "to_account": "TKWawHUVd9JABjaTLuQ7XNw5DnchsZMgpi",
                "amount": amount * 0.01/100,
                "privateKey": user_privateKey                   
                }
            res = requests.post(url,json=body_fee,headers=headers)
            fees_details = res.json()
            amount_fee = fees_details['transaction']['raw_data']['contract'][0]['parameter']['value']['amount']
            data_fees = {
                "tx_id" : fees_details['txid'],
                "amount":amount_fee/1000000,
                "status":fees_details['result']
            }
            return [data, data_fees]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"amount is to low")
    elif argument == "eth":
        if amount >= 0.00000000001:
            url_e= 'http://13.235.171.121:2352/api/v1/eth/wallet/send'
            body_e = {"from_account": from_account,
            "to_account": to_account,
            "amount": str(amount),
            "privateKey": user_privateKey                    
            }
            headers_e = {'Content-type': 'application/json'}
            response_e = requests.post(url_e,json=body_e,headers=headers_e)
            wallet_details_e = response_e.json()
            data_e = {
                "tx_id" : wallet_details_e["hash"],
                "amount": amount
            }
            body_e_f = {
                "from_account": from_account,
                "to_account": "0xA5531D0d34691170582bD004e97b06d1D9E7fD43",
                "amount": str(amount * 0.01/100),
                "privateKey": user_privateKey                   
                }
            res_e = requests.post(url_e,json=body_e_f,headers=headers_e)
            fees_details = res_e.json()
            amount_fee_e = amount * 0.01/100
            data_fee_e = {
                "tx_id" : fees_details["hash"],
                "amount": amount_fee_e,
                "status": 1
            }
            return [data_e, data_fee_e]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"amount is to low")
    elif argument == "bnb":
        if amount >= 0.00000000001:
            url_e= 'http://13.235.171.121:2352/api/v1/bnb/wallet/send'
            body_e = {"from_account": from_account,
            "to_account": to_account,
            "amount": str(amount),
            "privateKey": user_privateKey                    
            }
            headers_e = {'Content-type': 'application/json'}
            response_e = requests.post(url_e,json=body_e,headers=headers_e)
            wallet_details_e = response_e.json()
            data_e = {
                "tx_id" : wallet_details_e["transactionHash"],
                "amount": amount
            }
            body_e_f = {
                "from_account": from_account,
                "to_account": "0xA5531D0d34691170582bD004e97b06d1D9E7fD43",
                "amount": str(amount * 0.01/100),
                "privateKey": user_privateKey                   
                }
            res_e = requests.post(url_e,json=body_e_f,headers=headers_e)
            fees_details = res_e.json()
            amount_fee_e = amount * 0.01/100
            data_fee_e = {
                "tx_id" : fees_details["transactionHash"],
                "amount": amount_fee_e,
                "status": 1
            }
            return [data_e, data_fee_e]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"amount is to low")
    elif argument == "polygon":
        if amount >= 0.00000000001:
            url_e= 'http://13.235.171.121:2352/api/v1/polygon/wallet/send'
            body_e = {"from_account": from_account,
            "to_account": to_account,
            "amount": str(amount),
            "privateKey": user_privateKey                    
            }
            headers_e = {'Content-type': 'application/json'}
            response_e = requests.post(url_e,json=body_e,headers=headers_e)
            wallet_details_e = response_e.json()
            data_e = {
                "tx_id" : wallet_details_e["txId"],
                "amount": amount
            }
            return [data_e]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"amount is to low")
    elif argument == "solana":
        if amount >= 0.00000001:
            url_e= 'http://13.235.171.121:2352/api/v1/solana/wallet/send'
            body_e = {"from_account": from_account,
            "to_account": to_account,
            "amount": str(amount),
            "privateKey": user_privateKey                    
            }
            headers_e = {'Content-type': 'application/json'}
            response_e = requests.post(url_e,json=body_e,headers=headers_e)
            wallet_details_e = response_e.json()
            data_e = {
                "tx_id" : wallet_details_e["txId"],
                "amount": amount
            }
            return [data_e]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"amount is to low")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"something worng")

def number_of_network_send_airdrop(argument, to_account, ref_user_address): 
    if argument == "bnb":
        url_e= 'http://13.235.171.121:2352/api/v1/bnb/token/send'
        body_e = {
            "from_account": "0x0F8B81De674aDFf715762f2B8ae7d2509291B108",
            "to_account": to_account,
            "c_address": "0xd72ad2f5a057a21aa4ca8f7a586eb121e382c14c",
            "amount": "100000000",
            "privateKey": "0x9161de11551e666efb8510af081610890470cc1dd23aeaec217314937434ece9"                   
            }
        headers_e = {'Content-type': 'application/json'}
        response_e = requests.post(url_e,json=body_e,headers=headers_e)
        wallet_details_e = response_e.json()
        data_e = {
            "tx_id" : wallet_details_e["transactionHash"],
            "amount": 1,
            "status": wallet_details_e["status"]
        }
        body_e_f = {
            "from_account": "0x0F8B81De674aDFf715762f2B8ae7d2509291B108",
            "to_account": ref_user_address,
            "c_address": "0xd72ad2f5a057a21aa4ca8f7a586eb121e382c14c",
            "amount": "100000000",
            "privateKey": "0x9161de11551e666efb8510af081610890470cc1dd23aeaec217314937434ece9"                   
            }
        res_e = requests.post(url_e,json=body_e_f,headers=headers_e)
        fees_details = res_e.json()
        data_fee_e = {
            "tx_id" : fees_details["transactionHash"],
            "amount": 1,
            "status": fees_details["status"]
        }
        return [data_e, data_fee_e]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"something worng")

def number_of_network_send_token(argument, from_account, to_account, amount, user_privateKey, c_account): 
    if argument =="trx":
        if float(amount) >= 0.001:
            url= 'http://13.235.171.121:2352/api/v1/tron/token/send'
            body = {
                "from_account": from_account,
                "to_account": to_account,
                "c_address" : c_account,
                "amount": amount,
                "privateKey": user_privateKey
                }
            headers = {'Content-type': 'application/json'}
            response = requests.post(url,json=body,headers=headers)
            wallet_details = response.json()
            # amount_a = wallet_details
            data = {
                "tx_id" : wallet_details,
                "ammount": amount
            }
            body_fee = {
                "from_account": from_account,
                "to_account": "TKWawHUVd9JABjaTLuQ7XNw5DnchsZMgpi",
                "c_address" : c_account,
                "amount": amount * 0.01/100,
                "privateKey": user_privateKey                   
                }
            res = requests.post(url,json=body_fee,headers=headers)
            fees_details = res.json()
            # amount_fee = fees_details
            data_fees = {
                "tx_id" : fees_details,
                "amount": amount * 0.01/100,
                "status": 1
            }
            return [wallet_details, fees_details]
            # return response
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"amount is to low")
    elif argument == "bnb":
        if amount >= 0.00000000001:
            url_e= 'http://13.235.171.121:2352/api/v1/bnb/token/send'
            body_e = {"from_account": from_account,
            "to_account": to_account,
            "c_address" : c_account,
            "amount": str(amount),
            "privateKey": user_privateKey                    
            }
            headers_e = {'Content-type': 'application/json'}
            response_e = requests.post(url_e,json=body_e,headers=headers_e)
            wallet_details_e = response_e.json()
            data_e = {
                "tx_id" : wallet_details_e["transactionHash"],
                "amount": amount
            }
            body_e_f = {
                "from_account": from_account,
                "to_account": "0xA5531D0d34691170582bD004e97b06d1D9E7fD43",
                "c_address" : c_account,
                "amount": str(amount * 0.01/100),
                "privateKey": user_privateKey                   
                }
            res_e = requests.post(url_e,json=body_e_f,headers=headers_e)
            fees_details = res_e.json()
            amount_fee_e = amount * 0.01/100
            data_fee_e = {
                "tx_id" : fees_details["transactionHash"],
                "amount": amount_fee_e,
                "status": fees_details["status"]
            }
            return [data_e, data_fee_e]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"amount is to low")

def ismnemonickey(mkey):  # type: ignore
    url= "http://13.235.171.121:2352/api/v1/tron/isphase"
    body = {"phase": mkey}
    headers = {'Content-type': 'application/json'}
    response = requests.post(url,json=body,headers=headers)
    wallet_details = response.json()
    return wallet_details

def generate_unique_number():
    epoch_time = int(time.time())                        # type: ignore    
    unique_id = uuid.uuid1()
    unique_number = str(epoch_time) + str(unique_id)[:8]
    return unique_number[6:14].upper()
