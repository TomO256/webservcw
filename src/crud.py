from sqlalchemy import Session

import models, schemas
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
def update_price(db: Session, id: int, record: schemas.OilPriceCreate):
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



