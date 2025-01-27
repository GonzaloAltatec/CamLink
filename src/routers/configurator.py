# FastAPI imports
from fastapi import APIRouter, status

from src.utils.db.schemas import IDList

# Database import
from src.utils.db import models

# Hikvision API operator
from src.utils.operations import Hikvision as Hik

# import inspect

router = APIRouter(tags=["configurator"], prefix="/configure")


@router.post("/name", status_code=status.HTTP_200_OK)
async def device_name(id_list: IDList):
    for id in id_list.ids:
        device = models.device(id)
        if device != "Error" and device is not None:
            api = Hik(device["ip"], device["password"])
            conf = api.putname(device["name"])
            return conf


@router.post("/time", status_code=status.HTTP_200_OK)
async def device_time(id_list: IDList):
    for id in id_list.ids:
        device = models.device(id)
        if device != "Error" and device is not None:
            api = Hik(device["ip"], device["password"])
            conf = api.putime()
            return conf


@router.post("/osd", status_code=status.HTTP_200_OK)
async def device_osd(id_list: IDList):
    for id in id_list.ids:
        device = models.device(id)
        if device != "Error" and device is not None:
            api = Hik(device["ip"], device["password"])
            conf = api.putosd(device["name"])
            return conf
