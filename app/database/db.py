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

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")

    return connection

def initialize_database():
    connection = get_connection()

    # sends that SQL to SQLite and executes it.
    with open(SCHEMA_FILE, "r", encoding="utf-8") as schema:
        connection.executescript(schema.read())

    connection.commit()
    connection.close()

def seed_database():
    # Employees
    create_employee(
        "John",
        "Doe",
        "IT",
        "Senior System Administrator",
        "IT Manager",
        "2026-09-01"
    )

    create_employee(
        "Sarah",
        "Martin",
        "IT",
        "Senior Network Administrator",
        "IT Manager",
        "2026-09-01"
    )

    create_employee(
        "Mike",
        "Brown",
        "IT",
        "Tech Support L2",
        "John Doe",
        "2026-09-02"
    )

    create_employee(
        "Emily",
        "Wilson",
        "IT",
        "Tech Support L2",
        "John Doe",
        "2026-09-02"
    )

    create_employee(
        "Alex",
        "Taylor",
        "IT",
        "Tech Support L3",
        "John Doe",
        "2026-09-02"
    )

    # Assets
    create_asset(
        "LAP-001",
        "Laptop",
        "Dell",
        "DL-SENIOR-001",
        1,
        "2026-08-01",
        "2029-08-01"
    )

    update_asset(1, {
        "status": "Assigned"
    })

    create_asset(
        "LAP-002",
        "Laptop",
        "Lenovo",
        "LN-SENIOR-002",
        2,
        "2026-08-01",
        "2029-08-01"
    )

    update_asset(2, {
        "status": "Assigned"
    })

    # Example onboarding
    onboarding_id = create_onboarding(3)

    create_onboarding_task(
        onboarding_id,
        "Create AD user account",
        "Account",
        "IT Support"
    )

    print("Demo database seeded successfully.")

######################################### Employees #########################################

def get_employee(employee_id):
    connection = get_connection()

    query_result = connection.execute("SELECT * FROM employees WHERE id = ?",
                       (employee_id,)
    )

    employee = query_result.fetchone()

    connection.close()

    return employee

def get_employee_tickets(employee_id):
    connection = get_connection()

    query_result = connection.execute(
        """
        SELECT * FROM tickets 
        WHERE assigned_to = ?
        ORDER BY created_at DESC
        """,
        (employee_id, )
    )

    tickets = query_result.fetchall()

    connection.close()

    return tickets

def get_employee_active_ticket_count(employee_id):
    connection = get_connection()

    query_result = connection.execute(
        """
        SELECT COUNT(*) AS ticket_count
        FROM tickets
        WHERE assigned_to = ?
        AND status NOT IN ('Resolved', 'Closed')
        """,
        (employee_id, )
    )

    result = query_result.fetchone()

    connection.close()

    return result["ticket_count"]

def get_employees_by_department(department):
    connection = get_connection()

    query_result = connection.execute(
        """
        SELECT * FROM employees
        WHERE LOWER(department) = LOWER(?)
        ORDER BY last_name, first_name
        """,
        (department, )
    )

    employees = query_result.fetchall()

    connection.close()

    return employees


def get_all_employees():
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM employees ORDER BY last_name, first_name"
    )

    employees = query_result.fetchall()

    connection.close()

    return employees

def create_employee(first_name, last_name, department, job_title, manager, start_date):
    connection = get_connection()

    connection.execute(
        "INSERT INTO employees (first_name,  last_name, department, job_title, manager, start_date) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (first_name, last_name, department, job_title, manager, start_date)
    )
    connection.commit()
    connection.close()

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

