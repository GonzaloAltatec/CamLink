from typing import Optional
from pydantic import BaseModel

class Device(BaseModel):
    id: int
    name: str
    installation: str
    user: str
    password: str
    ip: str
    port: int
    model: Optional[str]

    class Config:
        from_attributes = True
