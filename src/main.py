from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import datetime

from . import schemas, crud, models,db

db.Base.metadata.create_all(bind=db.engine)
app = FastAPI(title="Oil Price Tracker")

def get_db():
    dbtemp =db.SessionLocal()
    try:
        yield dbtemp
    finally:
        dbtemp.close()

@app.post("/prices", response_model=schemas.OilPrice, status_code=201)
def create_price(record: schemas.OilPrice, db: Session = Depends(get_db)):
    return crud.create_price(db,record)

@app.get("/prices",response_model=list[schemas.OilPrice])
def list_prices(db: Session = Depends(get_db)):
    return crud.read_all_price(db)

@app.get("/prices/{id}",response_model=schemas.OilPrice)
def get_price(id: int, db: Session = Depends(get_db)):
    row = crud.read_one_price(db,id)
    if not row:
        raise HTTPException(404, "Record not Found")
    return row

@app.put("/prices/{id}",response_model=schemas.OilPrice)
def update_price(id: int, record: schemas.CreateOilPrice, db: Session = Depends(get_db)):
    update = crud.update_price(db,id,record)
    if not update:
        raise HTTPException(404, "Record not Found")
    return update

@app.delete("/prices/{id}",status_code=204)
def delete_price(id: int, db: Session = Depends(get_db)):
    delete = crud.delete_price(db,id)
    if not delete:
        raise HTTPException(404, "Record not Found")
    return None

@app.get("/prices/filter",response_model=list[schemas.OilPrice],tags=["Prices"])
def filter_prices(start:Optional[datetime.date]=None,end:Optional[datetime.date]=None,mini:Optional[float]=None,maxi:Optional[float]=None,db:Session=Depends(get_db)):
    return crud.filter_prices(db,start,end,mini,maxi)
