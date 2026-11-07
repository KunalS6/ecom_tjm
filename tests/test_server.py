import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from server import PRODUCTS, create_app


class StorefrontTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        database_path = Path(self.temp_directory.name) / "orders.sqlite3"
        self.app = create_app(database_path)
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_storefront_and_all_eight_products_are_available(self):
        self.assertIn("টক ঝাল মিষ্টি", self.client.get("/").get_data(as_text=True))
        products_response = self.client.get("/api/products")
        self.assertEqual(products_response.status_code, 200)
        products = products_response.get_json()
        self.assertEqual(len(products), 8)
        self.assertEqual(sum(product["category"] == "pickle" for product in products), 4)
        self.assertEqual(sum(product["category"] == "homemade" for product in products), 4)
        styles_response = self.client.get("/styles.css")
        script_response = self.client.get("/app.js")
        logo_response = self.client.get("/logo.jpeg")
        self.assertEqual(styles_response.status_code, 200)
        self.assertEqual(script_response.status_code, 200)
        self.assertEqual(logo_response.status_code, 200)
        self.assertEqual(logo_response.mimetype, "image/jpeg")
        styles_response.close()
        script_response.close()
        logo_response.close()

    def test_valid_order_is_persisted_with_server_calculated_prices(self):
        payload = {
            "name": "মিতা দাস",
            "phone": "+91 98765-43210",
            "address": "১২, রবীন্দ্র সরণি, কলকাতা",
            "note": "",
            "items": [
                {"id": "aamer-achar", "quantity": 2},
                {"id": "gurer-naru", "quantity": 1},
            ],
        }
        expected_total = PRODUCTS[0]["price"] * 2 + PRODUCTS[4]["price"]

        response = self.client.post("/api/orders", json=payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["total"], expected_total)
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            order = connection.execute(
                "SELECT customer_name, phone, items, total, status FROM orders"
            ).fetchone()
        self.assertEqual(order[0], "মিতা দাস")
        self.assertEqual(order[1], "+919876543210")
        self.assertEqual(json.loads(order[2])[0]["unit_price"], PRODUCTS[0]["price"])
        self.assertEqual(order[3], expected_total)
        self.assertEqual(order[4], "received")

    def test_invalid_product_and_contact_details_are_rejected(self):
        response = self.client.post(
            "/api/orders",
            json={
                "name": "A",
                "phone": "abc1234567",
                "address": "short",
                "items": [{"id": "not-a-product", "quantity": 1}],
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.get_json()["fields"])
        self.assertIn("phone", response.get_json()["fields"])
        self.assertIn("address", response.get_json()["fields"])
        self.assertIn("items", response.get_json()["fields"])
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 0)

    def test_order_quantity_is_bounded(self):
        response = self.client.post(
            "/api/orders",
            json={
                "name": "মিতা দাস",
                "phone": "9876543210",
                "address": "১২, রবীন্দ্র সরণি, কলকাতা",
                "items": [{"id": "aamer-achar", "quantity": 21}],
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("items", response.get_json()["fields"])


if __name__ == "__main__":
    unittest.main()
