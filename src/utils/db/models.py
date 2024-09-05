#SQLAlchemy functions and 
from sqlalchemy import Column, ForeignKey, Integer, String
#Relational Keys function
from sqlalchemy.orm import relationship
#Local DB config
from .database import Base

class System(Base):
    __tablename__ = 'systems'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    elements = Column(String) #Field to save Device ID's

class Device(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    user = Column(String)
    password = Column(String)
    ip = Column(String)
    port = Column(Integer)
    #parent_system = Column(Integer, ForeignKey('systems.id')) #Parent system ID
    #system = relationship('System', back_populates='system')
