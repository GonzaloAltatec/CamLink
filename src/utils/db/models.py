#SQLAlchemy functions and 
from sqlalchemy import Column, Integer, String
#Local DB config
from .database import Base

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    installation = Column(String)
    user = Column(String)
    password = Column(String)
    ip = Column(String)
    port = Column(Integer)
    model = Column(String) #Optional field to fill with device model
