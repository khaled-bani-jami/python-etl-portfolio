# python-etl-portfolio

Small ETL job: pulls users from a public API, cleans them with pandas and
loads them into SQLite. Uses public data only.

```
API -> pandas -> SQLite
```

## Run

```
py -3.13 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python etl.py --db company.db
```

Progress and errors are written to `etl.log`.

## Stack

Python 3.13, requests, pandas, sqlite3
