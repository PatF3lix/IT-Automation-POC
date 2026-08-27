import sqlite3, json
from pathlib import Path

######################################### DB connection #########################################

#BASE_DIR : IT-AUTOMATION-POC
#DATABASE_DIR: IT-AUTOMATION-POC/data
#DATABASE_FILE: IT-AUTOMATION-POC/data/automation.db
#SCHEMA_FILE: IT-AUTOMATION-POC/app/database/schema.sql

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE_DIR = BASE_DIR / "data"
DATABASE_FILE = DATABASE_DIR / "automation.db"
SCHEMA_FILE = Path(__file__).resolve().parent / "schema.sql"


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

######################################### Employees #########################################

def create_employee(first_name, last_name, department, job_title, manager, start_date):
    connection = get_connection()

    connection.execute(
        "INSERT INTO employees (first_name,  last_name, department, job_title, manager, start_date) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (first_name, last_name, department, job_title, manager, start_date)
    )
    connection.commit()
    connection.close()

def get_employee(employee_id):
    connection = get_connection()

    query_result = connection.execute("SELECT * FROM employees WHERE id = ?",
                       (employee_id,)
    )

    # fetchone() takes the result of your SQL query and retrieves the first matching row.
    employee = query_result.fetchone()

    connection.close()

    return employee

def update_employee(employee_id, updates):
    connection = get_connection()

    allowed_fields = {
        "first_name",
        "last_name",
        "department",
        "job_title",
        "manager",
        "start_date",
        "status"
    }

    # Only allow fields that actually exist in the employee table
    updates = {
        field: value
        for field, value in updates.items()
        if field in allowed_fields
    }

    if not updates:
        connection.close()
        return False

    set_clause = ", ".join(
        f"{field} = ?" for field in updates
    )

    query = f"""
        UPDATE employees
        SET {set_clause}
        WHERE id = ?
    """

    values = tuple(updates.values()) + (employee_id,)

    connection.execute(query, values)
    connection.commit()
    connection.close()

    return True

def delete_employee(employee_id):
    connection = get_connection()

    connection.execute(
        "DELETE FROM employees Where id = ?",
        (employee_id,)
    )

    connection.commit()
    connection.close()

######################################### Tickets #########################################

def create_ticket(ticket_number, employee_id, title, description):
    connection = get_connection()

    query_result = connection.execute(
        """
        INSERT INTO tickets
        (ticket_number, employee_id, title, description)
        VALUES (?, ?, ?, ?)
        """,
        (ticket_number, employee_id, title, description)
    )

    connection.commit()

    # return the id of the row just inserted
    ticket_id = query_result.lastrowid

    connection.close()

    return ticket_id

def get_ticket(ticket_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    ticket = query_result.fetchone()

    connection.close()

    return ticket

def update_ticket(ticket_id, updates):

    connection = get_connection()

    allowed_fields = {
        "ticket_number",
        "title",
        "description",
        "status"
    }

    updates = {
        field: value
        for field, value in updates.items()
        if field in allowed_fields
    }

    set_clause = ", ".join(
        f"{field} = ?" for field in updates
    )

    query = f"""
            UPDATE tickets
            SET {set_clause}
            WHERE id = ?
        """

    values = tuple(updates.values()) + (ticket_id,)

    connection.execute(query, values)
    connection.commit()
    connection.close()

    return True

def update_ticket_ai(ticket_id, category, priority, assigned_team, summary, recommendations):
    connection = get_connection()

    connection.execute(
        """
        UPDATE tickets
        SET category = ?,
            priority = ?,
            assigned_team = ?,
            ai_summary = ?,
            ai_recommendations = ?
        WHERE id = ?
        """,
        (
            category,
            priority,
            assigned_team,
            summary,
            json.dumps(recommendations),
            ticket_id
        )
    )

    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()

    ticket = get_ticket(1)

    if ticket:
        print(ticket["ticket_number"])
        print(ticket["title"])
        print(ticket["description"])
    else:
        print("Ticket not found")

    # create_employee("John", "Doe", "IT", "System Administrator", "Jane Doe", "2026-09-01")
    # create_employee("Jane", "Smith", "IT", "Programmeur", "John Doe", "2026-09-02")

    # print("Employee created")

    # employee = get_employee(1)
    # if employee is not None:
    #     print(employee["first_name"])
    #     print(employee["last_name"])
    #     print(employee["department"])
    #     print(employee["job_title"])
    # else:
    #     print("No employee with that id was found")

    # employee = get_employee(2)
    # if employee is not None:
    #     print(employee["first_name"])
    #     print(employee["last_name"])
    #     print(employee["department"])
    #     print(employee["job_title"])
    # else:
    #     print("No employee with that id was found")

    # update_result = update_employee(1, {"department": "Cybersecurity",
    #                                     "job_title": "Security Analyst"})

    # print("Update successful:", update_result)

    # delete_employee(1)


    print(f"Database initialized: {DATABASE_FILE}")