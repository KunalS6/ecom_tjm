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
| gunicorn | 23.0.0 | Production WSGI server used by Render |

SQLite, JSON, email composition, token generation, and browser interactions use the Python standard library or browser APIs. No real email or SMS service dependency is installed.

## Order and review workflow

1. Checkout saves the customer's name, phone, address, note, chosen products, prices, and total to SQLite at `instance\orders.sqlite3`.
2. Payment reference and screenshot are optional until the business supplies payment instructions. If attached, a screenshot must be JPEG, PNG, or WebP and at most 5 MB; it is re-encoded to remove metadata and stored outside the public website directory.
3. Configure email delivery below to email the owner a private review link. In local console mode the link is printed in the Flask terminal and **not emailed**. Review links expire after 48 hours. Do not share links or terminal output.
4. The reviewer accepts or rejects the order from the private review page. Rejection requires a reason. The customer status link shows all order details, decision, and rejection reason; accepted orders can download a Bengali PDF invoice.
5. SMS is attempted after either decision only when a sender is configured. Approval SMS confirms the order; rejection SMS includes the reviewer-provided reason. Receipt tokens expire after 30 days.

Use fictional customer information during local testing. The local development server, SQLite database, and local screenshot storage are not a secure production service.

## Email delivery for order review

New-order review email is sent to `tokjhalmistico.2027@gmail.com`. The message includes the order details and a secure link to accept or reject the order. The review link uses `TOKJHAL_PUBLIC_BASE_URL`; on Render the app automatically uses Render's `RENDER_EXTERNAL_URL`.

Render deployments use the Resend HTTPS API because the Render service could not establish a connection to Gmail SMTP. Create a Resend account and API key, then configure:

- `TOKJHAL_EMAIL_MODE`: `resend`
- `TOKJHAL_RESEND_API_KEY`: the Resend API key (keep it secret)
- `TOKJHAL_RESEND_FROM`: a sender address authorized by Resend
- `TOKJHAL_OWNER_EMAIL`: the inbox that receives review links

For production recipients, verify a domain with Resend and use a sender at that domain. Do not put credentials in source code, `render.yaml`, or GitHub. SMTP remains available for local environments that can reach their SMTP host.

For local testing, set these variables in the same PowerShell terminal before starting Flask:

```powershell
$env:TOKJHAL_EMAIL_MODE = "resend"
$env:TOKJHAL_OWNER_EMAIL = "tokjhalmistico.2027@gmail.com"
$env:TOKJHAL_RESEND_API_KEY = "your-resend-api-key"
$env:TOKJHAL_RESEND_FROM = "Tok Jhal Misti <orders@your-verified-domain.example>"
$env:TOKJHAL_PUBLIC_BASE_URL = "http://127.0.0.1:5000"
python server.py
```

### Render setup

The root `render.yaml` defines the Flask web service and sets Resend email mode and the business recipient. It declares the Resend API key and sender as dashboard-provided values (`sync: false`), so no credentials are stored in the repository.

1. Create a Resend account, verify a sending domain, and create an API key.
2. In Render's service **Environment** settings, set `TOKJHAL_RESEND_API_KEY` and `TOKJHAL_RESEND_FROM` using the key and verified sender address.
3. Deploy or trigger a redeploy. Review Render logs for email API errors.
4. Place a test order using your own test details. Confirm `notification_status` is `sent` and check the business inbox's spam folder. The email's review link opens the private accept/reject page.

Never paste API keys into chat, source code, screenshots, or GitHub. If a key is exposed, revoke it and create a replacement. Render automatically supplies its public URL when creating review links.

## Persistent order and payment-proof storage on Render

The app supports persistent paths through `TOKJHAL_DATABASE` and `TOKJHAL_PRIVATE_STORAGE`. Render's filesystem is ephemeral unless a persistent disk is attached. Render currently requires a paid web service for persistent disks; this repository does not automatically upgrade the service or create a billable disk.

To keep orders and private payment screenshots across deploys/restarts:

1. Upgrade the Render web service to a plan that supports persistent disks and attach a disk mounted at `/var/data`.
2. Set `TOKJHAL_DATABASE` to `/var/data/orders.sqlite3`.
3. Set `TOKJHAL_PRIVATE_STORAGE` to `/var/data/private`.
4. Redeploy and verify that the disk is mounted before accepting new orders.

Without this disk, local SQLite data and uploaded payment proofs may be lost on redeploy/restart. Previously lost orders cannot be recovered from the current service filesystem.

## SMS and production readiness

No SMS provider has been selected or configured, so SMS will not actually be delivered yet. The code calls the `SMS_SENDER` callback with an approval confirmation or rejection reason; connect this to a provider and configure its credentials before launch.

Do not deploy this prototype to accept actual orders until persistent storage and email delivery are configured and verified. Before production, the business must verify its real payment destination and prices, choose and configure an SMS provider, provide monitored email, and arrange HTTPS, persistent database and object storage, backups, access controls, retention/deletion policy, monitoring, and recovery procedures. Review the privacy and payment-handling requirements for the operating region.

## Hosting options for a preview

Free plans change; check the current terms and quotas before use. These are for a disposable demo, not reliable order handling:

- [Render](https://render.com/pricing): Python web-service preview; free services may sleep and local files are ephemeral.
- [Supabase](https://supabase.com/pricing): hosted Postgres and storage that could be evaluated for a separate persistent-data setup; free projects have quotas and inactivity behavior.
- [PythonAnywhere](https://www.pythonanywhere.com/pricing/): free Python web-app option for an introductory preview; check current outbound network restrictions before relying on SMTP.
- [Railway](https://railway.com/pricing): trial/credit-based option; not an unlimited free host.

The current app is built around local SQLite and local private files, so do not simply upload it to an ephemeral free web service and treat it as a live shop. For real orders, budget for persistent managed storage, secure operations, and backups.
