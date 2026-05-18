from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.database.connection import engine
from backend.models.base import Base
from backend.models import entities  # noqa: F401
from backend.routes import auth, dashboard, inventory, products, sales, suppliers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Inventory Management System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(suppliers.router)
app.include_router(sales.router)
app.include_router(dashboard.router)
app.include_router(inventory.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    messages = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error.get("loc", []) if part != "body")
        message = error.get("msg", "Invalid value")
        messages.append(f"{location}: {message}" if location else message)
    return JSONResponse(status_code=422, content={"detail": messages or ["Validation failed"]})


@app.get("/")
def health_check():
    return {"message": "SIMS API is running"}
