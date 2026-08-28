import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_DIR = BASE_DIR / "data"
DATABASE_FILE = DATABASE_DIR / "automation.db"
SCHEMA_FILE = Path(__file__).resolve().parent / "schema.sql"


def get_connection():
    DATABASE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    connection = get_connection()

    with open(SCHEMA_FILE, "r", encoding="utf-8") as schema:
        connection.executescript(schema.read())

    connection.commit()
    connection.close()