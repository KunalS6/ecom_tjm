# Environment, dependencies, and order-flow notes

## Verified local environment

- **OS:** Windows
- **Python:** 3.13.3 (the code uses Python 3.10+ syntax)
- **SQLite:** 3.49.1, included with Python's standard library
- **Browser:** plain JavaScript, HTML, and CSS; no Node.js or front-end build step
- **Branding:** supplied logo at `assets\tok-jhal-misti-logo.jpeg`
- **PDF font:** bundled Noto Sans Bengali static font and its OFL license at `assets\fonts`
- **Optional storefront fonts:** Hind Siliguri and Noto Serif Bengali from Google Fonts; system fallbacks are included

## Install and run on Windows

Run these commands from the project directory:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python server.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). Stop the server with `Ctrl+C` in its terminal. To use another port, set `$env:PORT` before starting the server.

Optional local paths can be set before launch:

```powershell
$env:TOKJHAL_DATABASE = "D:\tok-jhal-test\orders.sqlite3"
$env:TOKJHAL_PRIVATE_STORAGE = "D:\tok-jhal-test\private"
```

No payment number or UPI destination is configured or displayed. Customers are told not to transfer money before receiving payment instructions from the business.

## Exact Python dependencies

These are pinned in `requirements.txt` and were installed in the verified virtual environment:

| Package | Version | Purpose |
|---|---:|---|
| Flask | 3.1.3 | HTTP routes, JSON API, templates |
| blinker | 1.9.0 | Flask signals |
| click | 8.5.1 | Flask command-line support |
| itsdangerous | 2.2.0 | Flask signed-data utilities |
| Jinja2 | 3.1.6 | HTML template rendering |
| MarkupSafe | 3.0.4 | Safe HTML strings |
| Werkzeug | 3.1.9 | Flask development server and HTTP utilities |
| Pillow | 12.3.0 | Validate, normalize, and re-encode uploaded screenshots |
| fpdf2 | 2.9.0 | Generate order confirmation PDFs |
| fonttools | 4.68.0 | PDF font support dependency |
| uharfbuzz | 0.57.0 | Bengali text shaping in PDFs |

SQLite, JSON, email composition, token generation, and browser interactions use the Python standard library or browser APIs. No real email or SMS service dependency is installed.

## Order and review workflow

1. Checkout saves the customer's name, phone, address, note, chosen products, prices, and total to SQLite at `instance\orders.sqlite3`.
2. Payment reference and screenshot are optional until the business supplies payment instructions. If attached, a screenshot must be JPEG, PNG, or WebP and at most 5 MB; it is re-encoded to remove metadata and stored outside the public website directory.
3. Configure Gmail SMTP below to email the owner a private review link. By default, the link is printed in the Flask terminal and **not emailed**. Review links expire after 48 hours. Do not share links or terminal output.
4. The reviewer accepts or rejects the order from the private review page. Rejection requires a reason. The customer status link shows all order details, decision, and rejection reason; accepted orders can download a Bengali PDF invoice.
5. SMS is attempted after either decision only when a sender is configured. Approval SMS confirms the order; rejection SMS includes the reviewer-provided reason. Receipt tokens expire after 30 days.

Use fictional customer information during local testing. The local development server, SQLite database, and local screenshot storage are not a secure production service.

## Optional Gmail SMTP for local testing

Email delivery is off by default. To send review links using a Gmail account, first enable 2-Step Verification and create an app password in the account's security settings. Never put the account password in source code or commit it. Set these variables in the same PowerShell terminal before starting Flask:

```powershell
$env:TOKJHAL_EMAIL_MODE = "smtp"
$env:TOKJHAL_OWNER_EMAIL = "tokjhalmistico.2027@gmail.com"
$env:TOKJHAL_SMTP_USERNAME = "your-sender@gmail.com"
$env:TOKJHAL_SMTP_PASSWORD = "your-16-character-app-password"
$env:TOKJHAL_PUBLIC_BASE_URL = "http://127.0.0.1:5000"
python server.py
```

Use the app password only in your local environment. A review email includes an HTML button linking to the private, expiring review page; accept/reject actions happen on that page, and the optional screenshot is not attached to email. The default local URL works only on the computer running the app, not on a phone or another computer. SMTP delivery has not been tested with real credentials.

## SMS and production readiness

No SMS provider has been selected or configured, so SMS will not actually be delivered yet. The code calls the `SMS_SENDER` callback with an approval confirmation or rejection reason; connect this to a provider and configure its credentials before launch.

Do not deploy this prototype to accept actual orders. Before production, the business must verify its real payment destination and prices, choose and configure an SMS provider, provide monitored email, and arrange HTTPS, a production WSGI server, persistent private database and object storage, backups, access controls, retention/deletion policy, monitoring, and recovery procedures. Review the privacy and payment-handling requirements for the operating region. No hosting provider or free tier makes the current local storage configuration production-ready.

## Hosting options for a preview

Free plans change; check the current terms and quotas before use. These are for a disposable demo, not reliable order handling:

- [Render](https://render.com/pricing): Python web-service preview; free services may sleep and local files are ephemeral.
- [Supabase](https://supabase.com/pricing): hosted Postgres and storage that could be evaluated for a separate persistent-data setup; free projects have quotas and inactivity behavior.
- [PythonAnywhere](https://www.pythonanywhere.com/pricing/): free Python web-app option for an introductory preview; check current outbound network restrictions before relying on SMTP.
- [Railway](https://railway.com/pricing): trial/credit-based option; not an unlimited free host.

The current app is built around local SQLite and local private files, so do not simply upload it to an ephemeral free web service and treat it as a live shop. For real orders, budget for persistent managed storage, secure operations, and backups.
