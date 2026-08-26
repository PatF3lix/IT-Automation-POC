from flask import Flask, jsonify, request
from .database.db import get_employee, create_ticket

app = Flask(__name__)


@app.route("/")
def home():
    return "IT Automation POC is running!"

@app.route("/employees/<int:employee_id>")
def employee(employee_id):
    employee = get_employee(employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({
        "id": employee["id"],
        "first_name": employee["first_name"],
        "first_name": employee["last_name"],
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

    return jsonify ({
        "message": "Ticket created",
        "ticket_id": ticket_id
    }), 201


if __name__ == "__main__":
    app.run(debug=True)