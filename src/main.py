from fastapi import FastAPI, Depends, HTTPException,Response
from sqlalchemy.orm import Session
from typing import Optional
import datetime

from . import schemas, crud, models,db

db.Base.metadata.create_all(bind=db.engine)
app = FastAPI(title="Oil Price Tracker",
              description="API tracking oil prices and geopolitical events influencing them",
              openapi_tags=[{"name":"Prices","description":"Oil Price Data"},
                             {"name":"Analytics","description":"Statistics from the Oil Data"},
                             {"name":"Events","description":"Geopolitical Event Data"}])

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

@app.get("/prices/sort",response_model=list[schemas.OilPrice],tags=["Prices"])
def sort_prices(sort_by:str="date",order:str="asc",db:Session=Depends(get_db)):
    result = crud.sort_prices(db,sort_by,order)
    if result is None:
        raise HTTPException(300, "Invalid Sort Option")
    return result

### Event Stats

@app.get("/events",tags=["Events"])
def list_events(db:Session = Depends(get_db)):
    return db.query(models.OilPrice.filter(models.OilPrice.event_flag==1)).all()

@app.get("/events/type",tags=["Events"])
def event_type(type:str,db:Session=Depends(get_db)):
    return db.query(models.OilPrice).filter(models.OilPrice.event_type==type).all()

## Analytics

@app.get("/analytics/average",tags=["Analytics"])
def average_price(db:Session=Depends(get_db)):
    return {"average_price": crud.get_avg_price(db)}

@app.get("/analytics/max",tags="Analytics")
def max_price(db:Session=Depends(get_db)):
    return {"maximum_price":crud.get_max_price(db)}

@app.get("analytics/min",tags=["Analytics"])
def min_price(db:Session=Depends(get_db)):
    return {"minimum_price":crud.get_min_price(db)}


#Overall error handler

@app.exception_handler(Exception)
def main_exception(request,exc):
    return Response.JSONResponse(status_code=500,content={"error":"Internal Server Error","details":str(exc)})