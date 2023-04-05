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
from web3 import Web3

from app.config.database import SessionLocal, engine
from app.models.index import DbToken, DbUser
from app.schemas.index import Assets, AssetsAdd, AssetsNetwork


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_new_token(request: AssetsAdd, db: Session = Depends(get_db)):
    # token = db.query(DbToken).all()
    # tok = ''
    # for tk in token:
    #     if tk.token_network == "trx":
    #         tok = "trc20"
    #     elif tk.token_network == "eth":
    #         tok= "erc20"
    #     else:
    #         tok = "bep20"
    #     db.query(DbToken).filter(DbToken.token_id == tk.token_id).update({"token_type": f'{tok}'}, synchronize_session='evaluate')
    #     db.commit()
    # return "done"
    if not request.token_contect_id == "TM4q3gujYR7JUaFrZpM8x1P7NbQd6hwJts" and not request.token_contect_id == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t":
        new_token = DbToken(
            token_name = request.token_name,
            token_short_name= request.token_short_name,
            token_contect_id = request.token_contect_id, 
            token_logo = request.token_logo,
            token_decimal = request.token_decimal,
            token_can_show = 1,
            token_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
            token_network= request.token_network,
            token_type = request.token_type
        )
        db.add(new_token)
        db.commit()
        token = db.query(DbToken).filter(DbToken.token_id == new_token.token_id).first()
        return token
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"token already added")

def create_user_token(request: Assets, db: Session = Depends(get_db)):
    token = db.query(DbToken).filter(DbToken.token_contect_id == request.token_contect_id).first()
    if not request.token_contect_id == "TM4q3gujYR7JUaFrZpM8x1P7NbQd6hwJts" and not request.token_contect_id == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t" and not token:
        url = 'https://apilist.tronscan.org/api/contract?contract='+request.token_contect_id    # type: ignore
        response = requests.get(url)  # type: ignore
        data = response.json()
        new_token = DbToken(
            token_name = data["data"][0]['tokenInfo']["tokenName"],
            token_short_name= data["data"][0]['tokenInfo']["tokenAbbr"],
            token_contect_id = data["data"][0]['tokenInfo']["tokenId"],
            token_logo = data["data"][0]['tokenInfo']["tokenLogo"],
            token_type = data["data"][0]['tokenInfo']["tokenType"],
            token_decimal = data["data"][0]['tokenInfo']["tokenDecimal"],
            token_can_show = data["data"][0]['tokenInfo']["tokenCanShow"],
            token_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
        )
        db.add(new_token)
        db.commit()
        user = db.query(DbUser).filter(DbUser.user_address == request.address).first()
        if user.user_token_id == None:             # type: ignore
            token = str(new_token.token_id)
        else:
            token = user.user_token_id+","+str(new_token.token_id)            # type: ignore
        db.query(DbUser).filter(DbUser.user_address == request.address).update({"user_token_id": f'{token}'}, synchronize_session='evaluate')
        db.commit()
        token = db.query(DbToken).filter(DbToken.token_id == new_token.token_id).first()
        return token
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"token already added")

def show_token(network: str, db: Session = Depends(get_db)):
    token = db.query(DbToken).filter(DbToken.token_network == network).all()
    
    return token

def add_token(request: AssetsNetwork, db: Session = Depends(get_db)):
    token = db.query(DbToken).filter(DbToken.token_contect_id == request.token_contect_id).first()
    user = db.query(DbUser).filter(DbUser.user_address == request.address).first()
    if user.user_network == token.token_network:       # type: ignore
        if user.user_token_id == None:             # type: ignore
            token = str(token.token_id)           # type: ignore
        else:
            token = user.user_token_id+","+str(token.token_id)            # type: ignore
        db.query(DbUser).filter(DbUser.user_address == request.address).update({"user_token_id": f'{token}'}, synchronize_session='evaluate')
        db.commit()
        return token
    else:
        return {"msg": "worng network"}

def token_all_transaction(address: str, c_address: str, db: Session = Depends(get_db)):
    url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        data.append(dt)
    return data

def token_send_transaction(address: str, c_address:str , db: Session = Depends(get_db)):
    url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["from"] == address:
            data.append(dt)
    return data

def token_receive_transaction(address: str, c_address: str, db: Session = Depends(get_db)):
    url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["to"] == address:
            data.append(dt)
    return data

