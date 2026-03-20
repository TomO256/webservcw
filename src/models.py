from sqlalchemy import *
from . import db

class OilPrice(db.Base):
    __tablename__ = "oil_prices"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)


class GeoEvent(db.Base):
    __tablename__ = "geo_events"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    event_type = Column(String, nullable=True)
    event_description = Column(String, nullable=True)
    event_severity = Column(Integer, nullable=True)
    event_flag = Column(Integer, nullable=True)
