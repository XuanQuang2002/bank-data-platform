import csv
import os
from collections.abc import Iterator
from datetime import date
from pathlib import Path

import psycopg
from psycopg import sql

RAW_DIR = Path("data/raw")

TABLES = [
    ("district.asc", "district"),
    ("account.asc", "account"),
    ("client.asc", "client"),
    ("disp.asc", "disp"),
    ("card.asc", "card"),
    ("loan.asc", "loan"),
    ("order.asc", "permanent_order"),
    ("trans.asc", "trans"),
]

DATE_COLUMNS = {"date", "issued"}

TRUNCATE_SQL = """
    truncate berka.district, berka.account, berka.client, berka.disp,
             berka.card, berka.loan, berka.permanent_order, berka.trans
"""


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


def mask_birth_number(birth_number: str) -> str:
    """Hide the PII in a birth_number, keeping only its length visible."""
    return "*" * len(birth_number)


def mask_row(header: list[str], row: list[str]) -> list[str]:
    """Return a copy of the row that is safe to print."""
    return [
        mask_birth_number(value) if column == "birth_number" else value
        for column, value in zip(header, row)
    ]


def convert_row(header: list[str], row: list[str]) -> list[str | date | None]:
    """Clean every value and turn date columns into real dates."""
    values: list[str | date | None] = []
    for column, raw in zip(header, row):
        value = clean_value(raw)
        if value is not None and column in DATE_COLUMNS:
            value = parse_date(value)
        values.append(value)
    return values


def read_rows(path: Path) -> Iterator[list[str | date | None]]:
    """Yield converted rows one at a time, so the 1M-row file never sits in memory."""
    with path.open(newline="") as file:
        reader = csv.reader(file, delimiter=";")
        header = next(reader)
        for line_number, row in enumerate(
            reader, start=2
        ):  # start=2 to account for header line
            try:
                yield convert_row(header, row)
            except ValueError as e:
                safe_row = mask_row(header, row)
                raise ValueError(f"{path.name} line {line_number}: {safe_row}") from e


def load_table(cursor: psycopg.Cursor, path: Path, table: str) -> int:
    statement = sql.SQL("copy berka.{} from stdin").format(sql.Identifier(table))
    count = 0
    with cursor.copy(statement) as copy:
        for row in read_rows(path):
            copy.write_row(row)
            count += 1
    return count


def load_all(conn: psycopg.Connection, raw_dir: Path) -> dict[str, int]:
    counts = {}
    with conn.cursor() as cursor:
        cursor.execute(TRUNCATE_SQL)
        for file_name, table in TABLES:
            counts[table] = load_table(cursor, raw_dir / file_name, table)
    return counts


def main() -> None:
    with connect() as conn:
        counts = load_all(conn, RAW_DIR)
    for table, count in counts.items():
        print(f"Loaded {count} rows into {table}")


if __name__ == "__main__":
    main()
