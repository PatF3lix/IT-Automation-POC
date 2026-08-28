from .connection import get_connection


def get_asset(asset_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM assets WHERE id = ?",
        (asset_id,)
    )

    asset = query_result.fetchone()

    connection.close()

    return asset


def get_employee_assets(employee_id):
    connection = get_connection()

    query_result = connection.execute(
        "SELECT * FROM assets WHERE assigned_to = ?",
        (employee_id,)
    )

    assets = query_result.fetchall()

    connection.close()

    return assets


def create_asset(
    asset_tag,
    asset_type,
    manufacturer,
    serial_number,
    assigned_to,
    purchase_date,
    warranty_end
):
    connection = get_connection()

    query_result = connection.execute(
        """
        INSERT INTO assets
        (
            asset_tag,
            asset_type,
            manufacturer,
            serial_number,
            assigned_to,
            purchase_date,
            warranty_end
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            asset_tag,
            asset_type,
            manufacturer,
            serial_number,
            assigned_to,
            purchase_date,
            warranty_end
        )
    )

    connection.commit()

    asset_id = query_result.lastrowid

    connection.close()

    return asset_id


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

    query_result = connection.execute(query, values)

    connection.commit()

    asset_updated = query_result.rowcount > 0

    connection.close()

    return asset_updated


def delete_asset(asset_id):
    connection = get_connection()

    query_result = connection.execute(
        "DELETE FROM assets WHERE id = ?",
        (asset_id,)
    )

    connection.commit()

    asset_deleted = query_result.rowcount > 0

    connection.close()

    return asset_deleted