# Local libreries import
from src.utils.odoo import Odoo

# FastAPI imports
from fastapi import APIRouter, status

# Router endpoint definition
router = APIRouter(tags=["erp"], prefix="/erp")

# Enable Odoo client
client = Odoo()


# Get elements from Odoo system
@router.get("/system", status_code=status.HTTP_200_OK)
async def system_data(id: int):
    req = client.sys_req(id)
    return req


# Get NVR Odoo data
@router.get("/nvr", status_code=status.HTTP_200_OK)
async def system_nvr(id: int):
    req = client.sys_nvr(id)
    return req
