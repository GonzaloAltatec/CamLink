from pydantic import BaseModel, ConfigDict
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

    Config: ConfigDict = {
        'from_attributes': True
    }

class IDList(BaseModel):
    ids: List[int]
