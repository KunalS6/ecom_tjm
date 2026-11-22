from __future__ import annotations

import json
import html
import os
import re
import secrets
import smtplib
import sqlite3
import uuid
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from contextlib import closing
from email.message import EmailMessage
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from typing import Any

from flask import Flask, abort, jsonify, make_response, render_template, request, send_file, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
from fpdf import FPDF
from PIL import Image, ImageOps, UnidentifiedImageError


ROOT = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("TOKJHAL_DATABASE", ROOT / "instance" / "orders.sqlite3"))
PRIVATE_STORAGE = Path(os.environ.get("TOKJHAL_PRIVATE_STORAGE", ROOT / "instance" / "private"))
FONT_PATH = ROOT / "assets" / "fonts" / "NotoSansBengali-Regular.ttf"
MAX_PROOF_BYTES = 5 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000
ORDER_TOKEN_TTL = timedelta(hours=48)
RECEIPT_TOKEN_TTL = timedelta(days=30)
DEFAULT_OWNER_EMAIL = "tokjhalmistico.2027@gmail.com"

PRODUCTS = [
    {"id": "aamer-achar", "name": "আমের আচার", "english_name": "Aamer Achar", "category": "pickle", "description": "কাঁচা আমের চেনা টক-ঝাল স্বাদ", "price": 220, "icon": "🥭", "label": "জনপ্রিয়"},
    {"id": "lonkar-achar", "name": "লঙ্কার আচার", "english_name": "Lonkar Achar", "category": "pickle", "description": "লঙ্কার ঝাঁজে জমে যাক ভাতের পাতে", "price": 180, "icon": "🌶️", "label": "ঝালপ্রেমীদের"},
    {"id": "lebur-achar", "name": "লেবুর আচার", "english_name": "Lebur Achar", "category": "pickle", "description": "লেবুর টক-মিষ্টি, ঘরোয়া মশলায়", "price": 200, "icon": "🍋", "label": "টক-মিষ্টি"},
    {"id": "kooler-achar", "name": "কুলের আচার", "english_name": "Kooler Achar", "category": "pickle", "description": "কুলের মৌসুমি মিষ্টি-টক মজা", "price": 220, "icon": "🫒", "label": "মৌসুমি স্বাদ"},
    {"id": "gurer-naru", "name": "গুড়ের নাড়ু", "english_name": "Gurer Naru", "category": "homemade", "description": "গুড়ের মিষ্টি গন্ধে উৎসবের আমেজ", "price": 180, "icon": "🥥", "label": "ঘরের প্রিয়"},
    {"id": "papad", "name": "পাপড়", "english_name": "Papad", "category": "homemade", "description": "মুচমুচে আড্ডা কিংবা খাবারের সঙ্গী", "price": 120, "icon": "🫓", "label": "মুচমুচে"},
    {"id": "chinir-naru", "name": "চিনির নাড়ু", "english_name": "Chinir Naru", "category": "homemade", "description": "ছোট্ট মিষ্টি কামড়ে শৈশবের স্মৃতি", "price": 160, "icon": "🍬", "label": "মিষ্টিমুখ"},
    {"id": "sirir-naru", "name": "সিরির নাড়ু", "english_name": "Sirir Naru", "category": "homemade", "description": "পরিচিত ঘরোয়া স্বাদে মিষ্টি মুহূর্ত", "price": 170, "icon": "🍡", "label": "ঘরে তৈরি"},
]
PRODUCT_BY_ID = {product["id"]: product for product in PRODUCTS}


