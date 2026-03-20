import os
import hmac
import hashlib
import time
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import datetime

from . import schemas, crud, models, db

# Use environment vars to get API keys
API_KEY = os.getenv("API_KEY", "dev-api-key")
API_SECRET = os.getenv("API_SECRET", "dev-secret-key") 

RATE_LIMIT = {}
MAX_REQUESTS = 30
WINDOW_SECONDS = 60


db.Base.metadata.create_all(bind=db.engine)

app = FastAPI(
    title="Oil Price Tracker (Secure Edition)",
    description="Enterprise-grade API for oil prices and geopolitical events",
    version="2.0",
    openapi_tags=[
        {"name": "Prices", "description": "Oil Price Data"},
        {"name": "Analytics", "description": "Statistical Insights"},
        {"name": "Events", "description": "Geopolitical Event Data"}
    ]
)


def rate_limit(request: Request):
    ip = request.client.host
    now = time.time()

    if ip not in RATE_LIMIT:
        RATE_LIMIT[ip] = []

    RATE_LIMIT[ip] = [t for t in RATE_LIMIT[ip] if now - t < WINDOW_SECONDS]

    if len(RATE_LIMIT[ip]) >= MAX_REQUESTS:
        raise HTTPException(429, "Too many requests. Slow down.")

    RATE_LIMIT[ip].append(now)


# ----------------------------------------
# HMAC Request Signing
# ----------------------------------------
def verify_signature(
    x_timestamp: str = Header(...),
    x_signature: str = Header(...),
    request: Request = None
):
    # Reject stale requests (replay attack protection)
    now = int(time.time())
    ts = int(x_timestamp)

    if abs(now - ts) > 10:
        raise HTTPException(401, "Request timestamp expired")

    # Reconstruct message
    body = request._body if hasattr(request, "_body") else b""
    message = f"{x_timestamp}{request.method}{request.url.path}".encode() + body

    # Compute HMAC
    expected = hmac.new(
        API_SECRET.encode(),
        message,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, x_signature):
        raise HTTPException(401, "Invalid request signature")


# ----------------------------------------
# API Key Authentication + Scopes
# ----------------------------------------
def verify_api_key(
    x_api_key: str = Header(...),
    scope: str = "read"
):
    if x_api_key != API_KEY:
        raise HTTPException(401, "Invalid API Key")

    # Example of scope-based access control
    if scope == "write" and x_api_key != API_KEY:
        raise HTTPException(403, "API Key does not have write permissions")

def get_db():
    dbtemp = db.SessionLocal()
    try:
        yield dbtemp
    finally:
        dbtemp.close()


@app.post("/prices", response_model=schemas.OilPrice, status_code=201,
          tags=["Prices"],
          dependencies=[Depends(rate_limit),
                        Depends(verify_signature),
                        Depends(lambda: verify_api_key(scope="write"))])
async def create_price(record: schemas.OilPrice, db: Session = Depends(get_db)):
    return crud.create_price(db, record)


@app.get("/prices", response_model=list[schemas.OilPrice],
         tags=["Prices"],
         dependencies=[Depends(rate_limit),
                       Depends(verify_signature),
                       Depends(verify_api_key)])
async def list_prices(db: Session = Depends(get_db)):
    return crud.read_all_price(db)


@app.get("/prices/{id}", response_model=schemas.OilPrice,
         tags=["Prices"],
         dependencies=[Depends(rate_limit),
                       Depends(verify_signature),
                       Depends(verify_api_key)])
async def get_price(id: int, db: Session = Depends(get_db)):
    row = crud.read_one_price(db, id)
    if not row:
        raise HTTPException(404, "Record not Found")
    return row


@app.get("/prices/filter", tags=["Prices"],
         response_model=list[schemas.OilPrice],
         dependencies=[Depends(rate_limit),
                       Depends(verify_signature),
                       Depends(verify_api_key)])
async def filter_prices(
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
    mini: Optional[float] = None,
    maxi: Optional[float] = None,
    db: Session = Depends(get_db)
):
    return crud.filter_prices(db, start, end, mini, maxi)


@app.get("/analytics/average", tags=["Analytics"],
         dependencies=[Depends(rate_limit),
                       Depends(verify_signature),
                       Depends(verify_api_key)])
async def average_price(db: Session = Depends(get_db)):
    return {"average_price": crud.get_avg_price(db)}



@app.exception_handler(Exception)
async def main_exception(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error"}
    )
