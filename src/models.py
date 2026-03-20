from sqlalchemy import *
from .db import Base

class OilPrice(Base):
    __tablename__ = "oil_prices"
    id = Column(Integer,primary_key=True,index=True)
    date = Column(Date,nullable=False)
    price = Column(Float,nullable=False)
    event_type = Column(String,nullable=True)
    event_description=Column(String,nullable=True)
    event_severity=Column(Integer,nullable=True)
    event_flag=Column(Integer,nullable=True)