# FastAPI imports
from fastapi import APIRouter, status

# Database import
from ..utils.db import models
from ..utils.db.schemas import IDList

# Hikvision API operator
from ..utils.operations import Hikvision as Hik

import inspect

router = APIRouter(tags=["configurator"], prefix="/configure")


async def device_name(device: dict):
    api = Hik(device["ip"], device["password"])
    conf = api.putname(device["name"])
    return conf


@router.post("/", status_code=status.HTTP_200_OK)
async def configure(id_list: IDList):
    for id in id_list.ids:
        device = models.device(id)
        if device != "Error" and device is not None:
            name_conf = device_name(device)

            # Module reading
            current_module = inspect.getmodule(inspect.currentframe())
            functions = dict(
                inspect.getmembers(current_module, inspect.iscoroutinefunction)
            )
            # Listing function names
            excecution_order = [
                "device_name",
                "device_ntp",
                "device_dst",
                "device_security",
                "device_dns",
                "device_mail",
                "device_mstream",
                "device_sstream",
                "device_osd",
                "device_overlay",
                "device_motion",
                "device_record",
                "device_sderror",
                "device_access",
                "device_quota",
                "device_sd",
                "device_calendar",
            ]

            # Loop to execute all functions inside this module
            for func_name in excecution_order:
                if func_name in functions:
                    result = await functions[func_name](device)
                    key = func_name.split("_")[1]
                    # if key in parameters["report"]:
                    #    parameters["report"][key] = result

            return {"response": name_conf}
