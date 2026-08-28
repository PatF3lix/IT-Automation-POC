from .connection import get_connection


def get_employee(employee_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,)
    )

    employee = query_result.fetchone()

    connection.close()

    return employee


def get_employees_by_department(department):
    connection = get_connection()

    query_result = connection.execute(
        """
        SELECT * FROM employees
        WHERE LOWER(department) = LOWER(?)
        ORDER BY last_name, first_name
        """,
        (department,)
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


def create_employee(
    first_name,
    last_name,
    department,
    job_title,
    manager,
    start_date
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO employees
        (first_name, last_name, department, job_title, manager, start_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            first_name,
            last_name,
            department,
            job_title,
            manager,
            start_date
        )
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

    query_result = connection.execute(query, values)

    connection.commit()

    employee_updated = query_result.rowcount > 0

    connection.close()

    return employee_updated


def delete_employee(employee_id):
    connection = get_connection()

    query_result = connection.execute(
        "DELETE FROM employees WHERE id = ?",
        (employee_id,)
    )

    connection.commit()

    employee_deleted = query_result.rowcount > 0

    connection.close()

    return employee_deleted