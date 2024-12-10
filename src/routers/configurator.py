# FastAPI imports
from fastapi import APIRouter, status

# Database import
from ..utils.db import models
from ..utils.db.schemas import IDList

# Hikvision API operator
from ..utils.operations import Hikvision as Hik

router = APIRouter(tags=["configurator"], prefix="/configure")


def device_name(device: dict):
    api = Hik(device["ip"], device["password"])
    conf = api.putname(device["name"])
    return conf


@router.post("/", status_code=status.HTTP_200_OK)
def configure(id_list: IDList):
    for id in id_list.ids:
        device = models.device(id)
        if device != "Error" and device is not None:
            name_conf = device_name(device)

            return {"response": name_conf}
