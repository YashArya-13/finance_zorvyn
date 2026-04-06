from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.database import SessionLocal
from app import models
from app.utils.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 📊 SUMMARY API
@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    total_income = db.query(func.sum(models.FinancialRecord.amount))\
        .filter(models.FinancialRecord.type == "income").scalar() or 0

    total_expense = db.query(func.sum(models.FinancialRecord.amount))\
        .filter(models.FinancialRecord.type == "expense").scalar() or 0

    net_balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance
    }


# 📊 CATEGORY-WISE TOTAL
@router.get("/category")
def category_summary(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    data = db.query(
        models.FinancialRecord.category,
        func.sum(models.FinancialRecord.amount)
    ).group_by(models.FinancialRecord.category).all()

    return [{"category": c, "total": t} for c, t in data]


# 🕒 RECENT TRANSACTIONS
@router.get("/recent")
def recent_transactions(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    records = db.query(models.FinancialRecord)\
        .order_by(models.FinancialRecord.date.desc())\
        .limit(5).all()

    return records


# 📈 MONTHLY TREND
@router.get("/monthly")
def monthly_trend(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    data = db.query(
        func.strftime("%Y-%m", models.FinancialRecord.date),
        func.sum(models.FinancialRecord.amount)
    ).group_by(
        func.strftime("%Y-%m", models.FinancialRecord.date)
    ).all()

    return [{"month": m, "total": t} for m, t in data]