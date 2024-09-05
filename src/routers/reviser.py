#FastAPI imports
from fastapi import APIRouter, Depends, HTTPException, Response, status
#Typing functions
from typing import List
#SQLAlchemy Session import
from sqlalchemy.orm import Session
#Local libraries imports
from ..utils import comunication
#Database import
from ..utils.db import schemas, models, database
#Hikvision API operator
from ..utils.cconfig import Hikvision as Hik

router = APIRouter(
    tags=['reviser'],
    prefix='/revise'
)

@router.get('/{id}/db-info', status_code=status.HTTP_200_OK)
def db_info(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return device

@router.get('/{id}/info', status_code=status.HTTP_200_OK)
def info(id:int, db:Session=Depends(database.get_db)):
    device = db.query(models.Device).filter(models.Device.id == id).first()
    if not device:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    conf = Hik(device.ip, device.password)
    return(conf.info())
