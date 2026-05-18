from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.entities import Product, Sale
from backend.models.schemas import SaleCreate, SaleOut

router = APIRouter(prefix="/api/sales", tags=["Sales"])


@router.get("", response_model=list[SaleOut])
def list_sales(db: Session = Depends(get_db)):
    return db.query(Sale).order_by(Sale.created_at.desc()).all()


@router.post("", response_model=SaleOut, status_code=status.HTTP_201_CREATED)
def create_sale(
    payload: SaleCreate,
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    product.quantity -= payload.quantity
    total_price = round(product.price * payload.quantity, 2)

    sale = Sale(
        product_id=payload.product_id,
        quantity=payload.quantity,
        total_price=total_price,
    )
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale
