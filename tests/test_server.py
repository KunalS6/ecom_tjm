import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from server import PRODUCTS, create_app


class StorefrontTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        base_path = Path(self.temp_directory.name)
        database_path = base_path / "orders.sqlite3"
        self.private_path = base_path / "private"
        self.app = create_app(database_path, self.private_path)
        self.review_urls = []
        self.app.config["REVIEW_EMAIL_SENDER"] = lambda _order, url: self.review_urls.append(url)
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_directory.cleanup()

    def post_order(self, payload, image=None, filename="payment.png"):
        image_buffer = BytesIO()
        if image is None:
            Image.new("RGB", (24, 24), color=(206, 75, 43)).save(image_buffer, format="PNG")
            image = image_buffer.getvalue()
        payload.setdefault("proof_consent", True)
        return self.client.post(
            "/api/orders",
            data={
                "order": json.dumps(payload, ensure_ascii=False),
                "payment_proof": (BytesIO(image), filename),
            },
            content_type="multipart/form-data",
        )

    def test_storefront_and_all_eight_products_are_available(self):
        self.assertIn("টক ঝাল মিষ্টি", self.client.get("/").get_data(as_text=True))
        products_response = self.client.get("/api/products")
        self.assertEqual(products_response.status_code, 200)
        products = products_response.get_json()
        self.assertEqual(len(products), 8)
        self.assertEqual(sum(product["category"] == "pickle" for product in products), 4)
        self.assertEqual(sum(product["category"] == "homemade" for product in products), 4)
        self.assertEqual(self.client.get("/api/store-config").status_code, 404)
        self.assertNotIn("987654321", self.client.get("/").get_data(as_text=True))
        self.assertEqual(self.client.get(f"/order/{'a' * 24}?lang=en").status_code, 200)
        self.assertIn(
            '<html lang="en">',
            self.client.get(f"/order/{'a' * 24}?lang=en").get_data(as_text=True),
        )
        self.assertIn(
            '<html lang="bn">',
            self.client.get(f"/order/{'a' * 24}?lang=invalid").get_data(as_text=True),
        )
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
        review_script = self.client.get("/review.js")
        order_script = self.client.get("/order.js")
        self.assertEqual(review_script.status_code, 200)
        self.assertEqual(order_script.status_code, 200)
        review_script.close()
        order_script.close()

    @patch.dict(
        "os.environ",
        {
            "TOKJHAL_PUBLIC_BASE_URL": "",
            "RENDER_EXTERNAL_URL": "https://tok-jhal-misti.onrender.com",
        },
    )
    def test_render_external_url_is_used_for_private_review_links(self):
        app = create_app(
            Path(self.temp_directory.name) / "render-orders.sqlite3",
            Path(self.temp_directory.name) / "render-private",
        )
        self.assertEqual(
            app.config["PUBLIC_BASE_URL"],
            "https://tok-jhal-misti.onrender.com",
        )

    def test_order_can_be_placed_without_payment_number_or_screenshot(self):
        response = self.client.post(
            "/api/orders",
            json={
                "name": "মিতা দাস",
                "phone": "9876543210",
                "address": "১২, রবীন্দ্র সরণি, কলকাতা",
                "items": [{"id": "aamer-achar", "quantity": 1}],
            },
        )
        self.assertEqual(response.status_code, 201)
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            proof_path = connection.execute(
                "SELECT payment_proof_path FROM orders WHERE public_id = ?",
                (response.get_json()["order_id"],),
            ).fetchone()[0]
        self.assertIsNone(proof_path)

    @patch("server.smtplib.SMTP")
    def test_smtp_order_notification_targets_business_and_contains_review_link(self, smtp_factory):
        self.app.config.pop("REVIEW_EMAIL_SENDER")
        self.app.config.update(
            EMAIL_MODE="smtp",
            OWNER_EMAIL="tokjhalmistico.2027@gmail.com",
            PUBLIC_BASE_URL="https://tok-jhal-misti.example",
            SMTP_USERNAME="tokjhalmistico.2027@gmail.com",
            SMTP_PASSWORD="test-only-app-password",
        )
        response = self.client.post(
            "/api/orders",
            json={
                "name": "মিতা দাস",
                "phone": "9876543210",
                "address": "১২, রবীন্দ্র সরণি, কলকাতা",
                "items": [{"id": "aamer-achar", "quantity": 1}],
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()["notification_status"], "sent")
        smtp = smtp_factory.return_value.__enter__.return_value
        message = smtp.send_message.call_args.args[0]
        self.assertEqual(message["To"], "tokjhalmistico.2027@gmail.com")
        self.assertEqual(message["From"], "tokjhalmistico.2027@gmail.com")
        self.assertIn(
            "https://tok-jhal-misti.example/review/",
            message.get_body(preferencelist=("plain",)).get_content(),
        )
        self.assertIn(
            "Review and accept or reject this order",
            message.get_body(preferencelist=("html",)).get_content(),
        )

    def test_optional_payment_screenshot_is_private_when_attached(self):
        response = self.post_order(
            {
                "name": "মিতা দাস",
                "phone": "9876543210",
                "address": "১২, রবীন্দ্র সরণি, কলকাতা",
                "items": [{"id": "aamer-achar", "quantity": 1}],
            }
        )
        self.assertEqual(response.status_code, 201)
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            proof_path = connection.execute(
                "SELECT payment_proof_path FROM orders WHERE public_id = ?",
                (response.get_json()["order_id"],),
            ).fetchone()[0]
        proof_file = self.private_path / "payment-proofs" / proof_path
        self.assertTrue(proof_file.is_file())
        self.assertEqual(self.client.get(f"/instance/private/payment-proofs/{proof_path}").status_code, 404)

    def test_non_image_screenshot_is_rejected(self):
        response = self.post_order(
            {
                "name": "মিতা দাস",
                "phone": "9876543210",
                "address": "১২, রবীন্দ্র সরণি, কলকাতা",
                "items": [{"id": "aamer-achar", "quantity": 1}],
            },
            image=b"not an image",
            filename="payment.png",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("payment_proof", response.get_json()["fields"])
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 0)

    def test_order_review_approval_and_downloadable_bengali_pdf(self):
        payload = {
            "name": "মিতা দাস",
            "phone": "+91 98765-43210",
            "address": "১২, রবীন্দ্র সরণি, কলকাতা",
            "note": "",
            "payment_reference": "UPI-DEMO-001",
            "items": [
                {"id": "aamer-achar", "quantity": 2},
                {"id": "gurer-naru", "quantity": 1},
            ],
        }
        expected_total = PRODUCTS[0]["price"] * 2 + PRODUCTS[4]["price"]

        response = self.post_order(payload)

        self.assertEqual(response.status_code, 201)
        order_result = response.get_json()
        self.assertEqual(order_result["total"], expected_total)
        self.assertEqual(order_result["status"], "awaiting_review")
        self.assertEqual(order_result["notification_status"], "sent")
        self.assertEqual(len(order_result["receipt_token"]), 43)
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            order = connection.execute(
                "SELECT customer_name, phone, items, total, status, payment_proof_path, payment_reference FROM orders"
            ).fetchone()
        self.assertEqual(order[0], "মিতা দাস")
        self.assertEqual(order[1], "+919876543210")
        self.assertEqual(json.loads(order[2])[0]["unit_price"], PRODUCTS[0]["price"])
        self.assertEqual(order[3], expected_total)
        self.assertEqual(order[4], "awaiting_review")
        proof_path = self.private_path / "payment-proofs" / order[5]
        self.assertTrue(proof_path.is_file())
        self.assertEqual(order[6], "UPI-DEMO-001")
        self.assertEqual(self.client.get(f"/instance/private/payment-proofs/{order[5]}").status_code, 404)

        review_url = f"/api/reviews/{order_result['order_id']}"
        invalid_review = self.client.post(review_url, json={"action": "details", "token": "invalid"})
        self.assertEqual(invalid_review.status_code, 404)
        review_details = self.client.post(
            review_url,
            json={"action": "details", "token": self.read_review_token(order_result["order_id"])},
        )
        self.assertEqual(review_details.status_code, 200)
        self.assertEqual(review_details.get_json()["name"], "মিতা দাস")
        self.assertEqual(review_details.get_json()["total"], expected_total)
        self.assertEqual(review_details.get_json()["payment_reference"], "UPI-DEMO-001")
        self.assertTrue(review_details.get_json()["has_proof"])

        review_token = self.read_review_token(order_result["order_id"])
        proof_response = self.client.post(review_url, json={"action": "proof", "token": review_token})
        self.assertEqual(proof_response.status_code, 200)
        self.assertEqual(proof_response.mimetype, "image/jpeg")
        proof_response.close()
        pending_receipt = self.client.post(
            f"/api/orders/{order_result['order_id']}/receipt.pdf",
            json={"token": order_result["receipt_token"]},
        )
        self.assertEqual(pending_receipt.status_code, 409)
        approval = self.client.post(review_url, json={"action": "approve", "token": review_token})
        self.assertEqual(approval.status_code, 200)
        self.assertEqual(approval.get_json()["status"], "approved")
        self.assertEqual(approval.get_json()["sms_status"], "not_configured")
        repeated_approval = self.client.post(review_url, json={"action": "approve", "token": review_token})
        self.assertEqual(repeated_approval.status_code, 404)

        status_response = self.client.post(
            f"/api/orders/{order_result['order_id']}/status",
            json={"token": order_result["receipt_token"]},
        )
        self.assertEqual(status_response.status_code, 200)
        self.assertEqual(status_response.get_json()["status"], "approved")
        self.assertEqual(status_response.get_json()["name"], "মিতা দাস")
        self.assertEqual(status_response.get_json()["address"], "১২, রবীন্দ্র সরণি, কলকাতা")
        self.assertEqual(status_response.get_json()["total"], expected_total)
        pdf_response = self.client.post(
            f"/api/orders/{order_result['order_id']}/receipt.pdf",
            json={"token": order_result["receipt_token"]},
        )
        self.assertEqual(pdf_response.status_code, 200)
        self.assertEqual(pdf_response.mimetype, "application/pdf")
        self.assertTrue(pdf_response.data.startswith(b"%PDF-"))
        self.assertIn("tok-jhal-order-".encode(), pdf_response.headers["Content-Disposition"].encode())
        pdf_response.close()

    def test_configured_sms_sender_runs_only_after_approval(self):
        sent_messages = []
        self.app.config["SMS_SENDER"] = lambda phone, message: sent_messages.append((phone, message))
        order_response = self.post_order(
            {
                "name": "মিতা দাস",
                "phone": "9876543210",
                "address": "১২, রবীন্দ্র সরণি, কলকাতা",
                "items": [{"id": "aamer-achar", "quantity": 1}],
            }
        )
        order = order_response.get_json()
        self.assertEqual(sent_messages, [])

        review_token = self.read_review_token(order["order_id"])
        approval = self.client.post(
            f"/api/reviews/{order['order_id']}",
            json={"action": "approve", "token": review_token},
        )

        self.assertEqual(approval.get_json()["sms_status"], "sent")
        self.assertEqual(sent_messages[0][0], "9876543210")
        self.assertIn(order["order_id"][:8].upper(), sent_messages[0][1])

    def test_rejection_reason_is_saved_shown_to_customer_and_sent_by_sms(self):
        sent_messages = []
        self.app.config["SMS_SENDER"] = lambda phone, message: sent_messages.append((phone, message))
        order_response = self.client.post(
            "/api/orders",
            json={
                "name": "মিতা দাস",
                "phone": "9876543210",
                "address": "১২, রবীন্দ্র সরণি, কলকাতা",
                "items": [{"id": "aamer-achar", "quantity": 1}],
                "language": "en",
            },
        )
        order = order_response.get_json()
        token = self.read_review_token(order["order_id"])
        review_url = f"/api/reviews/{order['order_id']}"
        missing_reason = self.client.post(review_url, json={"action": "reject", "token": token})
        self.assertEqual(missing_reason.status_code, 400)
        self.assertEqual(sent_messages, [])

        reason = "The selected item is currently unavailable."
        rejection = self.client.post(
            review_url,
            json={"action": "reject", "token": token, "reason": reason},
        )
        self.assertEqual(rejection.status_code, 200)
        self.assertEqual(rejection.get_json()["status"], "payment_rejected")
        self.assertEqual(rejection.get_json()["rejection_reason"], reason)
        self.assertEqual(rejection.get_json()["sms_status"], "sent")
        self.assertEqual(sent_messages[0][0], "9876543210")
        self.assertIn(reason, sent_messages[0][1])

        status_response = self.client.post(
            f"/api/orders/{order['order_id']}/status",
            json={"token": order["receipt_token"]},
        )
        self.assertEqual(status_response.status_code, 200)
        self.assertEqual(status_response.get_json()["status"], "payment_rejected")
        self.assertEqual(status_response.get_json()["rejection_reason"], reason)
        self.assertEqual(status_response.get_json()["items"][0]["id"], "aamer-achar")

    def test_expired_review_link_cannot_show_payment_details(self):
        order_response = self.post_order(
            {
                "name": "মিতা দাস",
                "phone": "9876543210",
                "address": "১২, রবীন্দ্র সরণি, কলকাতা",
                "items": [{"id": "aamer-achar", "quantity": 1}],
            }
        )
        order = order_response.get_json()
        review_token = self.read_review_token(order["order_id"])
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            connection.execute(
                "UPDATE orders SET review_expires_at = '2000-01-01T00:00:00+00:00' WHERE public_id = ?",
                (order["order_id"],),
            )
            connection.commit()

        response = self.client.post(
            f"/api/reviews/{order['order_id']}",
            json={"action": "details", "token": review_token},
        )
        self.assertEqual(response.status_code, 410)

    def read_review_token(self, public_id):
        matching_urls = [url for url in self.review_urls if f"/review/{public_id}#" in url]
        self.assertEqual(len(matching_urls), 1)
        return matching_urls[0].rsplit("#", maxsplit=1)[1]

    def test_invalid_product_and_contact_details_are_rejected(self):
        response = self.post_order(
            {
                "name": "A",
                "phone": "abc1234567",
                "address": "short",
                "items": [{"id": "not-a-product", "quantity": 1}],
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", response.get_json()["fields"])
        self.assertIn("phone", response.get_json()["fields"])
        self.assertIn("address", response.get_json()["fields"])
        self.assertIn("items", response.get_json()["fields"])
        with closing(sqlite3.connect(self.app.config["DATABASE"])) as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 0)

    def test_order_quantity_is_bounded(self):
        response = self.post_order(
            {
                "name": "মিতা দাস",
                "phone": "9876543210",
                "address": "১২, রবীন্দ্র সরণি, কলকাতা",
                "items": [{"id": "aamer-achar", "quantity": 21}],
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("items", response.get_json()["fields"])


if __name__ == "__main__":
    unittest.main()
