from datetime import datetime
from ..database.db import (
    get_employee,
    create_onboarding,
    get_onboarding,
    create_onboarding_task,
    get_onboarding_tasks,
    update_onboarding,
    update_onboarding_task
)

def start_onboarding(employee_id):
    employee = get_employee(employee_id)

    if not employee:
        return False

    onboarding_id = create_onboarding(employee_id)

    tasks = [
        ("Create AD user account", "Account", "IT support"),
        ("Configure email and MFA", "Access", "IT support"),
        ("Prepare and assign laptop", "Hardware", "IT support"),
        ("Install required software", "Software", "System Administrator"),
        ("Grant department access", "Access", "System Administrator")
    ]

    for task, category, assigned_to in tasks:
        create_onboarding_task(
            onboarding_id,
            task,
            category,
            assigned_to
        )

    return onboarding_id

def get_onboarding_details(onboarding_id):
    onboarding = get_onboarding(onboarding_id)

    if not onboarding:
        return None

    tasks = get_onboarding_tasks(onboarding_id)

    return {
        "onboarding": dict(onboarding),
        "tasks": [dict(task) for task in tasks]
    }

def update_task(task_id, updates):
    return update_onboarding_task(task_id, updates)

def complete_onboarding(onboarding_id):
    onboarding = get_onboarding(onboarding_id)

    if not onboarding:
        return False

    tasks = get_onboarding_tasks(onboarding_id)

    if not tasks:
        return False

    # Every task must be completed
    for task in tasks:
        if task["status"] != "Completed":
            return False

    completed_at = datetime.now().isoformat(timespec="seconds")

    return update_onboarding(
        {
            "status": "Completed",
            "completed_at": completed_at
        }
    )