def get_ticket(ticket_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    ticket = query_result.fetchone()

    connection.close()

    return ticket


def create_ticket(employee_id, title, description):
    connection = get_connection()

    query_result = connection.execute(
        """
        INSERT INTO tickets
        (employee_id, title, description)
        VALUES (?, ?, ?)
        """,
        (employee_id, title, description)
    )

    connection.commit()

    ticket_id = query_result.lastrowid

    ticket_number = f"INC-{ticket_id:04d}"

    connection.execute(
        """
        UPDATE tickets
        SET ticket_number = ?
        WHERE id = ?
        """,
        (ticket_number, ticket_id)
    )

    connection.commit()
    connection.close()

    return ticket_id

def update_ticket(ticket_id, updates):

    connection = get_connection()

    allowed_fields = {
        "title",
        "description",
        "status"
    }

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

def delete_ticket(ticket_id):
    connection = get_connection()

    query_result = connection.execute(
        "DELETE FROM tickets WHERE id = ?",
        (ticket_id, )
    )

    connection.commit()

    ticket_deleted = query_result.rowcount > 0

    connection.close()

    return ticket_deleted

def assign_ticket_to_employee(ticket_id, employee_id):
    connection = get_connection()

    query_result = connection.execute(
        """
        UPDATE tickets
        SET assigned_to = ?
        WHERE id = ?
        """,
        (employee_id, ticket_id)
    )

    connection.commit()

    ticket_updated = query_result.rowcount > 0

    connection.close()

    return ticket_updated


######################################### IT Assets #########################################

def create_asset(asset_tag, asset_type, manufacturer, serial_number, assigned_to, purchase_date, warranty_end):
    connection = get_connection()

    query_result = connection.execute(
        """
        INSERT INTO assets
        (asset_tag, asset_type, manufacturer, serial_number, assigned_to, purchase_date, warranty_end)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (asset_tag, asset_type, manufacturer, serial_number, assigned_to, purchase_date, warranty_end)
    )

    connection.commit()

    asset_id = query_result.lastrowid

    connection.close()

    return asset_id


def get_asset(asset_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM assets WHERE id = ?",
        (asset_id, )
    )

    asset = query_result.fetchone()

    connection.close()

    return asset

def get_employee_assets(employee_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM assets WHERE assigned_to = ? ",
        (employee_id, )
    )

    assets = query_result.fetchall()

    connection.close()

    return assets

def update_asset(asset_id, updates):

    connection = get_connection()

    allowed_fields = {
        "asset_tag",
        "asset_type",
        "manufacturer",
        "serial_number",
        "status",
        "assigned_to",
        "purchase_date",
        "warranty_end"
    }

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
            UPDATE assets
            SET {set_clause}
            WHERE id = ?
        """

    values = tuple(updates.values()) + (asset_id,)

    connection.execute(query, values)
    connection.commit()
    connection.close()

    return True

def delete_asset(asset_id):
    connection = get_connection()

    query_result = connection.execute(
        "DELETE FROM assets WHERE id = ?",
                       (asset_id, )
        )

    connection.commit()

    asset_deleted = query_result.rowcount > 0

    connection.close()

    return asset_deleted 

######################################### Onboarding #########################################

def get_onboarding(onboarding_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM onboardings WHERE id = ?",
        (onboarding_id, )
    )

    onboarding = query_result.fetchone()

    connection.close()

    return onboarding

def get_onboarding_tasks(onboarding_id):
    connection = get_connection()

    query_result = connection.execute(
        """
        SELECT * FROM onboarding_tasks
        WHERE onboarding_id = ?
        """,
        (onboarding_id, )
    )

    tasks = query_result.fetchall()

    connection.close()

    return tasks

def create_onboarding(employee_id):
    connection = get_connection()

    query_result = connection.execute(
        """
        INSERT INTO onboardings (employee_id)
        VALUES (?)
        """,
        (employee_id, )
    )

    connection.commit()

    onboarding_id = query_result.lastrowid

    connection.close()

    return onboarding_id

def create_onboarding_task(onboarding_id, task, category, assigned_to):
    connection = get_connection()

    query_result = connection.execute(
        """
        INSERT INTO onboarding_tasks
        (onboarding_id, task, category, assigned_to)
        VALUES (?, ?, ?, ?)
        """,
        (onboarding_id, task, category, assigned_to)
    )

    connection.commit()

    task_id = query_result.lastrowid

    connection.close()

    return task_id

def update_onboarding(onboarding_id, updates):
    connection = get_connection()

    allowed_fields = {
        "status",
        "completed_at"
    }

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
        UPDATE onboardings
        SET {set_clause}
        WHERE id = ?
    """

    values = tuple(updates.values()) + (onboarding_id,)

    query_result = connection.execute(query, values)

    connection.commit()

    onboarding_updated = query_result.rowcount > 0

    connection.close()

    return onboarding_updated


def update_onboarding_task(task_id, updates):
    connection = get_connection()

    allowed_fields = {
        "task",
        "category",
        "assigned_to",
        "status"
    }

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
        UPDATE onboarding_tasks
        SET {set_clause}
        WHERE id = ?
    """

    values = tuple(updates.values()) + (task_id,)
    
    query_result = connection.execute(query, values)

    connection.commit()

    tasks_updated = query_result.rowcount > 0

    connection.close()

    return tasks_updated
    
if __name__ == "__main__":
    initialize_database()
    seed_database()
    print(f"Database initialized: {DATABASE_FILE}")