import os
import unittest
from base64 import b64encode

os.environ["DATABASE_URL"] = "sqlite:///./test_sims.db"

from fastapi.testclient import TestClient

from backend.main import app


class TestSIMSAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.admin_username = "owner_admin"
        cls.employee_username = "staff_employee"
        cls.password = "StrongPass123"

        cls.client.post(
            "/api/auth/register",
            json={
                "username": cls.admin_username,
                "password": cls.password,
                "role": "admin",
            },
        )
        cls.client.post(
            "/api/auth/register",
            json={
                "username": cls.employee_username,
                "password": cls.password,
                "role": "employee",
            },
        )

    @staticmethod
    def basic_auth_header(username: str, password: str):
        token = b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
        return {"Authorization": f"Basic {token}"}

    def test_supplier_product_and_sale_flow(self):
        supplier = self.client.post(
            "/api/suppliers",
            headers=self.basic_auth_header(self.admin_username, self.password),
            json={
                "supplier_name": "Main Supplier",
                "phone": "12345678",
                "email": "s@example.com",
                "address": "Street 10",
            },
        )
        self.assertEqual(supplier.status_code, 200)
        supplier_id = supplier.json()["id"]

        product = self.client.post(
            "/api/products",
            headers=self.basic_auth_header(self.admin_username, self.password),
            json={
                "name": "Laptop",
                "category": "Electronics",
                "quantity": 5,
                "price": 1000,
                "supplier_id": supplier_id,
            },
        )
        self.assertEqual(product.status_code, 200)
        product_id = product.json()["id"]

        sale = self.client.post(
            "/api/sales",
            headers=self.basic_auth_header(self.employee_username, self.password),
            json={"product_id": product_id, "quantity": 2},
        )
        self.assertEqual(sale.status_code, 201)
        self.assertEqual(sale.json()["total_price"], 2000.0)

        updated = self.client.get(
            f"/api/products/{product_id}",
            headers=self.basic_auth_header(self.employee_username, self.password),
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.json()["quantity"], 3)

    def test_login_returns_user_profile_without_token(self):
        login = self.client.post(
            "/api/auth/login",
            json={
                "username": self.admin_username,
                "password": self.password,
                "role": "admin",
            },
        )
        self.assertEqual(login.status_code, 200)
        body = login.json()
        self.assertEqual(body["username"], self.admin_username)
        self.assertNotIn("access_token", body)

    def test_employee_cannot_create_products_or_suppliers(self):
        employee_headers = self.basic_auth_header(self.employee_username, self.password)

        supplier = self.client.post(
            "/api/suppliers",
            headers=employee_headers,
            json={
                "supplier_name": "Denied Seller",
                "phone": "11111111",
                "email": "denied@seller.com",
                "address": "No Access Street",
            },
        )
        self.assertEqual(supplier.status_code, 403)

        product = self.client.post(
            "/api/products",
            headers=employee_headers,
            json={
                "name": "Denied Product",
                "category": "Blocked",
                "quantity": 1,
                "price": 10,
                "supplier_id": 1,
            },
        )
        self.assertEqual(product.status_code, 403)

    def test_create_product_returns_clear_error_for_missing_supplier(self):
        response = self.client.post(
            "/api/products",
            headers=self.basic_auth_header(self.admin_username, self.password),
            json={
                "name": "Desk Lamp",
                "category": "Office",
                "quantity": 4,
                "price": 15.5,
                "supplier_id": 999999,
            },
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Supplier not found")

    def test_create_product_validation_errors_are_human_readable(self):
        response = self.client.post(
            "/api/products",
            headers=self.basic_auth_header(self.admin_username, self.password),
            json={
                "name": "  ",
                "category": "A",
                "quantity": -1,
                "price": 0,
                "supplier_id": 0,
            },
        )
        self.assertEqual(response.status_code, 422)
        details = response.json()["detail"]
        self.assertIsInstance(details, list)
        self.assertTrue(any("name" in message for message in details))
        self.assertTrue(any("category" in message for message in details))
        self.assertTrue(any("quantity" in message for message in details))


if __name__ == "__main__":
    unittest.main()
