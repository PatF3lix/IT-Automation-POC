from ..database import get_employee, get_asset, update_asset, get_employee_assets

def assign_asset(asset_id, employee_id):
    asset = get_asset(asset_id)

    if not asset:
        return False

    employee = get_employee(employee_id)

    if not employee:
        return False

    if asset["status"] != "Available":
        return False

    update_asset(asset_id, {
    "assigned_to": employee_id,
    "status": "Assigned"
    })

    return True

def return_asset(asset_id):
    asset = get_asset(asset_id)

    if not asset:
        return False

    if asset["status"] != "Assigned":
        return False

    update_asset(asset_id, {
        "assigned_to": None,
        "status": "Available"
    })

    return True


if __name__ == "__main__":
    # result = assign_asset(1,1)
    # print("Asset assigned:", result)

    # asset = get_asset(1)
    # print(dict(asset))

    assets = get_employee_assets(1)

    print("Employee 1 assets:")

    for asset in assets:
        print(dict(asset))