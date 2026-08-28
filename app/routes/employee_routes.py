from flask import Blueprint, jsonify

from ..database import (
    get_employee,
    get_all_employees,
    get_employee_assets,
    get_employee_tickets
)


employee_bp = Blueprint("employees", __name__)


@employee_bp.route("/employees/<int:employee_id>")
def get_employee_route(employee_id):
    employee = get_employee(employee_id)

    if employee is None:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({
        "id": employee["id"],
        "first_name": employee["first_name"],
        "last_name": employee["last_name"],
        "department": employee["department"],
        "job_title": employee["job_title"],
        "manager": employee["manager"],
        "start_date": employee["start_date"],
        "status": employee["status"]
    })


@employee_bp.route("/employees")
def get_all_employees_route():
    employees = get_all_employees()

    return jsonify([
        dict(employee)
        for employee in employees
    ])


@employee_bp.route("/employees/<int:employee_id>/assets")
def get_employee_assets_route(employee_id):
    employee_assets = get_employee_assets(employee_id)

    return jsonify({
        "employee_id": employee_id,
        "assets": [dict(asset) for asset in employee_assets]
    })


@employee_bp.route("/employees/<int:employee_id>/tickets")
def get_employee_tickets_route(employee_id):
    employee = get_employee(employee_id)

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    tickets = get_employee_tickets(employee_id)

    return jsonify({
        "employee_id": employee_id,
        "tickets": [dict(ticket) for ticket in tickets]
    })