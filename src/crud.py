from sqlalchemy.orm import Session
import sqlalchemy
import datetime

from . import models, schemas
#Create
def create_price(db: Session, record: schemas.CreateOilPrice):
    row = models.OilPrice(**record.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

#Read
def read_all_price(db: Session):
    return db.query(models.OilPrice).all()

def read_one_price(db: Session, id: int):
    return db.query(models.OilPrice).filter(models.OilPrice.id==id).first()

# Update
def update_price(db: Session, id: int, record: schemas.CreateOilPrice):
    row = read_one_price(db,id)
    if not row:
        return
    for v, i in record.dict().items():
        setattr(row,v,i)
    db.commit()
    db.refresh(row)
    return row

# Delete
def delete_price(db: Session, id: int):
    row = read_one_price(db,id)
    if not row:
        return
    db.delete(row)
    db.commit()
    return True

# Filter
def filter_prices(db: Session, start:datetime.date | None = None, end:datetime.date | None=None, mini:float|None=None, maxi:float |None=None):
    query = db.query(models.OilPrice)
    if start:
        query = query.filter(models.OilPrice.date >=start)
    if end:
        query = query.filter(models.OilPrice.date <=end)
    if mini:
        query = query.filter(models.OilPrice.price >=mini)
    if maxi:
        query = query.filter(models.OilPrice.price <=maxi)
    return query.all()


def sort_prices(db: Session, sort_by: str = "date", order: str = "asc"):
    column = getattr(models.OilPrice, sort_by, None)
    if not column:
        return None
    if order == "desc":
        return db.query(models.OilPrice).order_by(sqlalchemy.desc(column)).all()
    return db.query(models.OilPrice).order_by(sqlalchemy.asc(column)).all()

### Analytics

def get_avg_price(db:Session):
    return db.query(sqlalchemy.func.avg(models.OilPrice.price)).scalar()

def get_max_price(db:Session):
    return db.query(sqlalchemy.func.max(models.OilPrice.price)).scalar()

def get_min_price(db:Session):
    return db.query(sqlalchemy.func.min(models.OilPrice.price)).scalar()