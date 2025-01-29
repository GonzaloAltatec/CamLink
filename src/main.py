from fastapi import FastAPI
from .routers import reviser, configurator

app = FastAPI()


@app.get("/", status_code=200)
def root():
    return {"details": "API Online"}


app.include_router(reviser.router)
app.include_router(configurator.router)
