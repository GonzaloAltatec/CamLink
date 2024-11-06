from fastapi import FastAPI
from .routers import reviser, erp_data, configurator, develop

app = FastAPI()

app.include_router(reviser.router)
app.include_router(erp_data.router)
#app.include_router(develop.router)
app.include_router(configurator.router)