def trx_all_transaction(address: str, start:str, db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["tokenInfo"]["tokenAbbr"] == "trx":
            if not 'trigger_info' in dt:
                transac = {
                "transaction_id": dt["hash"],
                "token_info": {
                    "symbol": "TRX",
                    "address": "",
                    "decimals": dt["tokenInfo"]["tokenDecimal"],
                    "name": "Tron"
                },
                "block_timestamp": dt["timestamp"],
                "from": dt["contractData"]["owner_address"],
                "to": dt["contractData"]["to_address"],
                "type": "Transfer",
                "value": str(dt["contractData"]["amount"])
                }
                data.append(transac)
    return data

def trx_send_transaction(address: str, start:str , db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["ownerAddress"] == address and dt["tokenInfo"]["tokenAbbr"] == "trx":
            if not 'trigger_info' in dt:
                transac = transac = {
                "transaction_id": dt["hash"],
                "token_info": {
                "symbol": "TRX",
                "address": "",
                "decimals": dt["tokenInfo"]["tokenDecimal"],
                "name": "Tron"
                },
                "block_timestamp": dt["timestamp"],
                "from": dt["contractData"]["owner_address"],
                "to": dt["contractData"]["to_address"],
                "type": "Transfer",
                "value": str(dt["contractData"]["amount"])
                }
                data.append(transac)
    return data

def trx_receive_transaction(address: str, start: str, db: Session = Depends(get_db)):
    url = 'https://apilist.tronscan.org/api/transaction?sort=-timestamp&count=true&limit=50&start='+start+'&address='+address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["toAddress"] == address and dt["tokenInfo"]["tokenAbbr"] == "trx":
            if not 'trigger_info' in dt:
                transac = transac = {
                "transaction_id": dt["hash"],
                "token_info": {
                "symbol": "TRX",
                "address": "",
                "decimals": dt["tokenInfo"]["tokenDecimal"],
                "name": "Tron"
                },
                "block_timestamp": dt["timestamp"],
                "from": dt["contractData"]["owner_address"],
                "to": dt["contractData"]["to_address"],
                "type": "Transfer",
                "value": str(dt["contractData"]["amount"])
                }
                data.append(transac)
    return data

def all_token_transaction(address: str, c_address: str, db: Session = Depends(get_db)):
    url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        data.append(dt)
    return data

def send_token_transaction(address: str, c_address:str , db: Session = Depends(get_db)):
    url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["from"] == address:
            data.append(dt)
    return data

def receive_token_transaction(address: str, c_address: str, db: Session = Depends(get_db)):
    url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
    response = requests.get(url)
    reacharge_responce = response.json()
    data = []
    for dt in reacharge_responce["data"]:
        if dt["to"] == address:
            data.append(dt)
    return data

def token_transaction_all(address: str, c_address:str, network: str, db: Session = Depends(get_db)):
    reacharge_responce = number_of_network_trans(network, address, c_address)
    return reacharge_responce

def token_transaction_send(address: str, c_address:str, network: str, db: Session = Depends(get_db)):
    reacharge_responce = number_of_network_trans_send(network, address, c_address)
    return reacharge_responce

def token_transaction_receive(address: str, c_address:str, network: str, db: Session = Depends(get_db)):
    reacharge_responce = number_of_network_trans_receive(network, address, c_address)
    return reacharge_responce

def create_user_token_network(request: AssetsNetwork, db: Session = Depends(get_db)):
    data = number_of_network_token_add(request.network, request.address, request.token_contect_id)
    return data
    # if not data.status_code == 404:      # type: ignore
        # new_token = DbToken(
        #     token_name = data["token_name"],              # type: ignore
        #     token_short_name= data["token_short_name"],   # type: ignore
        #     token_contect_id = data["token_contect_id"],  # type: ignore
        #     token_logo = data["token_logo"],              # type: ignore
        #     token_decimal = data["token_decimal"],        # type: ignore
        #     token_can_show = data["token_can_show"],      # type: ignore
        #     token_network = data["token_network"],        # type: ignore
        #     token_registration_date_time=datetime.now(pytz.timezone('Asia/Calcutta')),
        # )
        # db.add(new_token)
        # db.commit()
        # user = db.query(DbUser).filter(DbUser.user_address == request.address).first()
        # if user.user_token_id == None:             # type: ignore
        #     token = str(new_token.token_id)
        # else:
        #     token = user.user_token_id+","+str(new_token.token_id)            # type: ignore
        # db.query(DbUser).filter(DbUser.user_address == request.address).update({"user_token_id": f'{token}'}, synchronize_session='evaluate')
        # db.commit()
        # token = db.query(DbToken).filter(DbToken.token_id == new_token.token_id).first()
        # return token
    # else:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"token already added")





def number_of_network_trans(argument, address, c_address): 
    if argument =="trx":
        url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
        response = requests.get(url)
        reacharge_responce = response.json()
        data = []
        for dt in reacharge_responce["data"]:
            if dt["from"] == address:
                data.append(dt)
        return data
    elif argument == "eth":
        api_key = "4H9HPQ1GPGHIAG3D58Y4RPPI4AE6NGA4U8"
        url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&contractaddress={c_address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        if result["message"] == "OK":
            transactions = result["result"]
            return transactions
        else:
            return []

def number_of_network_trans_send(argument, address, c_address): 
    if argument =="trx":
        url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
        response = requests.get(url)
        reacharge_responce = response.json()
        data = []
        for dt in reacharge_responce["data"]:
            data.append(dt)
        return data
    elif argument == "eth":
        api_key = "4H9HPQ1GPGHIAG3D58Y4RPPI4AE6NGA4U8"
        url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&contractaddress={c_address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        if result["message"] == "OK":
            transactions = result["result"]
            return transactions
        else:
            return []

def number_of_network_trans_receive(argument, address, c_address): 
    if argument =="trx":
        url = 'https://api.trongrid.io/v1/accounts/'+address+'/transactions/trc20?limit=50&contract_address='+c_address
        response = requests.get(url)
        reacharge_responce = response.json()
        data = []
        for dt in reacharge_responce["data"]:
            if dt["to"] == address:
                data.append(dt)
        return data
    elif argument == "eth":
        api_key = "4H9HPQ1GPGHIAG3D58Y4RPPI4AE6NGA4U8"
        url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={address}&contractaddress={c_address}&sort=desc&apikey={api_key}"
        response = requests.get(url)
        result = response.json()
        if result["message"] == "OK":
            transactions = result["result"]
            return transactions
        else:
            return []

def number_of_network_token_add(argument, address, c_address): 
    if argument =="trx":
        if not c_address == "TM4q3gujYR7JUaFrZpM8x1P7NbQd6hwJts" and not c_address == "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t":
            url = 'https://apilist.tronscan.org/api/contract?contract='+request.token_contect_id    # type: ignore
            response = requests.get(url)  # type: ignore
            data = response.json()
            resp = {
                'token_name': data["data"][0]['tokenInfo']["tokenName"],
                'token_short_name': data["data"][0]['tokenInfo']["tokenAbbr"],
                'token_contect_id': data["data"][0]['tokenInfo']["tokenId"],
                'token_logo': data["data"][0]['tokenInfo']["tokenLogo"],
                'token_decimal': data["data"][0]['tokenInfo']["tokenDecimal"],
                'token_can_show': data["data"][0]['tokenInfo']["tokenCanShow"],
                'token_network': "trx"
            }   
            return resp
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"token already added")
    elif argument == "eth":
        if not c_address == "0xdAC17F958D2ee523a2206206994597C13D831ec7" and not c_address == "0xB8c77482e45F1F44dE1745F52C74426C631bDD52":
            w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/86a9285ab42b47ddbec539e3bec12d0a'))
            url = url = f'https://api.etherscan.io/api?module=contract&action=tokeninfo&address={c_address}&apikey=4H9HPQ1GPGHIAG3D58Y4RPPI4AE6NGA4U8'
            response = requests.get(url)
            result = response.json()
            abi = json.loads(result["result"])
            # if result["status"] == "1":
            contract = w3.eth.contract(address=c_address, abi=abi)
            # # print(contract)
            name = contract.functions.name().call()
            # symbol = contract.functions.symbol().call()
            # decimals = contract.functions.name()
            # logo_url = contract.functions.tokenURI(0).call()
            # response = requests.get(logo_url)
            # logo_image = response.content   
            # resp = {
            #     'token_name': name,
            #     'token_short_name': symbol,
            #     'token_contect_id': c_address,
            #     'token_logo': logo_image,
            #     'token_decimal': decimals,
            #     'token_can_show': 1,
            #     'token_network': "eth"
            # }
            return name
            # else:
            #     return []
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"token already added")