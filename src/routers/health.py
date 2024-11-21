#FastAPI imports
from fastapi import APIRouter, status
#Event logger
import logging

logging.basicConfig(level=logging.ERROR)

router = APIRouter(
    tags=['health'],
    prefix='/health'
)


