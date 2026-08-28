from .employees import create_employee
from .assets import create_asset, update_asset
from .onboarding import (
    create_onboarding,
    create_onboarding_task
)


def seed_database():

    # Employees

    create_employee(
        "John",
        "Doe",
        "IT",
        "Senior System Administrator",
        "IT Manager",
        "2026-09-01"
    )

    create_employee(
        "Sarah",
        "Martin",
        "IT",
        "Senior Network Administrator",
        "IT Manager",
        "2026-09-01"
    )

    create_employee(
        "Mike",
        "Brown",
        "IT",
        "Tech Support L2",
        "John Doe",
        "2026-09-02"
    )

    create_employee(
        "Emily",
        "Wilson",
        "IT",
        "Tech Support L2",
        "John Doe",
        "2026-09-02"
    )

    create_employee(
        "Alex",
        "Taylor",
        "IT",
        "Tech Support L3",
        "John Doe",
        "2026-09-02"
    )

    # Assets

    create_asset(
        "LAP-001",
        "Laptop",
        "Dell",
        "DL-SENIOR-001",
        1,
        "2026-08-01",
        "2029-08-01"
    )

    update_asset(
        1,
        {
            "status": "Assigned"
        }
    )

    create_asset(
        "LAP-002",
        "Laptop",
        "Lenovo",
        "LN-SENIOR-002",
        2,
        "2026-08-01",
        "2029-08-01"
    )

    update_asset(
        2,
        {
            "status": "Assigned"
        }
    )

    # Example onboarding

    onboarding_id = create_onboarding(3)

    create_onboarding_task(
        onboarding_id,
        "Create AD user account",
        "Account",
        "IT Support"
    )

    print("Demo database seeded successfully.")