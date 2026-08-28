# app/database/__init__.py

from .connection import (
    get_connection,
    initialize_database,
    DATABASE_FILE
)

from .employees import (
    get_employee,
    get_employees_by_department,
    get_all_employees,
    create_employee,
    update_employee,
    delete_employee
)

from .tickets import (
    get_ticket,
    get_employee_tickets,
    get_employee_active_ticket_count,
    create_ticket,
    update_ticket,
    update_ticket_ai,
    assign_ticket_to_employee,
    delete_ticket
)

from .assets import (
    get_asset,
    get_employee_assets,
    create_asset,
    update_asset,
    delete_asset
)

from .onboarding import (
    get_onboarding,
    get_onboarding_tasks,
    create_onboarding,
    create_onboarding_task,
    update_onboarding,
    update_onboarding_task
)

from .seed import seed_database