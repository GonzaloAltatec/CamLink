from fastapi import FastAPI
from src.routers import develop
from .routers import reviser, erp_data

app = FastAPI()

app.include_router(reviser.router)
app.include_router(erp_data.router)
app.include_router(develop.router)
