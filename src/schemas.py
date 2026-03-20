from pydantic import BaseModel
import datetime

class OilBase(BaseModel):
    date: datetime.date
    price: float

class CreateOilPrice(OilBase):
    pass

class OilPrice(OilBase):
    id: int
    class Config:
        orm_mode = True