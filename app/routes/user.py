from datetime import datetime
from typing import List, Optional

import pytz
from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     WebSocket, responses, status)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm.session import Session

from app.config.database import SessionLocal, engine
from app.models.index import DbUser
from app.oprations.index import (backup_wallet_phase, backup_wallet_private,
                                 change_pass, change_tok, create_new_wallet,
                                 create_wallet, details_all_wallet,
                                 details_wallet, details_wallet_bal,
                                 import_eth_wallet, import_wallet,
                                 network_wallet_bal, random_number, send_all,
                                 send_trx, show_all_note_transaction,
                                 show_all_receive_transaction,
                                 show_all_send_transaction,
                                 show_all_transaction, show_note_transaction,
                                 show_receive_transaction,
                                 show_send_transaction, show_transaction,
                                 show_user_network_wallet, show_user_wallet,
                                 varify_pass, wallet_delete, wallet_update,
                                 wallet_update_all)
from app.schemas.index import (ImportWallet, ImportWalletAll, User, UserNew,
                               WalletDetails, WalletDetailsAll, deleteWallet,
                               liveprice, passChange, passVarify, sendAll,
                               sendTron, updateWallet, updateWalletAll)

user = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user.post('/wallet/import', status_code=status.HTTP_201_CREATED)
def importEthWallet(request: ImportWalletAll, db: Session = Depends(get_db)):
    return import_eth_wallet(request, db )

@user.post('/tron/wallet/gen', status_code=status.HTTP_201_CREATED)
def createWallet(request: User, db: Session = Depends(get_db)):
    return create_new_wallet(request,db)
    
@user.post('/tron/wallet/import', status_code=status.HTTP_201_CREATED)
def importWallet(request: ImportWallet, db: Session = Depends(get_db)):
    return import_wallet(request, db ) # type: ignore

@user.post('/tron/wallet/details', status_code=status.HTTP_200_OK)
def detailsWallet(request: WalletDetails, db: Session = Depends(get_db)):
    return details_wallet(request, db)  # type: ignore

@user.post('/wallet/details', status_code=status.HTTP_200_OK)
def detailsWalletAll(request: WalletDetailsAll, db: Session = Depends(get_db)):
    return details_all_wallet(request, db)  # type: ignore

@user.post('/tron/wallet/balance', status_code=status.HTTP_200_OK)
def detailsWalletBal(request: WalletDetails, db: Session = Depends(get_db)):
    return details_wallet_bal(request, db)  # type: ignore

@user.get('/user/wallet/{hash_id}/', status_code=status.HTTP_200_OK)
def Userwallet(hash_id: str, db: Session = Depends(get_db)):  
    return show_user_wallet(hash_id, db)           

@user.post('/tron/send', status_code=status.HTTP_200_OK)
def sendTrx(request: sendTron, db: Session = Depends(get_db)):  
    return send_trx(request, db)  

@user.get('/transaction/all/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionAll(address: str, start:str, db: Session = Depends(get_db)):
    return show_all_transaction(address, start, db)  

@user.get('/transaction/send/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionSend(address: str, start:str, db: Session = Depends(get_db)):
    return show_send_transaction(address, start, db)  

@user.get('/transaction/receive/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionReceive(address: str, start:str, db: Session = Depends(get_db)):
    return show_receive_transaction(address, start, db)  

@user.get('/transaction/note/{address}/{start}', status_code=status.HTTP_200_OK)
def transactionNote(address: str, start:str, db: Session = Depends(get_db)):
    return show_note_transaction(address, start, db) 

@user.post('/verify/pass', status_code=status.HTTP_200_OK)
def varifyPass(request: passVarify, db: Session = Depends(get_db)):  
    return varify_pass(request, db)  

@user.post('/change/pass', status_code=status.HTTP_202_ACCEPTED)
def changePass(request: passChange, db: Session = Depends(get_db)):  
    return change_pass(request, db)

@user.post('/wallet/update', status_code=status.HTTP_202_ACCEPTED)
def walletUpdate(request: updateWallet, db: Session = Depends(get_db)):  
    return wallet_update(request, db)

@user.post('/wallet/update/all', status_code=status.HTTP_202_ACCEPTED)
def walletUpdateAll(request: updateWalletAll, db: Session = Depends(get_db)):  
    return wallet_update_all(request, db)

@user.post('/wallet/backup', status_code=status.HTTP_200_OK)
def WalletBackup(request: WalletDetails, db: Session = Depends(get_db)):
    return backup_wallet_private(request, db)  # type: ignore

@user.post('/wallet/backup/phase', status_code=status.HTTP_200_OK)
def WalletBackupPhase(request: WalletDetails, db: Session = Depends(get_db)):
    return backup_wallet_phase(request, db)  # type: ignore

@user.post('/wallet/delete', status_code=status.HTTP_202_ACCEPTED)
def walletDelete(request: deleteWallet, db: Session = Depends(get_db)):  
    return wallet_delete(request, db)

@user.post('/wallet/gen', status_code=status.HTTP_201_CREATED)
def createEthWallet(request: UserNew, db: Session = Depends(get_db)):
    return create_wallet(request,db)

@user.get('/user/wallet/{hash_id}/{network}', status_code=status.HTTP_200_OK)
def UserAllwallet(hash_id: str, network:str, db: Session = Depends(get_db)):  
    return show_user_network_wallet(hash_id, network, db) 

@user.post('/all/send', status_code=status.HTTP_200_OK)
def sendAllToken(request: sendAll, db: Session = Depends(get_db)):  
    return send_all(request, db)

@user.get('/change/tok', status_code=status.HTTP_202_ACCEPTED)
def changetok(db: Session = Depends(get_db)):  
    return change_tok(db)

@user.get('/all/transaction/{address}/{network}', status_code=status.HTTP_200_OK)
def transaction(address: str, network: str, db: Session = Depends(get_db), start: str = None):              # type: ignore 
    return show_transaction(address, network, db, start)  

@user.get('/send/transaction/{address}/{network}', status_code=status.HTTP_200_OK)
def transactionAllSend(address: str, network: str, db: Session = Depends(get_db), start: str = None):           # type: ignore 
    return show_all_send_transaction(address, network, db, start)  

@user.get('/receive/transaction/{address}/{network}', status_code=status.HTTP_200_OK)
def transactionAllReceive(address: str, network: str, db: Session = Depends(get_db), start: str = None):            # type: ignore 
    return show_all_receive_transaction(address, network, db, start) 

@user.get('/note/transaction/{address}/{network}', status_code=status.HTTP_200_OK)
def transactionNoteReceive(address: str, network: str, db: Session = Depends(get_db), start: str = None):            # type: ignore 
    return show_all_note_transaction(address, network, db, start) 

@user.post('/all/wallet/balance', status_code=status.HTTP_200_OK)
def allWalletBal(request: WalletDetailsAll, db: Session = Depends(get_db)):
    return network_wallet_bal(request, db)  # type: ignore

@user.get('/random/{number}', status_code=status.HTTP_200_OK)
def randomNumber(number: int, db: Session = Depends(get_db)):            # type: ignore 
    return random_number(number, db) 