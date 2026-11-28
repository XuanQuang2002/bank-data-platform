import os

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


def main() -> None:
    with connect() as conn:
        version = conn.execute("select version()").fetchone()[0]
        print(f"Connected: {version}")


if __name__ == "__main__":
    main()
