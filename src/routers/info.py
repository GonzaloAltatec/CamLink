# Local libreries import
from src.utils.odoo import Odoo
from src.utils.operations import Hikvision as Hik

from src.utils.db import models

# FastAPI imports
from fastapi import APIRouter, status

# XML Parser
import xml.etree.ElementTree as ET

# Router endpoint definition
router = APIRouter(tags=["info"], prefix="/info")

# Enable Odoo client
client = Odoo()


# Read SD status
@router.get("/sd", status_code=status.HTTP_200_OK)
async def sd_info(id: int):
    device = models.device(id)
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        req = api.getsd()
        return req


# Read FW version
@router.get("/firmware", status_code=status.HTTP_200_OK)
async def fw_info(id: int):
    device = models.device(id)
    if device is not None and isinstance(device, dict):
        api = Hik(device["ip"], device["password"])
        req = api.info()
        return req


# Read NVR Data
@router.get("/nvr", status_code=status.HTTP_200_OK)
async def nvr_info(id: int):
    device_list = client.sys_nvr(id)
    device_info_list = []

    if device_list is not None and isinstance(device_list, list):
        for device in device_list:
            api = Hik(device["host"], device["password"])
            req = api.info()
            if req is not None and isinstance(req, str):
                root = ET.ElementTree(ET.fromstring(req))

                name_tag = root.find(
                    "ns:deviceName", {"ns": "http://www.hikvision.com/ver20/XMLSchema"}
                )
                name_text = name_tag.text if name_tag is not None else None

                firmware_tag = root.find(
                    "ns:firmwareVersion",
                    {"ns": "http://www.hikvision.com/ver20/XMLSchema"},
                )
                firmware_text = firmware_tag.text if firmware_tag is not None else None

                build_tag = root.find(
                    "ns:firmwareReleasedDate",
                    {"ns": "http://www.hikvision.com/ver20/XMLSchema"},
                )
                build_text = build_tag.text if build_tag is not None else None

                model_tag = root.find(
                    "ns:model", {"ns": "http://www.hikvision.com/ver20/XMLSchema"}
                )
                model_text = model_tag.text if model_tag is not None else None

                device_dict = {
                    "device": name_text,
                    "data": {
                        "firmware": f"{firmware_text} {build_text}",
                        "model": model_text,
                    },
                }

                device_info_list.append(device_dict)
    return device_info_list
