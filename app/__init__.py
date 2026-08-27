import json
from flask import Flask, jsonify, request
from .services.ticket_service import process_ticket
from .services.asset_service import assign_asset, return_asset
from .database.db import (
    get_employee,
    create_ticket,
    get_ticket,
    update_ticket,
    delete_ticket,
    create_asset,
    get_asset,
    update_asset,
    delete_asset,
    get_employee_assets
)
from .services.onboarding_service import (
    start_onboarding,
    get_onboarding_details,
    update_task,
    complete_onboarding
)

app = Flask(__name__)

######################################### FRONT END Routes #####################################

@app.route("/")
def home():
    return "IT Automation POC is running!"

######################################### API Employees Routes #################################

@app.route("/employees/<int:employee_id>")
def get_employee_route(employee_id):
    employee = get_employee(employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({
        "id": employee["id"],
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "department": employee["department"],
        "job_title": employee["job_title"]
    })

@app.route("/employees/<int:employee_id>/assets")
def get_employee_assets_route(employee_id):

    employee_assets = get_employee_assets(employee_id)

    return jsonify({
        "employee_id": employee_id,
        "assets": [dict(asset) for asset in employee_assets]
    })

@app.route("/employees/<int:employee_id>/onboarding", methods=["POST"])
def start_employee_onboarding(employee_id):

    onboarding_id = start_onboarding(employee_id)

    if not onboarding_id:
        return jsonify({"error": "Employee not found"}), 404

    onboarding = get_onboarding_details(onboarding_id)

    return jsonify(onboarding), 201

######################################### API Tickets Routes #################################

@app.route("/tickets", methods=["POST"])
def create_new_ticket_route():

    data = request.get_json()

    ticket_id = create_ticket(
        data["ticket_number"],
        data["employee_id"],
        data["title"],
        data["description"]
    )

    process_ticket(ticket_id)
    ticket = get_ticket(ticket_id)

    return jsonify({
    "id": ticket["id"],
    "ticket_number": ticket["ticket_number"],
    "title": ticket["title"],
    "description": ticket["description"],
    "category": ticket["category"],
    "priority": ticket["priority"],
    "assigned_team": ticket["assigned_team"],
    "ai_summary": ticket["ai_summary"],
    "ai_recommendations": json.loads(ticket["ai_recommendations"])
    }), 201

@app.route("/tickets/<int:ticket_id>")
def get_ticket_route(ticket_id):
    ticket = get_ticket(ticket_id)

    if ticket is None:
        return jsonify({"error": "Ticket not found"}), 404

    return jsonify({
        "id": ticket["id"],
        "ticket_number": ticket["ticket_number"],
        "title": ticket["title"],
        "description": ticket["description"],
        "category": ticket["category"],
        "priority": ticket["priority"],
        "assigned_team": ticket["assigned_team"],
        "ai_summary": ticket["ai_summary"],
        "ai_recommendations": json.loads(ticket["ai_recommendations"])
        })

@app.route("/tickets/<int:ticket_id>", methods=["PUT"])
def update_ticket_route(ticket_id):
    data = request.get_json()

    ticket_updated = update_ticket(ticket_id, data)

    if not ticket_updated:
        return jsonify({"error": "Ticket not found or no valid fields provided"}), 404

    # Re-analyse if the ticket information changed
    if "description" in data or "title" in data:
        process_ticket(ticket_id)

    ticket = get_ticket(ticket_id)

    return jsonify({
        "id": ticket["id"],
        "ticket_number": ticket["ticket_number"],
        "title": ticket["title"],
        "description": ticket["description"],
        "category": ticket["category"],
        "priority": ticket["priority"],
        "assigned_team": ticket["assigned_team"],
        "ai_summary": ticket["ai_summary"],
        "ai_recommendations": json.loads(ticket["ai_recommendations"])
    })

@app.route("/tickets/<int:ticket_id>", methods=["DELETE"])
def delete_ticket_route(ticket_id):
    ticket = get_ticket(ticket_id)
    ticket_deleted = delete_ticket(ticket_id)

    if not ticket_deleted:
        return jsonify({"error": "Ticket not found"}), 404

    return jsonify({
            "id": ticket["id"],
            "ticket_number": ticket["ticket_number"],
            "title": ticket["title"],
            "description": ticket["description"],
            "category": ticket["category"],
            "priority": ticket["priority"],
            "assigned_team": ticket["assigned_team"],
            "ai_summary": ticket["ai_summary"],
            "ai_recommendations": json.loads(ticket["ai_recommendations"])
        })

######################################### API Assets Routes #################################

@app.route("/assets/<int:asset_id>")
def get_asset_route(asset_id):

    asset = get_asset(asset_id)

    if asset is None:
        return jsonify({"error": "Asset not found"}), 404

    return jsonify({
        "id": asset["id"],
        "asset_tag": asset["asset_tag"],
        "asset_type": asset["asset_type"],
        "manufacturer": asset["manufacturer"],
        "serial_number": asset["serial_number"],
        "status": asset["status"],
        "assigned_to": asset["assigned_to"],
        "purchase_date": asset["purchase_date"],
        "warranty_end": asset["warranty_end"],
        })


@app.route("/assets", methods=["POST"])
def create_new_asset_route():

    data = request.get_json()

    asset_id = create_asset(
        data["asset_tag"],
        data["asset_type"],
        data["manufacturer"],
        data["serial_number"],
        data["assigned_to"],
        data["purchase_date"],
        data["warranty_end"],
    )

    asset = get_asset(asset_id)

    return jsonify({
    "id": asset["id"],
    "asset_tag": asset["asset_tag"],
    "asset_type": asset["asset_type"],
    "manufacturer": asset["manufacturer"],
    "serial_number": asset["serial_number"],
    "status": asset["status"],
    "assigned_to": asset["assigned_to"],
    "purchase_date": asset["purchase_date"],
    "warranty_end": asset["warranty_end"],
    }), 201

@app.route("/assets/<int:asset_id>", methods=["PUT"])
def update_asset_route(asset_id):

    data = request.get_json()

    asset_updated = update_asset(asset_id, data)

    if not asset_updated:
        return jsonify({"error": "Asset not found"}), 404

    asset = get_asset(asset_id)

    return jsonify({
        "id": asset["id"],
        "asset_tag": asset["asset_tag"],
        "asset_type": asset["asset_type"],
        "manufacturer": asset["manufacturer"],
        "serial_number": asset["serial_number"],
        "status": asset["status"],
        "assigned_to": asset["assigned_to"],
        "purchase_date": asset["purchase_date"],
        "warranty_end": asset["warranty_end"],
        })


@app.route("/assets/<int:asset_id>", methods=["DELETE"])
def delete_asset_route(asset_id):

    asset = get_asset(asset_id)
    asset_deleted = delete_asset(asset_id)

    if not asset_deleted:
        return jsonify({"error": "Asset not found"}), 404

    return jsonify({
            "id": asset["id"],
            "asset_tag": asset["asset_tag"],
            "asset_type": asset["asset_type"],
            "manufacturer": asset["manufacturer"],
            "serial_number": asset["serial_number"],
            "status": asset["status"],
            "assigned_to": asset["assigned_to"],
            "purchase_date": asset["purchase_date"],
            "warranty_end": asset["warranty_end"],
            })

@app.route("/assets/<int:asset_id>/assign", methods=["POST"])
def assign_asset_route(asset_id):

    data = request.get_json()
    employee_id = data["employee_id"]

    asset_assigned = assign_asset(asset_id, employee_id)

    if not asset_assigned:
        return jsonify({"error": "Asset could not be assigned"}), 404

    asset = get_asset(asset_id)

    return jsonify({
                "id": asset["id"],
                "asset_tag": asset["asset_tag"],
                "asset_type": asset["asset_type"],
                "manufacturer": asset["manufacturer"],
                "serial_number": asset["serial_number"],
                "status": asset["status"],
                "assigned_to": asset["assigned_to"],
                "purchase_date": asset["purchase_date"],
                "warranty_end": asset["warranty_end"],
                })

@app.route("/assets/<int:asset_id>/return", methods=["POST"])
def return_asset_route(asset_id):

    asset_returned = return_asset(asset_id)

    if not asset_returned:
        return jsonify({"Error": "Asset could not be returned"}), 404

    asset = get_asset(asset_id)

    return jsonify({
        "id": asset["id"],
        "asset_tag": asset["asset_tag"],
        "asset_type": asset["asset_type"],
        "manufacturer": asset["manufacturer"],
        "serial_number": asset["serial_number"],
        "status": asset["status"],
        "assigned_to": asset["assigned_to"],
        "purchase_date": asset["purchase_date"],
        "warranty_end": asset["warranty_end"],
    })

######################################### API ONBOARDING Routes #################################

@app.route("/onboardings/<int:onboarding_id>")
def get_onboarding_route(onboarding_id):

    onboarding = get_onboarding_details(onboarding_id)

    if not onboarding:
        return jsonify({"error": "Onboarding not found"}), 404

    return jsonify(onboarding)

@app.route("/onboarding/tasks/<int:task_id>", methods=["PUT"])
def update_onboarding_task_route(task_id):

    data = request.get_json()

    task_updated = update_task(task_id, data)

    if not task_updated:
        return jsonify({
            "error": "Task not found or no valid fields provided"
        }), 404

    return jsonify({
        "message":  "Task updated",
        "task_id": task_id
    })

@app.route("/onboardings/<int:onboarding_id>/complete", methods=["POST"])
def complete_onboarding_route(onboarding_id):

    onboarding_completed = complete_onboarding(onboarding_id)

    if not onboarding_completed:
        return jsonify({
            "error": "Onboarding cannot be completed. All tasks must be completed"
        }), 400

    onboarding = get_onboarding_details(onboarding_id)

    return jsonify(onboarding)

if __name__ == "__main__":
    app.run(debug=True)