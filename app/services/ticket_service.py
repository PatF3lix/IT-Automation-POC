from .ollama_service import analyze_ticket
from ..database.db import (
    get_ticket,
    update_ticket_ai,
    get_employees_by_department,
    get_employee_active_ticket_count,
    assign_ticket_to_employee
)


def process_ticket(ticket_id):
    ticket = get_ticket(ticket_id)

    if ticket_id is None:
        return False

    ticket_analysis = analyze_ticket(ticket["description"])

    update_ticket_ai(
        ticket_id,
        ticket_analysis["category"],
        ticket_analysis["priority"],
        ticket_analysis["assigned_team"],
        ticket_analysis["summary"],
        ticket_analysis["recommendations"]
    )

    return True

if __name__ == "__main__":

    result = process_ticket(1)
    print("Ticket processed:", result)