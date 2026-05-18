from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.entities import Product, Sale, Supplier

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/summary")
def dashboard_summary(
    low_stock_threshold: int = 5,
    db: Session = Depends(get_db),
):
    total_products = db.query(func.count(Product.id)).scalar() or 0
    total_sales = db.query(func.coalesce(func.sum(Sale.total_price), 0)).scalar() or 0
    low_stock_products = db.query(func.count(Product.id)).filter(Product.quantity <= low_stock_threshold).scalar() or 0
    total_suppliers = db.query(func.count(Supplier.id)).scalar() or 0

    return {
        "total_products": total_products,
        "total_sales": float(total_sales),
        "low_stock_products": low_stock_products,
        "total_suppliers": total_suppliers,
    }
