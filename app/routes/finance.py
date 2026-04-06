from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date

from app import models, schemas
from app.database import SessionLocal
from app.utils.auth import get_current_user
from app.utils.role_checker import require_roles

router = APIRouter(prefix="/records", tags=["Financial Records"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ➕ CREATE RECORD (Admin + Analyst)
@router.post("/")
def create_record(
    record: schemas.RecordCreate,
    db: Session = Depends(get_db),
    user = Depends(require_roles(["admin", "analyst"]))
):
    new_record = models.FinancialRecord(
        amount=record.amount,
        type=record.type,
        category=record.category,
        date=record.date,
        notes=record.notes,
        user_id=user.id
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


# 📄 GET RECORDS (ALL USERS)
@router.get("/")
def get_records(
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None)
):
    query = db.query(models.FinancialRecord)

    if type:
        query = query.filter(models.FinancialRecord.type == type)

    if category:
        query = query.filter(models.FinancialRecord.category == category)

    if start_date:
        query = query.filter(models.FinancialRecord.date >= start_date)

    if end_date:
        query = query.filter(models.FinancialRecord.date <= end_date)

    return query.all()


# ✏️ UPDATE RECORD (Admin only)
@router.put("/{record_id}")
def update_record(
    record_id: int,
    updated: schemas.RecordCreate,
    db: Session = Depends(get_db),
    user = Depends(require_roles(["admin"]))
):
    record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    record.amount = updated.amount
    record.type = updated.type
    record.category = updated.category
    record.date = updated.date
    record.notes = updated.notes

    db.commit()

    return {"message": "Record updated"}


# ❌ DELETE RECORD (Admin only)
@router.delete("/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_roles(["admin"]))
):
    record = db.query(models.FinancialRecord).filter(models.FinancialRecord.id == record_id).first()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()

    return {"message": "Record deleted"}