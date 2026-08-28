from flask import Blueprint, jsonify, request

from ..database import (
    create_asset,
    get_asset,
    update_asset,
    delete_asset
)

from ..services.asset_service import (
    assign_asset,
    return_asset
)


asset_bp = Blueprint("assets", __name__)


@asset_bp.route("/assets/<int:asset_id>")
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
        "warranty_end": asset["warranty_end"]
    })


@asset_bp.route("/assets", methods=["POST"])
def create_new_asset_route():
    data = request.get_json()

    asset_id = create_asset(
        data["asset_tag"],
        data["asset_type"],
        data["manufacturer"],
        data["serial_number"],
        data["assigned_to"],
        data["purchase_date"],
        data["warranty_end"]
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
        "warranty_end": asset["warranty_end"]
    }), 201


@asset_bp.route("/assets/<int:asset_id>", methods=["PUT"])
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
        "warranty_end": asset["warranty_end"]
    })


@asset_bp.route("/assets/<int:asset_id>", methods=["DELETE"])
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
        "warranty_end": asset["warranty_end"]
    })


@asset_bp.route("/assets/<int:asset_id>/assign", methods=["POST"])
def assign_asset_route(asset_id):
    data = request.get_json()

    employee_id = data["employee_id"]

    asset_assigned = assign_asset(asset_id, employee_id)

    if not asset_assigned:
        return jsonify({
            "error": "Asset could not be assigned"
        }), 404

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
        "warranty_end": asset["warranty_end"]
    })


@asset_bp.route("/assets/<int:asset_id>/return", methods=["POST"])
def return_asset_route(asset_id):
    asset_returned = return_asset(asset_id)

    if not asset_returned:
        return jsonify({
            "Error": "Asset could not be returned"
        }), 404

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
        "warranty_end": asset["warranty_end"]
    })