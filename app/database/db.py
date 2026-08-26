import sqlite3
from pathlib import Path

#BASE_DIR : IT-AUTOMATION-POC
#DATABASE_DIR: IT-AUTOMATION-POC/data
#DATABASE_FILE: IT-AUTOMATION-POC/data/automation.db
#SCHEMA_FILE: IT-AUTOMATION-POC/app/database/schema.sql

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_DIR = BASE_DIR / "data"
DATABASE_FILE = DATABASE_DIR / "automation.db"
SCHEMA_FILE = Path(__file__).resolve().parent / "schema.sql"

# Gives us a connection to the SQLite database
def get_connection():
    DATABASE_DIR.mkdir(exist_ok=True)
    connection = sqlite3.connect(DATABASE_FILE)

    # This controls how SQLite returns rows.
    connection.row_factory = sqlite3.Row

    # Enable foreign key enforcement
    connection.execute("PRAGMA foreign_keys = ON")

    return connection

def initialize_database():
    connection = get_connection()

    # sends that SQL to SQLite and executes it.
    with open(SCHEMA_FILE, "r", encoding="utf-8") as schema:
        connection.executescript(schema.read())

    connection.commit()
    connection.close()

def create_employee(first_name, last_name, department, job_title, manager, start_date):
    connection = get_connection()

    connection.execute(
        "INSERT INTO employees (first_name,  last_name, department, job_title, manager, start_date) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (first_name, last_name, department, job_title, manager, start_date)
    )
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()

    create_employee("John", "Doe", "IT", "System Administrator", "Jane Doe", "2026-09-01")
    print("Employee created")
    # print(f"Database initialized: {DATABASE_FILE}")