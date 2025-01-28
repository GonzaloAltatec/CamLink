# FastAPI imports
from fastapi import APIRouter, status

# Models import
from src.utils.db import models
from src.utils.db.schemas import IDList

# Hikvision API operator
from src.utils.operations import Hikvision as Hik

router = APIRouter(tags=["configurator"], prefix="/configure")


async def device_dict(id):
    device = models.device(id)
    if device != "Error" and device is not None and isinstance(device, dict):
        return device


@router.post("/name", status_code=status.HTTP_200_OK)
async def device_name(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putname(device["name"])
            return conf


@router.post("/time", status_code=status.HTTP_200_OK)
async def device_time(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putime()
            return conf


@router.post("/osd", status_code=status.HTTP_200_OK)
async def device_osd(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putosd(device["name"])
            return conf


@router.post("/mail", status_code=status.HTTP_200_OK)
async def device_mail(id_list: IDList):
    for id in id_list.ids:
        device = await device_dict(id)
        if device is not None and isinstance(device, dict):
            api = Hik(device["ip"], device["password"])
            conf = api.putmail(device["name"], device["installation"])
            return conf
