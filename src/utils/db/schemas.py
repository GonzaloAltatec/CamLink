from pydantic import BaseModel
from typing import List

class Device(BaseModel):
    id: int
    name: str
    installation: str
    user: str
    password: str
    ip: str
    port: int
    model: str

    class Config:
        from_attributes = True

class IDList(BaseModel):
    ids: List[int]
