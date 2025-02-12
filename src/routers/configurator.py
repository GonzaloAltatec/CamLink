# FastAPI imports
from fastapi import APIRouter, BackgroundTasks, status

# Models import
from src.utils.db import models
from src.utils.db.schemas import IDList

# Hikvision API operator
from src.utils.operations import Hikvision as Hik

# Custom Exceptions
from src.utils.exceptions import (
    DeviceConnectionError,
    DeviceRequestError,
    DeviceTimeoutError,
)

# Event logger
import logging
import inspect

logging.basicConfig(level=logging.ERROR)

# Router endpoint definition
router = APIRouter(tags=["configurator"], prefix="/configure")


## Get device info as dictionary
async def device_dict(id):
    device = models.device(id)
    if device != "Error" and device is not None and isinstance(device, dict):
        return device


# Configure device name
@router.post("/name", status_code=status.HTTP_200_OK)
async def device_name(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.putname(device["name"])
        conf_status.append(conf)
    return conf_status


# Configure device time and DST operations
@router.post("/time", status_code=status.HTTP_200_OK)
async def device_time(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.putime()
        conf_status.append(conf)
    return conf_status


# Configure OSD
@router.post("/osd", status_code=status.HTTP_200_OK)
async def device_osd(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.putosd(device["name"])
        conf_status.append(conf)
    return conf_status


# Configure mail data
@router.post("/mail", status_code=status.HTTP_200_OK)
async def device_mail(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.putmail(device["name"], device["installation"])
        conf_status.append(conf)
    return conf_status


# Configure security options
@router.post("/security", status_code=status.HTTP_200_OK)
async def device_security(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.putsec()
        conf_status.append(conf)
    return conf_status


# Configure Network settings
@router.post("/dns", status_code=status.HTTP_200_OK)
async def device_dns(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.putnet()
        conf_status.append(conf)
    return conf_status


# Configure Video settings
@router.post("/video", status_code=status.HTTP_200_OK)
async def device_video(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.putvideo(device["name"])
        conf_status.append(conf)
    return conf_status


# Configure Event settings
@router.post("/event", status_code=status.HTTP_200_OK)
async def device_event(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.putevents()
        conf_status.append(conf)
    return conf_status


# Configure Exception settings
@router.post("/exception", status_code=status.HTTP_200_OK)
async def device_exception(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.putexcepts()
        conf_status.append(conf)
    return conf_status


# Configure Schedule settings
@router.post("/calendar", status_code=status.HTTP_200_OK)
async def device_calendar(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.putschedule()
        conf_status.append(conf)
    return conf_status


# Configure SD
@router.post("/sd", status_code=status.HTTP_200_OK)
async def device_sd(id_list: IDList, background_tasks: BackgroundTasks):
    async def safe_formatter_sd(api: Hik):
        try:
            await api.sd_formatter()
        except Exception as e:
            print(f"Error en {api.ip}: {str(e)}")

    for device_id in id_list.ids:
        device = await device_dict(device_id)
        # conf_status = []
        if device is not None and isinstance(device, dict):
            print(f"formateando dispositivo: {id}")
            api = Hik(device["ip"], device["password"])
            background_tasks.add_task(safe_formatter_sd, api)
            # conf_status.append(conf)
    return {"status": "formatting"}


# Reboot
@router.post("/reboot", status_code=status.HTTP_200_OK)
async def device_reboot(id: int):
    device = await device_dict(id)
    conf_status = []
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        conf = api.reboot()
        conf_status.append(conf)
    return conf_status


# Batch configuration
@router.post("/", status_code=status.HTTP_200_OK)
async def configure(id_list: IDList):
    configurations = []
    for id in id_list.ids:
        try:
            # Module reading
            current_module = inspect.getmodule(inspect.currentframe())
            functions = dict(
                inspect.getmembers(current_module, inspect.iscoroutinefunction)
            )

            # Listing function names
            excecution_order = [
                "device_name",
                "device_time",
                "device_osd",
                "device_mail",
                "device_security",
                "device_dns",
                "device_video",
                "device_event",
                "device_exception",
                "device_calendar",
                # "device_sd",
                # "device_reboot",
            ]

            # Loop to execute all functions inside this module
            for func_name in excecution_order:
                if func_name in functions:
                    result = await functions[func_name](id)
                    configurations.append(result)

        except DeviceConnectionError as e:
            logging.error(f"Connection Error: {e}")
            configurations.append({"id": str(id), "details": "Device connection Error"})
        except DeviceTimeoutError as e:
            logging.error(f"Timeout Error: {e}")
            configurations.append(
                {"id": str(id), "details": "Timeout comunication Error"}
            )
        except DeviceRequestError as e:
            logging.error(f"Request Error: {e}")
            configurations.append({"id": str(id), "details": f"Request Error: {e}"})

    return configurations
