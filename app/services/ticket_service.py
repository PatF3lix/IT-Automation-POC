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

# 1. Get employees in the right department
# 2. Look at each employee's role
# 3. Give that role a score
# 4. substract their current ticket workload
# 5. keep whoever has the highest final score
# 6. Assign the ticket to them


def assign_best_employee(ticket_id, required_department, preferred_role):
    employees = get_employees_by_department(required_department)

    if not employees:
        return None

    best_employee = None
    best_score = None

    for employee in employees:
        role = employee["job_title"].lower()
        preferred = preferred_role.lower()

        role_score = 0

        if preferred in role or role in preferred:
            role_score = 10

        elif "l3" in preferred and "l3" in role:
            role_score = 9

        elif "l2" in preferred and "l2" in role:
            role_score = 8

        elif "network" in preferred and "network" in role:
            role_score = 10

        elif "system" in preferred and "system" in role:
            role_score = 10

        elif "support" in preferred and "support" in role:
            role_score = 7

        active_tickets = get_employee_active_ticket_count(
            employee["id"]
        )

        score = (role_score * 10) - active_tickets

        if best_score is None or score > best_score:
            best_score = score
            best_employee = employee

    if best_employee:
        assign_ticket_to_employee(
            ticket_id,
            best_employee["id"]
        )

    return best_employee


if __name__ == "__main__":

    result = process_ticket(1)
    print("Ticket processed:", result)