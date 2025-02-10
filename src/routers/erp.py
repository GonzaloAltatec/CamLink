# Local libreries import
from src.utils.odoo import Odoo

# FastAPI imports
from fastapi import APIRouter, status

# Router endpoint definition
router = APIRouter(tags=["erp"], prefix="/erp")
