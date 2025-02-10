# Local libreries import
from src.utils.odoo import Odoo
from src.utils.operations import Hikvision as Hik

from src.utils.db import models

# FastAPI imports
from fastapi import APIRouter, status

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
