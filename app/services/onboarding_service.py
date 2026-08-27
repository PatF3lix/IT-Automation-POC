

def create_onboarding(employee_id):
    employee = get_employee(employee_id)

    if not employee:
        return False

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

def get_onboarding(onboarding_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM onboardings WHERE id = ?",
        (onboarding_id, )
    )

    onboarding = query_result.fetchone()

    connection.close()

    return onboarding

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

if __name__ == "__main__":

    onboarding = get_onboarding(2)

    print("Before:", dict(onboarding))

    result = update_onboarding(
        2,
        {
            "status": "In Progress"
        }
    )

    print("Update successful:", result)

    onboarding = get_onboarding(2)

    print("After:", dict(onboarding))
    # onboarding_id = create_onboarding(1)

    # if onboarding_id:
    #     print("Onboarding created:", onboarding_id)

    #     onboarding = get_onboarding(onboarding_id)

    #     if onboarding:
    #         print("Onboarding:", dict(onboarding))
    #     else:
    #         print("Onboarding not found")

    # else:
    #     print("Employee not found")

    # onboarding_id = create_onboarding(1)

    # if onboarding_id:
    #     print("Onboarding created:", onboarding_id)
    # else:
    #     print("Employee not found")