def create_app(database_path: Path | None = None, private_storage_path: Path | None = None) -> Flask:
    app = Flask(__name__, template_folder=".", static_folder=None)
    app.config["DATABASE"] = str(database_path or os.environ.get("TOKJHAL_DATABASE", DATABASE))
    app.config["PRIVATE_STORAGE"] = str(private_storage_path or os.environ.get("TOKJHAL_PRIVATE_STORAGE", PRIVATE_STORAGE))
    app.config["MAX_CONTENT_LENGTH"] = MAX_PROOF_BYTES + 64 * 1024
    app.config["EMAIL_MODE"] = os.environ.get("TOKJHAL_EMAIL_MODE", "console").lower()
    app.config["OWNER_EMAIL"] = os.environ.get("TOKJHAL_OWNER_EMAIL", DEFAULT_OWNER_EMAIL)
    app.config["PUBLIC_BASE_URL"] = (
        os.environ.get("TOKJHAL_PUBLIC_BASE_URL")
        or os.environ.get("RENDER_EXTERNAL_URL")
        or "http://127.0.0.1:5000"
    ).rstrip("/")
    app.config["SMTP_HOST"] = os.environ.get("TOKJHAL_SMTP_HOST", "smtp.gmail.com")
    app.config["SMTP_PORT"] = int(os.environ.get("TOKJHAL_SMTP_PORT", "587"))
    app.config["SMTP_USERNAME"] = os.environ.get("TOKJHAL_SMTP_USERNAME", "")
    app.config["SMTP_PASSWORD"] = os.environ.get("TOKJHAL_SMTP_PASSWORD", "")
    app.config["RESEND_API_KEY"] = os.environ.get("TOKJHAL_RESEND_API_KEY", "")
    app.config["RESEND_FROM"] = os.environ.get("TOKJHAL_RESEND_FROM", "")
    app.config["BREVO_API_KEY"] = os.environ.get("TOKJHAL_BREVO_API_KEY", "")
    app.config["BREVO_FROM_NAME"] = os.environ.get("TOKJHAL_BREVO_FROM_NAME", "Tok Jhal Misti Co.")
    app.config["BREVO_FROM_EMAIL"] = os.environ.get("TOKJHAL_BREVO_FROM_EMAIL", "")
    initialize_database(app.config["DATABASE"])
    Path(app.config["PRIVATE_STORAGE"], "payment-proofs").mkdir(parents=True, exist_ok=True)

    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/styles.css")
    def styles():
        return send_from_directory(ROOT, "styles.css", mimetype="text/css")

    @app.get("/app.js")
    def script():
        return send_from_directory(ROOT, "app.js", mimetype="text/javascript")

    @app.get("/logo.jpeg")
    def logo():
        return send_from_directory(ROOT / "assets", "tok-jhal-misti-logo.jpeg", mimetype="image/jpeg")

    @app.get("/review/<public_id>")
    def review_page(public_id: str):
        if not re.fullmatch(r"[a-f0-9]{24}", public_id):
            abort(404)
        response = make_response(render_template("review.html", public_id=public_id))
        response.headers["Cache-Control"] = "no-store"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @app.get("/order/<public_id>")
    def order_page(public_id: str):
        if not re.fullmatch(r"[a-f0-9]{24}", public_id):
            abort(404)
        language = "en" if request.args.get("lang") == "en" else "bn"
        response = make_response(render_template("order.html", public_id=public_id, language=language))
        response.headers["Cache-Control"] = "no-store"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @app.get("/review.js")
    def review_script():
        return send_from_directory(ROOT, "review.js", mimetype="text/javascript")

    @app.get("/order.js")
    def order_script():
        return send_from_directory(ROOT, "order.js", mimetype="text/javascript")

    @app.errorhandler(RequestEntityTooLarge)
    def uploaded_file_too_large(_error):
        return jsonify(error="স্ক্রিনশট ৫ MB-এর মধ্যে হতে হবে।"), 413

    @app.get("/api/products")
    def list_products():
        return jsonify(PRODUCTS)

    @app.post("/api/orders")
    def create_order():
        proof_upload = request.files.get("payment_proof")
        if request.mimetype == "multipart/form-data":
            try:
                payload: Any = json.loads(request.form.get("order", ""))
            except json.JSONDecodeError:
                payload = None
        else:
            payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="অর্ডারের তথ্য পড়া যায়নি। আবার চেষ্টা করুন।"), 400

        name = payload.get("name")
        phone = payload.get("phone")
        phone_number = re.sub(r"[\s().-]", "", phone) if isinstance(phone, str) else ""
        customer_email = payload.get("email")
        address = payload.get("address")
        note = payload.get("note", "")
        payment_reference = payload.get("payment_reference", "")
        proof_consent = payload.get("proof_consent")
        items = payload.get("items")

        errors: dict[str, str] = {}
        if not isinstance(name, str) or not 2 <= len(name.strip()) <= 80:
            errors["name"] = "নাম ২ থেকে ৮০ অক্ষরের মধ্যে লিখুন।"
        if not re.fullmatch(r"\+?\d{7,15}", phone_number):
            errors["phone"] = "সঠিক ফোন নম্বর লিখুন (৭–১৫টি সংখ্যা)।"
        if (
            not isinstance(customer_email, str)
            or len(customer_email.strip()) > 254
            or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", customer_email.strip())
        ):
            errors["email"] = "সঠিক ইমেল ঠিকানা লিখুন।"
        if not isinstance(address, str) or not 8 <= len(address.strip()) <= 300:
            errors["address"] = "সম্পূর্ণ ঠিকানা লিখুন (কমপক্ষে ৮ অক্ষর)।"
        if not isinstance(note, str) or len(note) > 500:
            errors["note"] = "নোট ৫০০ অক্ষরের মধ্যে লিখুন।"
        if not isinstance(payment_reference, str) or len(payment_reference.strip()) > 100:
            errors["payment_reference"] = "পেমেন্ট রেফারেন্স ১০০ অক্ষরের মধ্যে লিখুন।"
        if proof_upload is not None and proof_upload.filename and proof_consent is not True:
            errors["proof_consent"] = "স্ক্রিনশট পর্যালোচনার সম্মতি আবশ্যক।"

        order_items: list[dict[str, Any]] = []
        if not isinstance(items, list) or not items:
            errors["items"] = "অর্ডারে অন্তত একটি পণ্য যোগ করুন।"
        else:
            quantities: dict[str, int] = {}
            for item in items:
                if not isinstance(item, dict):
                    errors["items"] = "পণ্যের তালিকা সঠিক নয়।"
                    break
                product_id = item.get("id")
                quantity = item.get("quantity")
                if (
                    not isinstance(product_id, str)
                    or product_id not in PRODUCT_BY_ID
                    or type(quantity) is not int
                    or not 1 <= quantity <= 20
                ):
                    errors["items"] = "পণ্যের তালিকা সঠিক নয়।"
                    break
                quantities[product_id] = quantities.get(product_id, 0) + quantity
                if quantities[product_id] > 20:
                    errors["items"] = "একটি পণ্যের সর্বোচ্চ ২০টি অর্ডার করা যাবে।"
                    break
            if "items" not in errors:
                for product_id, quantity in quantities.items():
                    product = PRODUCT_BY_ID[product_id]
                    order_items.append(
                        {
                            "id": product_id,
                            "name": product["name"],
                            "quantity": quantity,
                            "unit_price": product["price"],
                            "line_total": product["price"] * quantity,
                        }
                    )

        if errors:
            return jsonify(error="তথ্যগুলো একবার দেখে নিন।", fields=errors), 400

        total = sum(item["line_total"] for item in order_items)
        public_id = uuid.uuid4().hex[:24]
        review_token = secrets.token_urlsafe(32)
        receipt_token = secrets.token_urlsafe(32)
        expires_at = (datetime.now(timezone.utc) + ORDER_TOKEN_TTL).isoformat()
        receipt_expires_at = (datetime.now(timezone.utc) + RECEIPT_TOKEN_TTL).isoformat()
        proof_path = None
        if proof_upload is not None and proof_upload.filename:
            try:
                proof_path = save_payment_screenshot(proof_upload, Path(app.config["PRIVATE_STORAGE"]))
            except ValueError as error:
                return jsonify(error=str(error), fields={"payment_proof": str(error)}), 400

        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.execute(
                """
                INSERT INTO orders (
                    public_id, customer_name, phone, delivery_address, note, items, total, status,
                    payment_proof_path, review_token_hash, review_expires_at, receipt_token_hash,
                    receipt_token_expires_at, payment_reference, customer_language, customer_email,
                    notification_status, customer_email_status, sms_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, 'awaiting_review', ?, ?, ?, ?, ?, ?, ?, ?, 'pending', 'not_sent', 'not_configured')
                """,
                (
                    public_id,
                    name.strip(),
                    phone_number,
                    address.strip(),
                    note.strip(),
                    json.dumps(order_items, ensure_ascii=False),
                    total,
                    proof_path,
                    token_hash(review_token),
                    expires_at,
                    token_hash(receipt_token),
                    receipt_expires_at,
                    payment_reference.strip(),
                    "en" if payload.get("language") == "en" else "bn",
                    customer_email.strip(),
                ),
            )
            order_id = cursor.lastrowid
            connection.commit()
            order = connection.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()

        review_url = f"{app.config['PUBLIC_BASE_URL']}/review/{public_id}#{review_token}"
        notification_status = send_review_notification(app, order, review_url)
        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            connection.execute(
                "UPDATE orders SET notification_status = ? WHERE id = ?",
                (notification_status, order_id),
            )
            connection.commit()

        message = (
            "আপনার পেমেন্টের প্রমাণ পেয়েছি। যাচাই শেষে অর্ডার নিশ্চিত করা হবে।"
            if payload.get("language") != "en"
            else "Payment proof received. Your order will be confirmed after we verify the payment."
        )
        return jsonify(
            order_id=public_id,
            receipt_token=receipt_token,
            total=total,
            status="awaiting_review",
            notification_status=notification_status,
            message=message,
        ), 201

    @app.post("/api/reviews/<public_id>")
    def review_order(public_id: str):
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="Review details are invalid."), 400
        order, error_response = authorized_order(app, public_id, payload.get("token"), "review_token_hash")
        if error_response:
            return error_response
        if order["status"] != "awaiting_review":
            return jsonify(error="This order has already been reviewed."), 409

        action = payload.get("action")
        if action == "proof":
            return send_private_proof(app, order)
        if action == "details":
            return jsonify(
                order_id=order["public_id"],
                name=order["customer_name"],
                email=order["customer_email"],
                phone=order["phone"],
                address=order["delivery_address"],
                note=order["note"],
                payment_reference=order["payment_reference"],
                items=json.loads(order["items"]),
                total=order["total"],
                has_proof=bool(order["payment_proof_path"]),
                created_at=order["created_at"],
            )
        if action not in {"approve", "reject"}:
            return jsonify(error="Review action is invalid."), 400

        status = "approved" if action == "approve" else "payment_rejected"
        customer_email_token = secrets.token_urlsafe(32)
        customer_email_token_expires_at = (
            datetime.now(timezone.utc) + RECEIPT_TOKEN_TTL
        ).isoformat()
        rejection_reason = ""
        if status == "payment_rejected":
            rejection_reason = payload.get("reason", "").strip() if isinstance(payload.get("reason"), str) else ""
            if not 4 <= len(rejection_reason) <= 500:
                return jsonify(error="Please provide a rejection reason between 4 and 500 characters."), 400
        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            cursor = connection.execute(
                """
                UPDATE orders
                SET status = ?, rejection_reason = ?,
                    approved_at = CASE WHEN ? = 'approved' THEN ? ELSE approved_at END,
                    review_token_hash = NULL,
                    customer_email_token_hash = ?,
                    customer_email_token_expires_at = ?
                WHERE id = ? AND status = 'awaiting_review' AND review_token_hash = ?
                """,
                (
                    status,
                    rejection_reason,
                    status,
                    datetime.now(timezone.utc).isoformat(),
                    token_hash(customer_email_token),
                    customer_email_token_expires_at,
                    order["id"],
                    token_hash(payload["token"]),
                ),
            )
            connection.commit()
            if cursor.rowcount != 1:
                return jsonify(error="This order has already been reviewed."), 409

        reviewed_order = dict(order)
        reviewed_order["customer_language"] = order["customer_language"]
        reviewed_order["customer_email_token"] = customer_email_token
        customer_email_status = send_customer_decision_notification(
            app, reviewed_order, status, rejection_reason
        )
        sms_status = send_order_sms(app, reviewed_order, status, rejection_reason)
        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            connection.execute(
                "UPDATE orders SET customer_email_status = ?, sms_status = ? WHERE id = ?",
                (customer_email_status, sms_status, order["id"]),
            )
            connection.commit()

        return jsonify(
            status=status,
            customer_email_status=customer_email_status,
            sms_status=sms_status,
            order_id=public_id,
            rejection_reason=rejection_reason,
        )

    @app.post("/api/orders/<public_id>/status")
    def order_status(public_id: str):
        payload = request.get_json(silent=True)
        token = payload.get("token") if isinstance(payload, dict) else None
        order, error_response = authorized_order(app, public_id, token, "receipt_token_hash")
        if error_response:
            return error_response
        return jsonify(
            order_id=order["public_id"],
            status=order["status"],
            name=order["customer_name"],
            phone=order["phone"],
            address=order["delivery_address"],
            note=order["note"],
            payment_reference=order["payment_reference"],
            items=json.loads(order["items"]),
            total=order["total"],
            rejection_reason=order["rejection_reason"],
            created_at=order["created_at"],
            notification_status=order["notification_status"],
            customer_email_status=order["customer_email_status"],
            sms_status=order["sms_status"],
        )

    @app.post("/api/orders/<public_id>/receipt.pdf")
    def order_receipt(public_id: str):
        payload = request.get_json(silent=True)
        token = payload.get("token") if isinstance(payload, dict) else None
        order, error_response = authorized_order(app, public_id, token, "receipt_token_hash")
        if error_response:
            return error_response
        if order["status"] != "approved":
            return jsonify(error="The order receipt is only available after payment approval."), 409
        pdf_bytes = build_order_pdf(order)
        return send_file(
            BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"tok-jhal-order-{public_id[:8]}.pdf",
        )

    return app


