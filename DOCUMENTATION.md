# Smart Inventory Management System (SIMS)

## Project Summary

Smart Inventory Management System (SIMS) is a full-stack inventory application for small businesses. It provides a FastAPI backend, a MySQL database, and a Bootstrap-based frontend for managing users, suppliers, products, sales, and inventory movement.

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Testing:** Python `unittest`

## Repository Structure

```text
smart-inventory-system/
├── backend/
│   ├── main.py
│   ├── database/
│   ├── dependencies/
│   ├── models/
│   ├── routes/
│   └── utils/
├── database/
│   ├── schema.sql
│   └── sample_data.sql
├── frontend/
│   ├── css/
│   ├── js/
│   └── pages/
├── tests/
├── requirements.txt
└── README.md
```

## Key Features

- User registration and login
- Role-based access control for `admin` and `employee`
- Product CRUD and search
- Supplier management
- Sales creation and sales history
- Inventory stock-in, stock-out, and quantity updates
- Low-stock alerts
- Dashboard summary endpoint
- Responsive frontend pages

## Backend Architecture

The backend starts from `backend/main.py`, where the FastAPI application is created, routers are included, CORS is enabled, and validation errors are converted into cleaner messages.

### Main backend entrypoint

```python
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.database.connection import engine
from backend.models.base import Base
from backend.models import entities  # noqa: F401
from backend.routes import auth, dashboard, inventory, products, sales, suppliers
```

The application also creates database tables on startup:

```python
Base.metadata.create_all(bind=engine)
```

And exposes a simple health check:

```python
@app.get("/")
def health_check():
    return {"message": "SIMS API is running"}
```

## Database Design

The SQL schema defines four main tables:

- `users`
- `suppliers`
- `products`
- `sales`

### Schema summary

```sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'employee') NOT NULL DEFAULT 'employee'
);
```

```sql
CREATE TABLE IF NOT EXISTS suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(120) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(150) NOT NULL,
    address VARCHAR(255) NOT NULL
);
```

```sql
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    category VARCHAR(100) NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    price DECIMAL(10,2) NOT NULL,
    supplier_id INT NOT NULL,
    CONSTRAINT fk_products_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
      ON DELETE RESTRICT ON UPDATE CASCADE
);
```

```sql
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sales_product FOREIGN KEY (product_id) REFERENCES products(id)
      ON DELETE RESTRICT ON UPDATE CASCADE
);
```

## API Endpoints

### Authentication

- `POST /api/auth/register`
- `POST /api/auth/login`

### Products

- `GET /api/products`
- `GET /api/products/{id}`
- `POST /api/products`
- `PUT /api/products/{id}`
- `DELETE /api/products/{id}`

### Suppliers

- `GET /api/suppliers`
- `POST /api/suppliers`
- `PUT /api/suppliers/{id}`
- `DELETE /api/suppliers/{id}`

### Sales

- `GET /api/sales`
- `POST /api/sales`

### Inventory

- `POST /api/inventory/stock-in/{product_id}`
- `POST /api/inventory/stock-out/{product_id}`
- `PUT /api/inventory/quantity/{product_id}`
- `GET /api/inventory/low-stock`

### Dashboard

- `GET /api/dashboard/summary`

## Frontend Pages

The `frontend/pages` directory contains the static user interface pages:

- `login.html`
- `dashboard.html`
- `products.html`
- `add-product.html`
- `suppliers.html`
- `sales.html`

The frontend communicates with the backend using the API base configured in `frontend/js/api.js`.

## Installation and Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

- **Windows:** `.
  .venv\Scripts\activate`
- **macOS/Linux:** `source .venv/bin/activate`

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the database connection

```bash
export DATABASE_URL='mysql+pymysql://root:password@localhost:3306/sims'
```

### 4. Initialize the database

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/sample_data.sql
```

### 5. Run the backend server

```bash
uvicorn backend.main:app --reload
```

## Testing

The project includes automated tests in `tests/test_api.py`.

### Run tests

```bash
python -m unittest tests/test_api.py
```

## Test Coverage Summary

The tests currently cover:

- admin and employee registration setup
- supplier creation and product creation flow
- sales creation and inventory quantity reduction
- login response structure
- employee permission restrictions
- missing supplier error handling
- validation error formatting

### Example test scenarios

#### 1. Supplier, product, and sale flow

- create a supplier as admin
- create a product linked to that supplier
- create a sale as employee
- verify the sale total price
- verify product quantity is updated

#### 2. Access control checks

- employee users are blocked from creating products
- employee users are blocked from creating suppliers

#### 3. Validation checks

- invalid product input returns a readable `422` response

#### 4. Error handling checks

- creating a product with a missing supplier returns `404 Supplier not found`

## Notes on Authentication

Protected endpoints require HTTP Basic authentication headers for a registered user.

## Health Check

You can confirm the API is running by visiting:

- `GET /`

Expected response:

```json
{"message": "SIMS API is running"}
```

## License

No license file is currently included in the repository.
