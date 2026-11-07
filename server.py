from __future__ import annotations

import json
import os
import re
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, request, send_from_directory


ROOT = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("TOKJHAL_DATABASE", ROOT / "instance" / "orders.sqlite3"))

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


def create_app(database_path: Path | None = None) -> Flask:
    app = Flask(__name__, template_folder=".", static_folder=None)
    app.config["DATABASE"] = str(database_path or DATABASE)
    initialize_database(app.config["DATABASE"])

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

    @app.get("/api/products")
    def list_products():
        return jsonify(PRODUCTS)

    @app.post("/api/orders")
    def create_order():
        payload: Any = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="অর্ডারের তথ্য পড়া যায়নি। আবার চেষ্টা করুন।"), 400

        name = payload.get("name")
        phone = payload.get("phone")
        phone_number = re.sub(r"[\s().-]", "", phone) if isinstance(phone, str) else ""
        address = payload.get("address")
        note = payload.get("note", "")
        items = payload.get("items")

        errors: dict[str, str] = {}
        if not isinstance(name, str) or not 2 <= len(name.strip()) <= 80:
            errors["name"] = "নাম ২ থেকে ৮০ অক্ষরের মধ্যে লিখুন।"
        if not re.fullmatch(r"\+?\d{7,15}", phone_number):
            errors["phone"] = "সঠিক ফোন নম্বর লিখুন (৭–১৫টি সংখ্যা)।"
        if not isinstance(address, str) or not 8 <= len(address.strip()) <= 300:
            errors["address"] = "সম্পূর্ণ ঠিকানা লিখুন (কমপক্ষে ৮ অক্ষর)।"
        if not isinstance(note, str) or len(note) > 500:
            errors["note"] = "নোট ৫০০ অক্ষরের মধ্যে লিখুন।"

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
        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            cursor = connection.execute(
                """
                INSERT INTO orders (customer_name, phone, delivery_address, note, items, total)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    name.strip(),
                    phone_number,
                    address.strip(),
                    note.strip(),
                    json.dumps(order_items, ensure_ascii=False),
                    total,
                ),
            )
            connection.commit()
            order_id = cursor.lastrowid

        return jsonify(order_id=order_id, total=total, message="আপনার অর্ডারটি আমরা পেয়েছি।"), 201

    return app


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
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
