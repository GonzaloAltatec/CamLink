#FastAPI imports
from fastapi import APIRouter, Depends, HTTPException, Response, status
#SQLAlchemy Session import
from sqlalchemy.orm import Session
#Local Odoo library
from ..utils.odoo import Odoo
#Database import
from ..utils.db import schemas, models, database
#Operations module
from ..utils.operations import Hikvision as Hik

router = APIRouter(
    tags=['erp-data'],
    prefix='/erp-data'
)

#ENDPOINT: Recive Odoo element ID and read it's properties
def create_device(id:int, request:schemas.Device, db:Session = Depends(database.get_db)):
    #Send element ID to Odoo Class
    erp = Odoo(id)
    #Get element properties
    properties_ids = erp.element_ids()

    #Read all property ID's
    for ids in properties_ids:
        data = erp.element_data(ids)

    #Read System from element
    sys_name = erp.element_sys()

    #Creating a list for key-value pairs
    key_lst = []
    val_lst = []

    #Reading data and appending 'name' and 'value' field to lists
    for x in data:
        key_lst.append(x['name'])
        val_lst.append(x['valor'])

    #Creating a dictionary using 'zip' with our 2 lists
    device_data = dict(zip(key_lst, val_lst))

    #Requesting device model
    try:
        conf = Hik(device_data['DIRECCION IP'], device_data['PASSWORD'])
        device_model = conf.getmodel()
    except Exception:
        return "ERROR: Device Offline"

    #Give Odoo data to Device Model
    new_device = models.Device(id=id, 
                               name=device_data['NOMBRE'],
                               installation=sys_name,
                               user=device_data['USUARIO'],
                               password=device_data['PASSWORD'],
                               ip=device_data['DIRECCION IP'],
                               port=int(device_data['PUERTO HTTP']),
                               model=device_model
                               )
    #Make changes on the DB
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return(new_device)
