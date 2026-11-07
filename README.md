# Tok Jhal Misti Co.

A Bengali-first storefront for homemade pickles, sweets, and papad. The site includes the supplied logo, Bengali/English language switch, product search and filters, a shopping bag, and an order-review flow.

## Run locally

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python server.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000). To stop it, press `Ctrl+C` in the terminal running Flask.

## Order review flow

Checkout saves the customer details and order items in SQLite, then sends the business a private review link by email when SMTP is configured. The reviewer can accept the order or reject it with a required reason. The customer status page shows the decision and the full order; accepted orders can download a Bengali invoice. An optional payment screenshot can be attached and is stored privately.

The payment number is intentionally not shown or configured yet. Customers are warned not to send money until the business shares payment instructions. Email defaults to a terminal log until Gmail SMTP is configured. SMS requires an SMS provider and credentials; the app will send the approval or rejection reason through the configured sender. See [ENVIRONMENT.md](ENVIRONMENT.md) for setup, dependencies, and limitations.

This is a **local prototype, not ready for real customer data or payments**. Configure email, SMS, secure hosting, persistent storage, backups, and the real payment destination before launch.

The sample product prices are placeholders; set actual prices and pack sizes before any real orders.
