from sqlalchemy.orm import Session
import sqlalchemy
import datetime

from . import models, schemas

##Comments Created and Code Reviewed by AI

# ---------------------------------------------------------
# Create
# ---------------------------------------------------------
def create_price(db: Session, record: schemas.CreateOilPrice) -> models.OilPrice:
    """
    Create a new OilPrice record.

    Args:
        db (Session): SQLAlchemy session.
        record (schemas.CreateOilPrice): Pydantic schema containing date and price.

    Returns:
        models.OilPrice: The newly created OilPrice database row.
    """
    row = models.OilPrice(**record.dict())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


# ---------------------------------------------------------
# Read
# ---------------------------------------------------------
def read_all_price(db: Session) -> list[models.OilPrice]:
    """
    Retrieve all oil price records.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        list[models.OilPrice]: All price rows in the database.
    """
    return db.query(models.OilPrice).all()


def read_one_price(db: Session, record_id: int) -> models.OilPrice | None:
    """
    Retrieve a single oil price record by ID.

    Args:
        db (Session): SQLAlchemy session.
        record_id (int): Primary key of the OilPrice record.

    Returns:
        models.OilPrice | None: The found record or None.
    """
    return db.query(models.OilPrice).filter(models.OilPrice.id == record_id).first()


# ---------------------------------------------------------
# Update
# ---------------------------------------------------------
def update_price(db: Session, record_id: int, record: schemas.CreateOilPrice) -> models.OilPrice | None:
    """
    Update an existing oil price record.

    Args:
        db (Session): SQLAlchemy session.
        record_id (int): ID of the record to update.
        record (schemas.CreateOilPrice): New values for the record.

    Returns:
        models.OilPrice | None: Updated row or None if not found.
    """
    row = read_one_price(db, record_id)
    if not row:
        return None

    for field, value in record.dict().items():
        setattr(row, field, value)

    db.commit()
    db.refresh(row)
    return row


# ---------------------------------------------------------
# Delete
# ---------------------------------------------------------
def delete_price(db: Session, record_id: int) -> bool:
    """
    Delete an oil price record.

    Args:
        db (Session): SQLAlchemy session.
        record_id (int): ID of the record to delete.

    Returns:
        bool: True if deleted, False if not found.
    """
    row = read_one_price(db, record_id)
    if not row:
        return False

    db.delete(row)
    db.commit()
    return True


# ---------------------------------------------------------
# Filtering
# ---------------------------------------------------------
def filter_prices(
    db: Session,
    start: datetime.date | None = None,
    end: datetime.date | None = None,
    mini: float | None = None,
    maxi: float | None = None
) -> list[models.OilPrice]:
    """
    Filter oil prices by date range and/or price range.

    Args:
        db (Session): SQLAlchemy session.
        start (date | None): Minimum date.
        end (date | None): Maximum date.
        mini (float | None): Minimum price.
        maxi (float | None): Maximum price.

    Returns:
        list[models.OilPrice]: Filtered records.
    """
    query = db.query(models.OilPrice)

    if start:
        query = query.filter(models.OilPrice.date >= start)
    if end:
        query = query.filter(models.OilPrice.date <= end)
    if mini is not None:
        query = query.filter(models.OilPrice.price >= mini)
    if maxi is not None:
        query = query.filter(models.OilPrice.price <= maxi)

    return query.all()


# ---------------------------------------------------------
# Sorting
# ---------------------------------------------------------
def sort_prices(
    db: Session,
    sort_by: str = "date",
    order: str = "asc"
) -> list[models.OilPrice] | None:
    """
    Sort the oil price table by any valid column.

    Args:
        db (Session): SQLAlchemy session.
        sort_by (str): Column to sort by (default "date").
        order (str): "asc" or "desc".

    Returns:
        list[models.OilPrice] | None: Sorted results or None if column invalid.
    """
    column = getattr(models.OilPrice, sort_by, None)
    if column is None:
        return None  # invalid sort field

    ordering = sqlalchemy.asc(column) if order == "asc" else sqlalchemy.desc(column)
    return db.query(models.OilPrice).order_by(ordering).all()


# ---------------------------------------------------------
# Analytics
# ---------------------------------------------------------
def get_avg_price(db: Session) -> float | None:
    """
    Compute the average oil price.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        float | None: Average price or None if table empty.
    """
    return db.query(sqlalchemy.func.avg(models.OilPrice.price)).scalar()


def get_max_price(db: Session) -> float | None:
    """
    Retrieve the maximum recorded oil price.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        float | None: Max price or None if no data.
    """
    return db.query(sqlalchemy.func.max(models.OilPrice.price)).scalar()


def get_min_price(db: Session) -> float | None:
    """
    Retrieve the minimum recorded oil price.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        float | None: Min price or None if no data.
    """
    return db.query(sqlalchemy.func.min(models.OilPrice.price)).scalar()