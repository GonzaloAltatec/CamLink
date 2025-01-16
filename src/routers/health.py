# FastAPI imports
from fastapi import APIRouter

# Event logger
import logging

logging.basicConfig(level=logging.ERROR)

router = APIRouter(tags=["health"], prefix="/health")
