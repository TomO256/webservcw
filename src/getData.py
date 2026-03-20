import kagglehub
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime

from db import SessionLocal,Base, engine
from models import OilPrice, GeoEvent
Base.metadata.create_all(bind=engine)

DATASET = "kavyadhyani/global-oil-prices-and-geopolitical-events"
FILE_PATH = "oil_geopolitics_dataset_2010_2026.csv"
EVENT_FILE = "geopolitical_events_timeline.csv"

def load_event_dataset():
    df = kagglehub.dataset_load(
        kagglehub.KaggleDatasetAdapter.PANDAS,
        DATASET,
        EVENT_FILE
    )
    return df


def import_events():
    df = load_event_dataset()

    df = df.rename(columns={
        "date": "date",
        "eventType": "event_type",
        "eventDescription": "event_description",
        "eventSeverity": "event_severity",
        "eventFlag": "event_flag"
    })

    db: Session = SessionLocal()

    for _, row in df.iterrows():
        try:
            date = datetime.strptime(str(row["date"]), "%Y-%m-%d").date()

            record = GeoEvent(
                date=date,
                event_type=row.get("event_type"),
                event_description=row.get("event_description"),
                event_severity=row.get("event_severity"),
                event_flag=row.get("event_flag")
            )

            db.add(record)

        except Exception:
            pass

    db.commit()
    db.close()
    print("Event import complete.")

def load_dataset():
    df = kagglehub.dataset_load(
        kagglehub.KaggleDatasetAdapter.PANDAS,
        DATASET,
        FILE_PATH
    )
    return df

def import_data():
    df = load_dataset()
    df = df.rename(columns={
        "Date": "date",
        "brent_price": "price",
    })

    db: Session = SessionLocal()

    for _, row in df.iterrows():
        try:
            date = datetime.strptime(row["date"], "%Y-%m-%d").date()
            price = float(row["price"])

            record = OilPrice(
                date=date,
                price=price
            )

            db.add(record)
        except Exception as e:
            # print("Skipping row:", e)
            pass

    db.commit()
    db.close()
    print("Import complete.")

if __name__ == "__main__":
    import_data()
    import_events()
