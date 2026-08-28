from .connection import get_connection

def get_onboarding(onboarding_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM onboardings WHERE id = ?",
        (onboarding_id,)
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
        (onboarding_id,)
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
        (employee_id,)
    )

    connection.commit()

    onboarding_id = query_result.lastrowid

    connection.close()

    return onboarding_id


def create_onboarding_task(
    onboarding_id,
    task,
    category,
    assigned_to
):
    connection = get_connection()

    query_result = connection.execute(
        """
        INSERT INTO onboarding_tasks
        (onboarding_id, task, category, assigned_to)
        VALUES (?, ?, ?, ?)
        """,
        (
            onboarding_id,
            task,
            category,
            assigned_to
        )
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

    task_updated = query_result.rowcount > 0

    connection.close()

    return task_updated