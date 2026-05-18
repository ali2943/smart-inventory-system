from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=72)
    role: Literal["admin", "employee"] = "employee"


class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=72)
    role: Literal["admin", "employee"] | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str


class SupplierBase(BaseModel):
    supplier_name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=6, max_length=20)
    email: EmailStr
    address: str = Field(min_length=5, max_length=255)


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(SupplierBase):
    pass


class SupplierOut(SupplierBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProductBase(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    category: str = Field(min_length=2, max_length=100)
    quantity: int = Field(ge=0)
    price: float = Field(gt=0)
    supplier_id: int = Field(gt=0)

    @field_validator("name", "category")
    @classmethod
    def normalize_non_empty_text(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) < 2:
            raise ValueError("must be at least 2 non-space characters")
        return normalized


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class SaleCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class SaleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    total_price: float
    created_at: datetime


class QuantityUpdate(BaseModel):
    quantity: int = Field(ge=0)


class StockAdjustment(BaseModel):
    quantity: int = Field(gt=0)
