import kagglehub
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime

from db import SessionLocal, Base, engine
from models import OilPrice, GeoEvent

##Comments Created and Code Reviewed by AI

# -------------------------------------------------------------------
# Initialize the database schema.
# This ensures that tables exist before data import begins.
# In production you would use Alembic migrations instead, but for a
# single-purpose pipeline this is acceptable.
# -------------------------------------------------------------------
Base.metadata.create_all(bind=engine)

# Dataset/filename definitions for clarity and maintainability.
DATASET = "kavyadhyani/global-oil-prices-and-geopolitical-events"
FILE_PATH = "oil_geopolitics_dataset_2010_2026.csv"
EVENT_FILE = "geopolitical_events_timeline.csv"


# -------------------------------------------------------------------
# LOAD EVENT DATASET
# This function pulls only the event timeline CSV from Kaggle using
# kagglehub and loads it into a Pandas DataFrame.
# Using a dedicated function keeps the ingestion logic separated from
# side effects (database writes).
# -------------------------------------------------------------------
def load_event_dataset():
    df = kagglehub.dataset_load(
        kagglehub.KaggleDatasetAdapter.PANDAS,
        DATASET,
        EVENT_FILE
    )
    return df


# -------------------------------------------------------------------
# IMPORT EVENTS INTO DATABASE
# This ingests each event row and maps Kaggle's column names to our
# database schema. Using try/except ensures a single bad row will not
# break the entire import (robustness for large datasets).
# -------------------------------------------------------------------
def import_events():
    df = load_event_dataset()

    # Normalize dataset column names to match our SQLAlchemy model fields.
    df = df.rename(columns={
        "date": "date",
        "eventType": "event_type",
        "eventDescription": "event_description",
        "eventSeverity": "event_severity",
        "eventFlag": "event_flag"
    })

    db: Session = SessionLocal()

    # Iterate row-by-row.
    # For large datasets consider using bulk operations or chunking.
    for _, row in df.iterrows():
        try:
            # Convert string to Python date object.
            # Using explicit parsing avoids silent type mismatches.
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
            # Unknown or malformed rows are skipped.
            # Logging is recommended in production to track data issues.
            pass

    db.commit()
    db.close()
    print("Event import complete.")


# -------------------------------------------------------------------
# LOAD OIL PRICE DATASET
# Similar to event loading but for the primary oil price table.
# -------------------------------------------------------------------
def load_dataset():
    df = kagglehub.dataset_load(
        kagglehub.KaggleDatasetAdapter.PANDAS,
        DATASET,
        FILE_PATH
    )
    return df


# -------------------------------------------------------------------
# IMPORT OIL PRICE DATA
# Loads the historical oil price dataset, renames columns, converts 
# values, and writes to SQLAlchemy model.
# -------------------------------------------------------------------
def import_data():
    df = load_dataset()

    # Normalize column names to match our database schema.
    df = df.rename(columns={
        "Date": "date",
        "brent_price": "price",
    })

    db: Session = SessionLocal()

    for _, row in df.iterrows():
        try:
            # Parse dates consistently.
            date = datetime.strptime(row["date"], "%Y-%m-%d").date()

            # Force numeric conversion to avoid object-type pollution.
            price = float(row["price"])

            record = OilPrice(
                date=date,
                price=price
            )

            # Add to session; delay commit for performance.
            db.add(record)

        except Exception:
            # Corrupt or unexpected rows are ignored.
            # As above, production code should log these failures.
            pass

    db.commit()
    db.close()
    print("Import complete.")


# -------------------------------------------------------------------
# MAIN EXECUTION
# Running the script directly performs the full ingestion pipeline.
# Keeping this separate avoids import-time side effects when imported
# into other modules or used by FastAPI.
# -------------------------------------------------------------------
if __name__ == "__main__":
    import_data()
    import_events()