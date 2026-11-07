# Tok Jhal Misti Co.

A Bengali-first storefront for homemade pickles, sweets, and papad. It includes the Tok Jhal Misti Co. logo, a Bengali/English language switch, product search and filters, a shopping bag, and an SQLite-backed checkout.

## Start the website

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python server.py
```

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000). Setup, dependency, database, and production notes are in [ENVIRONMENT.md](ENVIRONMENT.md).

The sample product prices are placeholders; set the actual prices and pack sizes in `server.py` before accepting real orders.