def token_hash(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


def send_private_proof(app: Flask, order: sqlite3.Row):
    filename = order["payment_proof_path"]
    if not isinstance(filename, str) or not re.fullmatch(r"[a-f0-9]{32}\.jpg", filename):
        abort(404)
    proof_path = Path(app.config["PRIVATE_STORAGE"], "payment-proofs", filename)
    if not proof_path.is_file():
        abort(404)
    response = send_file(proof_path, mimetype="image/jpeg", as_attachment=False, max_age=0)
    response.headers["Cache-Control"] = "no-store, private"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


def authorized_order(app: Flask, public_id: str, token: Any, token_column: str):
    if not re.fullmatch(r"[a-f0-9]{24}", public_id) or not isinstance(token, str) or len(token) > 200:
        return None, (jsonify(error="This link is invalid or has expired."), 404)
    with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
        connection.row_factory = sqlite3.Row
        order = connection.execute("SELECT * FROM orders WHERE public_id = ?", (public_id,)).fetchone()
    if order is None:
        return None, (jsonify(error="This link is invalid or has expired."), 404)
    if token_column == "receipt_token_hash":
        token_options = (
            ("receipt_token_hash", "receipt_token_expires_at"),
            ("customer_email_token_hash", "customer_email_token_expires_at"),
        )
    else:
        token_options = ((token_column, "review_expires_at"),)
    token_digest = token_hash(token)
    matching_expiry = None
    for hash_column, expiry_column in token_options:
        stored_hash = order[hash_column]
        if stored_hash and secrets.compare_digest(stored_hash, token_digest):
            matching_expiry = order[expiry_column]
            break
    if matching_expiry is None:
        return None, (jsonify(error="This link is invalid or has expired."), 404)
    if datetime.fromisoformat(matching_expiry) <= datetime.now(timezone.utc):
        error = "This review link has expired." if token_column == "review_token_hash" else "This order link has expired."
        return None, (jsonify(error=error), 410)
    return order, None


def save_payment_screenshot(upload, private_storage: Path) -> str:
    raw = upload.read(MAX_PROOF_BYTES + 1)
    if not raw or len(raw) > MAX_PROOF_BYTES:
        raise ValueError("স্ক্রিনশট ৫ MB-এর মধ্যে হতে হবে।")
    try:
        with Image.open(BytesIO(raw)) as image:
            if image.format not in {"PNG", "JPEG", "WEBP"}:
                raise ValueError("JPG, PNG অথবা WebP স্ক্রিনশট আপলোড করুন।")
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise ValueError("ছবির আকার খুব বড়। ছোট স্ক্রিনশট আপলোড করুন।")
            image.verify()
        with Image.open(BytesIO(raw)) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            image.thumbnail((2200, 2200))
            output = BytesIO()
            image.save(output, format="JPEG", quality=86, optimize=True)
    except UnidentifiedImageError as error:
        raise ValueError("সঠিক ছবি আপলোড করুন (JPG, PNG অথবা WebP)।") from error
    except Image.DecompressionBombError as error:
        raise ValueError("ছবির আকার খুব বড়। ছোট স্ক্রিনশট আপলোড করুন।") from error
    except OSError as error:
        raise ValueError("ছবিটি পড়া যায়নি। আবার আপলোড করুন।") from error

    filename = f"{uuid.uuid4().hex}.jpg"
    proof_directory = private_storage / "payment-proofs"
    proof_directory.mkdir(parents=True, exist_ok=True)
    (proof_directory / filename).write_bytes(output.getvalue())
    return filename


def send_review_notification(app: Flask, order: sqlite3.Row, review_url: str) -> str:
    email_sender = app.config.get("REVIEW_EMAIL_SENDER")
    if email_sender is not None:
        try:
            email_sender(order, review_url)
        except (OSError, smtplib.SMTPException) as error:
            app.logger.exception("Could not send order review email for %s.", order["public_id"], exc_info=error)
            return "failed"
        return "sent"
    if app.config["EMAIL_MODE"] == "console":
        app.logger.warning("NEW ORDER %s — review link (not emailed): %s", order["public_id"], review_url)
        return "console"
    item_lines = [
        f"- {item['name']} × {item['quantity']} — ₹{item['line_total']}"
        for item in json.loads(order["items"])
    ]
    if order["customer_language"] == "en":
        text_body = (
            f"New order {order['public_id']}\n"
            f"Customer: {order['customer_name']}\nPhone: {order['phone']}\n"
            f"Address: {order['delivery_address']}\n\n"
            + "\n".join(item_lines)
            + f"\n\nTotal: ₹{order['total']}\nReview and accept/reject this order: {review_url}\n"
            "The optional screenshot is available only through this private review page."
        )
    else:
        text_body = (
            f"নতুন অর্ডার: {order['public_id']}\n"
            f"নাম: {order['customer_name']}\nফোন: {order['phone']}\n"
            f"ঠিকানা: {order['delivery_address']}\n\n"
            + "\n".join(item_lines)
            + f"\n\nমোট: ₹{order['total']}\nঅর্ডারটি পর্যালোচনা ও গ্রহণ/বাতিল করতে: {review_url}\n"
            "ঐচ্ছিক স্ক্রিনশটটি শুধু এই ব্যক্তিগত রিভিউ লিংকে দেখা যাবে।"
        )
    html_body = f"""\
        <html>
          <body style="font-family:Arial,sans-serif;color:#263b2b">
            <h1>New order to review</h1>
            <p><strong>Order:</strong> {html.escape(order['public_id'])}</p>
            <p><strong>Customer:</strong> {html.escape(order['customer_name'])} · {html.escape(order['phone'])} · {html.escape(order['customer_email'])}</p>
            <p><strong>Address:</strong> {html.escape(order['delivery_address'])}</p>
            <p><strong>Total:</strong> ₹{order['total']}</p>
            <p><a href="{html.escape(review_url, quote=True)}" style="display:inline-block;padding:12px 20px;background:#d94b32;color:#fff;text-decoration:none;border-radius:8px">Review and accept or reject this order</a></p>
            <p>The customer will see your decision and any rejection reason on their order status page.</p>
          </body>
        </html>
        """
    return send_email_via_provider(
        app,
        recipient=app.config["OWNER_EMAIL"],
        subject=f"New order to review — {order['public_id']}",
        text_body=text_body,
        html_body=html_body,
        order_id=order["public_id"],
        message_kind="owner review",
    )


def send_customer_decision_notification(
    app: Flask,
    order: dict[str, Any],
    status: str,
    rejection_reason: str,
) -> str:
    email_sender = app.config.get("CUSTOMER_EMAIL_SENDER")
    receipt_url = (
        f"{app.config['PUBLIC_BASE_URL']}/order/{order['public_id']}"
        f"?lang={order['customer_language']}#{order['customer_email_token']}"
    )
    if email_sender is not None:
        try:
            email_sender(order, status, rejection_reason, receipt_url)
        except (OSError, smtplib.SMTPException) as error:
            app.logger.exception(
                "Could not send order decision email for %s.",
                order["public_id"],
                exc_info=error,
            )
            return "failed"
        return "sent"
    if app.config["EMAIL_MODE"] == "console":
        app.logger.warning(
            "Order decision email is not configured for order %s.",
            order["public_id"],
        )
        return "console"

    approved = status == "approved"
    if order["customer_language"] == "en":
        subject = (
            f"Your order {order['public_id'][:8].upper()} is confirmed"
            if approved
            else f"Update about your order {order['public_id'][:8].upper()}"
        )
        decision = (
            "Your order has been approved."
            if approved
            else f"Your order could not be accepted. Reason: {rejection_reason}"
        )
        text_body = (
            f"Hello {order['customer_name']},\n\n{decision}\n"
            f"View your order details: {receipt_url}\n"
        )
        html_decision = (
            "<p>Your order has been approved.</p>"
            if approved
            else f"<p>Your order could not be accepted.</p><p><strong>Reason:</strong> {html.escape(rejection_reason)}</p>"
        )
        heading = "Your order is confirmed" if approved else "An update about your order"
    else:
        subject = (
            f"আপনার অর্ডার {order['public_id'][:8].upper()} নিশ্চিত"
            if approved
            else f"আপনার অর্ডার {order['public_id'][:8].upper()} সম্পর্কে আপডেট"
        )
        decision = (
            "আপনার অর্ডারটি গ্রহণ করা হয়েছে।"
            if approved
            else f"আপনার অর্ডারটি গ্রহণ করা যায়নি। কারণ: {rejection_reason}"
        )
        text_body = (
            f"প্রিয় {order['customer_name']},\n\n{decision}\n"
            f"অর্ডারের বিস্তারিত দেখুন: {receipt_url}\n"
        )
        html_decision = (
            "<p>আপনার অর্ডারটি গ্রহণ করা হয়েছে।</p>"
            if approved
            else f"<p>আপনার অর্ডারটি গ্রহণ করা যায়নি।</p><p><strong>কারণ:</strong> {html.escape(rejection_reason)}</p>"
        )
        heading = "আপনার অর্ডার নিশ্চিত" if approved else "আপনার অর্ডার সম্পর্কে আপডেট"
    html_body = f"""\
        <html>
          <body style="font-family:Arial,sans-serif;color:#263b2b">
            <h1>{heading}</h1>
            <p>{html.escape(order['customer_name'])},</p>
            {html_decision}
            <p><a href="{html.escape(receipt_url, quote=True)}">View your order</a></p>
          </body>
        </html>
        """
    return send_email_via_provider(
        app,
        recipient=order["customer_email"],
        subject=subject,
        text_body=text_body,
        html_body=html_body,
        order_id=order["public_id"],
        message_kind="customer decision",
    )


def send_email_via_provider(
    app: Flask,
    recipient: str,
    subject: str,
    text_body: str,
    html_body: str,
    order_id: str,
    message_kind: str,
) -> str:
    email_mode = app.config["EMAIL_MODE"]
    if email_mode == "brevo":
        if not app.config["BREVO_API_KEY"] or not app.config["BREVO_FROM_EMAIL"]:
            app.logger.error("Brevo email mode is enabled but API key/from address are not configured.")
            return "failed"
    elif email_mode == "resend":
        if not app.config["RESEND_API_KEY"] or not app.config["RESEND_FROM"]:
            app.logger.error("Resend email mode is enabled but API key/from address are not configured.")
            return "failed"
    elif email_mode == "smtp":
        if not app.config["SMTP_USERNAME"] or not app.config["SMTP_PASSWORD"]:
            app.logger.error("SMTP mode is enabled but SMTP username/password are not configured.")
            return "failed"
    else:
        app.logger.error("Unsupported email mode: %s", email_mode)
        return "failed"

    message = EmailMessage()
    message["Subject"] = subject
    message["To"] = recipient
    message.set_content(text_body)
    message.add_alternative(html_body, subtype="html")
    try:
        if email_mode == "resend":
            payload = {
                "from": app.config["RESEND_FROM"],
                "to": [recipient],
                "subject": message["Subject"],
                "text": message.get_body(preferencelist=("plain",)).get_content(),
                "html": message.get_body(preferencelist=("html",)).get_content(),
            }
            api_request = urllib.request.Request(
                "https://api.resend.com/emails",
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {app.config['RESEND_API_KEY']}",
                    "Content-Type": "application/json",
                    "Idempotency-Key": f"{order_id}-{message_kind.replace(' ', '-')}",
                },
                method="POST",
            )
            with urllib.request.urlopen(api_request, timeout=15):
                pass
        elif email_mode == "brevo":
            payload = {
                "sender": {
                    "name": app.config["BREVO_FROM_NAME"],
                    "email": app.config["BREVO_FROM_EMAIL"],
                },
                "to": [{"email": recipient}],
                "subject": subject,
                "textContent": text_body,
                "htmlContent": html_body,
            }
            api_request = urllib.request.Request(
                "https://api.brevo.com/v3/smtp/email",
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers={
                    "api-key": app.config["BREVO_API_KEY"],
                    "accept": "application/json",
                    "content-type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(api_request, timeout=15):
                pass
        else:
            message["From"] = app.config["SMTP_USERNAME"]
            with smtplib.SMTP(app.config["SMTP_HOST"], app.config["SMTP_PORT"], timeout=15) as smtp:
                smtp.starttls()
                smtp.login(app.config["SMTP_USERNAME"], app.config["SMTP_PASSWORD"])
                smtp.send_message(message)
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        app.logger.error(
            "Email API rejected order %s with HTTP %s: %s",
            order_id,
            error.code,
            details,
        )
        return "failed"
    except (OSError, urllib.error.URLError, smtplib.SMTPException) as error:
        app.logger.exception(
            "Could not send %s email for order %s.",
            message_kind,
            order_id,
            exc_info=error,
        )
        return "failed"
    return "sent"


def send_order_sms(app: Flask, order: dict[str, Any], status: str, rejection_reason: str = "") -> str:
    sms_sender = app.config.get("SMS_SENDER")
    if sms_sender is not None:
        order_reference = order["public_id"][:8].upper()
        if order["customer_language"] == "bn":
            message = (
                f"টক ঝাল মিষ্টি কো.-এর অর্ডার {order_reference} নিশ্চিত হয়েছে। ধন্যবাদ!"
                if status == "approved"
                else f"টক ঝাল মিষ্টি কো.-এর অর্ডার {order_reference} গ্রহণ করা যায়নি। কারণ: {rejection_reason}"
            )
        else:
            message = (
                f"Your Tok Jhal Misti Co. order {order_reference} is approved. Thank you!"
                if status == "approved"
                else f"Your Tok Jhal Misti Co. order {order_reference} was not accepted. Reason: {rejection_reason}"
            )
        try:
            sms_sender(order["phone"], message)
        except (OSError, ValueError) as error:
            app.logger.exception("Could not send order status SMS for %s.", order["public_id"], exc_info=error)
            return "failed"
        return "sent"
    app.logger.warning(
        "SMS not sent for order %s: no SMS provider has been selected/configured.",
        order["public_id"],
    )
    return "not_configured"


def build_order_pdf(order: sqlite3.Row) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.add_font("NotoSansBengali", fname=str(FONT_PATH))
    pdf.set_text_shaping(use_shaping_engine=True, script="beng", language="ben")
    pdf.set_font("NotoSansBengali", size=18)
    pdf.set_text_color(35, 75, 45)
    pdf.cell(text="টক ঝাল মিষ্টি কো.")
    pdf.ln(13)
    pdf.set_font("NotoSansBengali", size=14)
    pdf.set_text_color(186, 64, 44)
    pdf.cell(text="অর্ডার নিশ্চিতকরণ")
    pdf.ln(12)
    pdf.set_text_color(41, 56, 33)
    pdf.set_font("NotoSansBengali", size=11)
    pdf.cell(text=f"অর্ডার নম্বর: {order['public_id'][:8].upper()}")
    pdf.ln(8)
    pdf.cell(text=f"তারিখ: {order['approved_at'] or order['created_at']}")
    pdf.ln(12)
    pdf.set_font("NotoSansBengali", size=12)
    pdf.cell(text=f"নাম: {order['customer_name']}")
    pdf.ln(8)
    pdf.cell(text=f"ফোন: {order['phone']}")
    pdf.ln(8)
    pdf.multi_cell(w=0, h=7, text=f"ডেলিভারির ঠিকানা: {order['delivery_address']}")
    if order["payment_reference"]:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=pdf.epw, h=7, text=f"পেমেন্ট রেফারেন্স: {order['payment_reference']}")
    if order["note"]:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=pdf.epw, h=7, text=f"বিশেষ নির্দেশ: {order['note']}")
    pdf.ln(5)
    pdf.set_font("NotoSansBengali", size=11)
    for item in json.loads(order["items"]):
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(
            w=pdf.epw,
            h=7,
            text=f"{item['name']} × {item['quantity']} — ₹{item['line_total']}",
        )
    pdf.ln(3)
    pdf.set_font("NotoSansBengali", size=13)
    pdf.cell(text=f"মোট: ₹{order['total']}")
    pdf.ln(12)
    pdf.set_font("NotoSansBengali", size=10)
    pdf.set_text_color(100, 100, 90)
    pdf.multi_cell(w=0, h=7, text="আমাদের ঘরোয়া স্বাদ বেছে নেওয়ার জন্য ধন্যবাদ।")
    return bytes(pdf.output())


