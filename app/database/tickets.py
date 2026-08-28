import json
from .connection import get_connection


def get_ticket(ticket_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    ticket = query_result.fetchone()

    connection.close()

    return ticket


def get_employee_tickets(employee_id):
    connection = get_connection()

    query_result = connection.execute(
        """
        SELECT * FROM tickets
        WHERE assigned_to = ?
        ORDER BY created_at DESC
        """,
        (employee_id,)
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
        (employee_id,)
    )

    result = query_result.fetchone()

    connection.close()

    return result["ticket_count"]


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

    query_result = connection.execute(query, values)

    connection.commit()

    ticket_updated = query_result.rowcount > 0

    connection.close()

    return ticket_updated


def update_ticket_ai(
    ticket_id,
    category,
    priority,
    assigned_team,
    summary,
    recommendations
):
    connection = get_connection()

    query_result = connection.execute(
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

    ticket_updated = query_result.rowcount > 0

    connection.close()

    return ticket_updated


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


def delete_ticket(ticket_id):
    connection = get_connection()

    query_result = connection.execute(
        "DELETE FROM tickets WHERE id = ?",
        (ticket_id,)
    )

    connection.commit()

    ticket_deleted = query_result.rowcount > 0

    connection.close()

    return ticket_deleted