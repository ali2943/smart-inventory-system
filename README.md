# Smart Inventory Management System (SIMS)

A simple full-stack inventory app for small businesses, built with FastAPI, MySQL, HTML, CSS, Bootstrap 5, and JavaScript.

## Folder Structure

```text
smart-inventory-system/
├── frontend/
│   ├── css/
│   ├── js/
│   └── pages/
├── backend/
│   ├── main.py
│   ├── routes/
│   ├── models/
│   └── database/
├── database/
│   ├── schema.sql
│   └── sample_data.sql
├── tests/
├── requirements.txt
└── README.md
```

## Features

- JWT authentication (register, login, profile)
- Roles: `admin`, `employee`
- Dashboard summary cards data API
- Product CRUD + search
- Inventory management (stock in/out, quantity update, low stock alert)
- Supplier CRUD
- Sales create + history + total price calculation
- Responsive Bootstrap pages with sidebar navigation

## Backend Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
export DATABASE_URL='mysql+pymysql://root:password@localhost:3306/sims'
export SECRET_KEY='your-very-strong-secret'
export ACCESS_TOKEN_EXPIRE_MINUTES='60'
```

4. Initialize database tables:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/sample_data.sql
```

5. Run API:

```bash
uvicorn backend.main:app --reload
```

## API Endpoints

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/profile`

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

Open files under `frontend/pages` in a browser (or serve statically):

- `login.html`
- `dashboard.html`
- `products.html`
- `add-product.html`
- `suppliers.html`
- `sales.html`

Update `API_BASE` in `frontend/js/api.js` if backend URL changes.

## Basic Test

```bash
python -m unittest tests/test_api.py
```
