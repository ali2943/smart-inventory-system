import os
import unittest

os.environ["DATABASE_URL"] = "sqlite:///./test_sims.db"

from fastapi.testclient import TestClient

from backend.main import app


class TestSIMSAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.email = "owner@example.com"
        cls.password = "StrongPass123"

        cls.client.post(
            "/api/auth/register",
            json={
                "name": "Owner",
                "email": cls.email,
                "password": cls.password,
                "role": "admin",
            },
        )

    def test_supplier_product_and_sale_flow(self):
        supplier = self.client.post(
            "/api/suppliers",
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
            json={"product_id": product_id, "quantity": 2},
        )
        self.assertEqual(sale.status_code, 201)
        self.assertEqual(sale.json()["total_price"], 2000.0)

        updated = self.client.get(f"/api/products/{product_id}")
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.json()["quantity"], 3)

    def test_login_returns_user_profile_without_token(self):
        login = self.client.post(
            "/api/auth/login", json={"email": self.email, "password": self.password}
        )
        self.assertEqual(login.status_code, 200)
        body = login.json()
        self.assertEqual(body["email"], self.email)
        self.assertNotIn("access_token", body)


if __name__ == "__main__":
    unittest.main()
