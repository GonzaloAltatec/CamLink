#FastAPI imports
from fastapi import APIRouter, Depends, HTTPException, Response, status
#SQLAlchemy Session import
from sqlalchemy.orm import Session
#Local Odoo library
from ..utils.odoo import Odoo
#Database import
from ..utils.db import schemas, models, database

router = APIRouter(
    tags=['erp-data'],
    prefix='/erp-data'
)

#ENDPOINT: Recive Odoo element ID and read it's properties
@router.post('/{id}/', status_code=status.HTTP_200_OK)
def create_device(id:int, request:schemas.Device, db:Session = Depends(database.get_db)):
    #Send element ID to Odoo Class
    erp = Odoo(id)
    #Get element properties
    properties_ids = erp.element_ids()

    #Read all property ID's
    for ids in properties_ids:
        data = erp.element_data(ids)

    #Creating a list for key-value pairs
    key_lst = []
    val_lst = []

    #Reading data and appending 'name' and 'value' field to lists
    for x in data:
        key_lst.append(x['name'])
        val_lst.append(x['valor'])

    #Creating a dictionary using 'zip' with our 2 lists
    device_data = dict(zip(key_lst, val_lst))

    #Give Odoo data to Device Model
    new_device = models.Device(id=id, 
                               name=device_data['NOMBRE'],
                               user=device_data['USUARIO'],
                               password=device_data['PASSWORD'],
                               ip=device_data['DIRECCION IP'],
                               port=int(device_data['PUERTO HTTP']),
                               )
    #Make changes on the DB
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return(new_device)
