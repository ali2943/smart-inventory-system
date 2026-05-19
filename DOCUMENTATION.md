# Smart Inventory Management System (SIMS)

A simple full-stack inventory management system for small businesses built with FastAPI, MySQL, HTML, CSS, Bootstrap 5, and JavaScript.

## Overview

SIMS helps manage users, suppliers, products, inventory movement, and sales from a single web application. It includes role-based access for `admin` and `employee` users, with the backend exposed through a REST API and the frontend implemented with static HTML/CSS/JavaScript pages.

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

## Main Technologies

- **Backend:** Python, FastAPI
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap 5
- **Testing:** Python `unittest`

## Core Features

- User registration and login with `username` and `password`
- Role-based access control for `admin` and `employee`
- Dashboard summary data API
- Product management with search and CRUD operations
- Inventory stock in / stock out / quantity update
- Low-stock alert endpoint
- Supplier management
- Sales creation and sales history
- Responsive frontend pages

## Database Tables

The database schema includes the following main tables:

- `users` — stores account information and user roles
- `suppliers` — stores supplier/seller details
- `products` — stores inventory items and links to suppliers
- `sales` — stores sales transactions and total price values

## Backend Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set the database connection string:

```bash
export DATABASE_URL='mysql+pymysql://root:password@localhost:3306/sims'
```

4. Create the database and sample tables/data:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/sample_data.sql
```

5. Start the API server:

```bash
uvicorn backend.main:app --reload
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

Open the files inside `frontend/pages` in a browser or serve them through a static file server.

Available pages include:

- `login.html`
- `dashboard.html`
- `products.html`
- `add-product.html`
- `suppliers.html`
- `sales.html`

If the backend URL changes, update the API base URL in `frontend/js/api.js`.

## Testing

Run the built-in test suite with:

```bash
python -m unittest tests/test_api.py
```

## Testing Highlights

The test suite currently checks:

- supplier and product creation flow
- sales creation and inventory quantity updates
- login response behavior
- access control for employee users
- validation error formatting
- missing supplier handling when creating a product

## Notes

- The API uses HTTP Basic authentication for protected endpoints.
- Validation errors are converted into human-readable messages.
- The root endpoint `GET /` returns a simple health message.

## License

No license file is currently included in the repository.
