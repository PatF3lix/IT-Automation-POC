from flask import Blueprint, jsonify, request

from ..database import get_employee

from ..services.onboarding_service import (
    start_onboarding,
    get_onboarding_details,
    update_task,
    complete_onboarding
)


onboarding_bp = Blueprint("onboarding", __name__)


def add_employee_name_to_onboarding(data):
    if not data:
        return data

    onboarding = dict(data["onboarding"])

    employee = get_employee(
        onboarding["employee_id"]
    )

    if employee:
        onboarding["employee_name"] = (
            f"{employee['first_name']} "
            f"{employee['last_name']}"
        )
    else:
        onboarding["employee_name"] = "Unknown Employee"

    return {
        "onboarding": onboarding,
        "tasks": data["tasks"]
    }


@onboarding_bp.route(
    "/employees/<int:employee_id>/onboarding",
    methods=["POST"]
)
def start_employee_onboarding(employee_id):
    onboarding_id = start_onboarding(employee_id)

    if not onboarding_id:
        return jsonify({
            "error": "Employee not found"
        }), 404

    onboarding = get_onboarding_details(
        onboarding_id
    )

    onboarding = add_employee_name_to_onboarding(
        onboarding
    )

    return jsonify(onboarding), 201


@onboarding_bp.route(
    "/onboardings/<int:onboarding_id>"
)
def get_onboarding_route(onboarding_id):
    onboarding = get_onboarding_details(
        onboarding_id
    )

    if not onboarding:
        return jsonify({
            "error": "Onboarding not found"
        }), 404

    onboarding = add_employee_name_to_onboarding(
        onboarding
    )

    return jsonify(onboarding)


@onboarding_bp.route(
    "/onboarding/tasks/<int:task_id>",
    methods=["PUT"]
)
def update_onboarding_task_route(task_id):
    data = request.get_json()

    task_updated = update_task(
        task_id,
        data
    )

    if not task_updated:
        return jsonify({
            "error": (
                "Task not found or "
                "no valid fields provided"
            )
        }), 404

    return jsonify({
        "message": "Task updated",
        "task_id": task_id
    })


@onboarding_bp.route(
    "/onboardings/<int:onboarding_id>/complete",
    methods=["POST"]
)
def complete_onboarding_route(onboarding_id):
    onboarding_completed = complete_onboarding(
        onboarding_id
    )

    if not onboarding_completed:
        return jsonify({
            "error": (
                "Onboarding cannot be completed. "
                "All tasks must be completed"
            )
        }), 400

    onboarding = get_onboarding_details(
        onboarding_id
    )

    onboarding = add_employee_name_to_onboarding(
        onboarding
    )

    return jsonify(onboarding)