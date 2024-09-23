from fastapi import FastAPI
from src.routers import develop
from .utils.db import models
from .utils.db.database import engine
from .routers import reviser, erp_data

app = FastAPI()

#DB Creation
models.Base.metadata.create_all(engine)

app.include_router(reviser.router)
app.include_router(erp_data.router)
app.include_router(develop.router)
