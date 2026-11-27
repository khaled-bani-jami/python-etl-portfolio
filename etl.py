"""Load users from a public API into SQLite, cleaned with pandas."""
import argparse
import logging
import sqlite3

import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
LOG_FILE = "etl.log"


def extract(url=API_URL):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_domain(email):
    # None for anything that isn't a plain name@host string
    if not isinstance(email, str) or "@" not in email:
        return None
    return email.split("@")[-1].lower()


def transform(users):
    df = pd.DataFrame(users)
    df["city"] = df["address"].apply(lambda a: a.get("city"))
    df["email_domain"] = df["email"].apply(get_domain)
    return df[["id", "name", "email", "city", "email_domain"]]


def load(df, db_file, table="users"):
    # replace, so a rerun doesn't duplicate rows
    with sqlite3.connect(db_file) as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)


def main():
    parser = argparse.ArgumentParser(description="Users ETL")
    parser.add_argument("--db", default="company.db", help="SQLite file")
    args = parser.parse_args()

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    try:
        users = extract()
        logging.info("extracted %d users", len(users))

        df = transform(users)
        load(df, args.db)
        logging.info("loaded %d rows into %s", len(df), args.db)
        print(f"Loaded {len(df)} rows into {args.db}")
    except requests.exceptions.RequestException:
        logging.exception("extract failed")
        print("Extract failed, see etl.log")
    except Exception:
        logging.exception("pipeline failed")
        print("Pipeline failed, see etl.log")


if __name__ == "__main__":
    main()