def initialize_database(database_path: str) -> None:
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                delivery_address TEXT NOT NULL,
                note TEXT NOT NULL DEFAULT '',
                items TEXT NOT NULL,
                total INTEGER NOT NULL CHECK (total >= 0),
                status TEXT NOT NULL DEFAULT 'received',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                public_id TEXT,
                payment_proof_path TEXT,
                review_token_hash TEXT,
                review_expires_at TEXT,
                receipt_token_hash TEXT,
                receipt_token_expires_at TEXT,
                payment_reference TEXT NOT NULL DEFAULT '',
                customer_language TEXT NOT NULL DEFAULT 'bn',
                customer_email TEXT NOT NULL DEFAULT '',
                notification_status TEXT NOT NULL DEFAULT 'not_sent',
                customer_email_status TEXT NOT NULL DEFAULT 'not_sent',
                customer_email_token_hash TEXT,
                customer_email_token_expires_at TEXT,
                sms_status TEXT NOT NULL DEFAULT 'not_configured',
                approved_at TEXT,
                rejection_reason TEXT NOT NULL DEFAULT ''
            )
            """
        )
        columns = {
            row[1]
            for row in connection.execute("PRAGMA table_info(orders)").fetchall()
        }
        migrations = {
            "public_id": "TEXT",
            "payment_proof_path": "TEXT",
            "review_token_hash": "TEXT",
            "review_expires_at": "TEXT",
            "receipt_token_hash": "TEXT",
            "receipt_token_expires_at": "TEXT",
            "payment_reference": "TEXT NOT NULL DEFAULT ''",
            "customer_language": "TEXT NOT NULL DEFAULT 'bn'",
            "customer_email": "TEXT NOT NULL DEFAULT ''",
            "notification_status": "TEXT NOT NULL DEFAULT 'not_sent'",
            "customer_email_status": "TEXT NOT NULL DEFAULT 'not_sent'",
            "customer_email_token_hash": "TEXT",
            "customer_email_token_expires_at": "TEXT",
            "sms_status": "TEXT NOT NULL DEFAULT 'not_configured'",
            "approved_at": "TEXT",
            "rejection_reason": "TEXT NOT NULL DEFAULT ''",
        }
        for column, definition in migrations.items():
            if column not in columns:
                connection.execute(f"ALTER TABLE orders ADD COLUMN {column} {definition}")
        connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_orders_public_id ON orders(public_id)")
        connection.commit()


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
