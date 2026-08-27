import json
from flask import Flask, jsonify, request
from .database.db import get_employee, create_ticket, get_ticket, update_ticket
from .services.ticket_service import process_ticket

app = Flask(__name__)

@app.route("/")
def home():
    return "IT Automation POC is running!"

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

@app.route("/tickets", methods=["POST"])
def create_new_ticket():

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
    
    
if __name__ == "__main__":
    app.run(debug=True)