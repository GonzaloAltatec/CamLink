from pydantic import BaseModel
from typing import List

class SystemBase(BaseModel):
    name: str

class System(SystemBase):
    id: int
    elements: List[int] = []

    model_config = {
        "from_attributes": True
    }

class DeviceBase(BaseModel):
    name: str
    parent_system: int

class Device(DeviceBase):
    id: int

    model_config = {
        "from_attributes": True
    }
