import os
from datetime import date

import psycopg


def connect() -> psycopg.Connection:
    # Credentials come from .env loaded into the shell, never from code
    return psycopg.connect(
        host="localhost",
        port=5432,
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
    )


def clean_value(raw: str) -> str | None:
    """Return None for Berka's missing-value markers: "", " " and "?"."""
    value = raw.strip()
    if value in ("", "?"):
        return None
    return value


def parse_date(raw: str) -> date:
    """Convert Berka's YYMMDD (optionally followed by " 00:00:00") to a date."""
    yymmdd = raw.strip()[:6]
    # All Berka event dates fall in 1993-1998, so the century is always 19xx
    year = 1900 + int(yymmdd[0:2])
    month = int(yymmdd[2:4])
    day = int(yymmdd[4:6])
    return date(year, month, day)


def main() -> None:
    with connect() as conn:
        version = conn.execute("select version()").fetchone()[0]
        print(f"Connected: {version}")


if __name__ == "__main__":
    main()
