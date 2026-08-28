import json

from flask import Blueprint, jsonify, request

from ..database import (
    create_ticket,
    get_ticket,
    update_ticket,
    delete_ticket
)

from ..services.ticket_service import process_ticket


ticket_bp = Blueprint("tickets", __name__)


@ticket_bp.route("/tickets", methods=["POST"])
def create_new_ticket_route():
    data = request.get_json()

    ticket_id = create_ticket(
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
        "assigned_to": ticket["assigned_to"],
        "ai_summary": ticket["ai_summary"],
        "ai_recommendations": json.loads(ticket["ai_recommendations"])
    }), 201


@ticket_bp.route("/tickets/<int:ticket_id>")
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
        "assigned_to": ticket["assigned_to"],
        "ai_summary": ticket["ai_summary"],
        "ai_recommendations": json.loads(ticket["ai_recommendations"])
    })


@ticket_bp.route("/tickets/<int:ticket_id>", methods=["PUT"])
def update_ticket_route(ticket_id):
    data = request.get_json()

    ticket_updated = update_ticket(ticket_id, data)

    if not ticket_updated:
        return jsonify({
            "error": "Ticket not found or no valid fields provided"
        }), 404

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


@ticket_bp.route("/tickets/<int:ticket_id>", methods=["DELETE"])
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