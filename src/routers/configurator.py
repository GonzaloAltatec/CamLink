# FastAPI imports
from fastapi import APIRouter, status

# Models import
from src.utils.db import models
from src.utils.db.schemas import IDList

# Hikvision API operator
from src.utils.operations import Hikvision as Hik

router = APIRouter(tags=["configurator"], prefix="/configure")


# Get device info as dictionary
async def device_dict(id):
    device = models.device(id)
    if device != "Error" and device is not None and isinstance(device, dict):
        return device


# Configure device name
@router.post("/name", status_code=status.HTTP_200_OK)
async def device_name(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putname(device["name"])
            return conf


# Configure device time and DST operations
@router.post("/time", status_code=status.HTTP_200_OK)
async def device_time(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putime()
            return conf


# Configure OSD
@router.post("/osd", status_code=status.HTTP_200_OK)
async def device_osd(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putosd(device["name"])
            return conf


# Configure mail data
@router.post("/mail", status_code=status.HTTP_200_OK)
async def device_mail(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putmail(device["name"], device["installation"])
            return conf


# Configure security options
@router.post("/security", status_code=status.HTTP_200_OK)
async def device_security(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putsec()
            return conf


# Configure Network settings
@router.post("/network", status_code=status.HTTP_200_OK)
async def device_network(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putnet()
            return conf


# Configure Video settings
@router.post("/video", status_code=status.HTTP_200_OK)
async def device_video(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        conf_status = []
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putvideo(device["name"])
            conf_status.append(conf)
        return conf_status


# Configure Event settings
@router.post("/event", status_code=status.HTTP_200_OK)
async def device_event(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        conf_status = []
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putevents()
            conf_status.append(conf)
        return conf_status
