from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.entities import Product, Supplier
from backend.models.schemas import ProductCreate, ProductOut, ProductUpdate
from backend.utils.auth import require_roles

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=list[ProductOut])
def list_products(
    search: str | None = None,
    _=Depends(require_roles("admin", "employee")),
    db: Session = Depends(get_db),
):
    query = db.query(Product)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    return query.order_by(Product.id.desc()).all()


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    _=Depends(require_roles("admin", "employee")),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductOut)
def create_product(
    payload: ProductCreate,
    _=Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    supplier = db.query(Supplier).filter(Supplier.id == payload.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    try:
        product = Product(**payload.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Unable to create product due to invalid related data. Please verify supplier and product details.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create product right now. Please try again.",
        ) from exc


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    _=Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    supplier = db.query(Supplier).filter(Supplier.id == payload.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")

    for key, value in payload.model_dump().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    _=Depends(require_roles("admin")),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
