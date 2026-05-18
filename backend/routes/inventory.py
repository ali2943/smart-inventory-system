from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.dependencies.auth import get_current_user
from backend.models.entities import Product, User
from backend.models.schemas import ProductOut, QuantityUpdate, StockAdjustment

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


@router.post("/stock-in/{product_id}", response_model=ProductOut)
def stock_in(
    product_id: int,
    payload: StockAdjustment,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.quantity += payload.quantity
    db.commit()
    db.refresh(product)
    return product


@router.post("/stock-out/{product_id}", response_model=ProductOut)
def stock_out(
    product_id: int,
    payload: StockAdjustment,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.quantity < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    product.quantity -= payload.quantity
    db.commit()
    db.refresh(product)
    return product


@router.put("/quantity/{product_id}", response_model=ProductOut)
def update_quantity(
    product_id: int,
    payload: QuantityUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.quantity = payload.quantity
    db.commit()
    db.refresh(product)
    return product


@router.get("/low-stock", response_model=list[ProductOut])
def low_stock(
    threshold: int = 5,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(Product).filter(Product.quantity <= threshold).order_by(Product.quantity.asc()).all()
