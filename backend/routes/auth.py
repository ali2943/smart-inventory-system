from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database.connection import get_db
from backend.models.entities import User
from backend.models.schemas import UserLogin, UserOut, UserRegister
from backend.utils.security import hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    username = payload.username.strip()
    existing = db.query(User).filter(User.email == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")

    user = User(
        name=username,
        email=username,
        password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(id=user.id, username=user.email, role=user.role)


@router.post("/login", response_model=UserOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    username = payload.username.strip()
    user = db.query(User).filter(User.email == username).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if payload.role and user.role != payload.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Account is not registered as {payload.role}",
        )

    return UserOut(id=user.id, username=user.email, role=user.role)
