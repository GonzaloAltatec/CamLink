from fastapi import FastAPI, Depends, HTTPException, status
from .utils.db import models, schemas
from .utils.db.database import engine, get_db
from .routers import reviser, erp_data

app = FastAPI()

#DB Creation
models.Base.metadata.create_all(engine)

app.include_router(reviser.router)
app.include_router(erp_data.router)
