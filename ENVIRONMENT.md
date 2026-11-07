# Environment and dependencies

## Application

- **Primary language:** Python 3.10 or newer; verified with Python 3.13.3 on Windows
- **Web framework:** Flask 3.1.3
- **Database:** SQLite 3.49.1, included with Python's standard library
- **Browser code:** plain JavaScript, HTML, and CSS; no Node.js or front-end build step
- **Branding:** supplied Tok Jhal Misti Co. logo at `assets\tok-jhal-misti-logo.jpeg`
- **Optional fonts:** Hind Siliguri and Noto Serif Bengali from Google Fonts; system fallbacks are included

## Install and run on Windows

From the project directory, create and activate a virtual environment, install the Python dependencies, and start the Flask server:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python server.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). To use another port, set `$env:PORT` before running `python server.py`.

To keep the SQLite database somewhere other than `instance\orders.sqlite3`, set `$env:TOKJHAL_DATABASE` to its full path before starting the server.

## Dependency list

`requirements.txt` pins the direct framework dependency and its resolved transitive dependencies for a reproducible installation:

- `Flask==3.1.3` — HTTP routes, JSON API, and HTML template rendering.
- `blinker==1.9.0` — Flask signals.
- `click==8.5.1` — Flask command-line support.
- `itsdangerous==2.2.0` — signed data utilities used by Flask.
- `Jinja2==3.1.6` — HTML template rendering.
- `MarkupSafe==3.0.4` — safe HTML string handling for Jinja.
- `Werkzeug==3.1.9` — Flask's WSGI server and HTTP utilities.

Order storage (`sqlite3`), JSON encoding, input validation, and all website interactions use the Python standard library or browser APIs; there are no payment, messaging, or JavaScript package dependencies.

## Orders, demo values, and production setup

Orders submitted through the checkout are saved to the local SQLite database. The site does not yet connect to a payment gateway, delivery provider, WhatsApp account, or order-management dashboard. The displayed INR prices are example values, not verified business prices; product pack sizes and delivery charges also need to be set by the business. Update the product records in `server.py` before taking real orders. The checkout currently asks the business to follow up with the customer by phone.

The development server in `server.py` is intended for local preview, not production hosting. Before deployment, choose a production WSGI server and hosting provider, configure HTTPS and backups for the order database, and establish an appropriate customer-data retention and privacy policy.