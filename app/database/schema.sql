CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department TEXT NOT NULL,
    job_title TEXT NOT NULL,
    manager TEXT,
    start_date TEXT,
    status TEXT NOT NULL DEFAULT 'Pending'
);

CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_tag TEXT NOT NULL UNIQUE,
    asset_type TEXT NOT NULL,
    manufacturer TEXT,
    serial_number TEXT UNIQUE,
    status TEXT NOT NULL DEFAULT 'Available',
    assigned_to INTEGER,
    purchase_date TEXT,
    warranty_end TEXT,

    FOREIGN KEY (assigned_to) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_number TEXT UNIQUE,
    employee_id INTEGER,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT,
    priority TEXT,
    assigned_team TEXT,
    status TEXT NOT NULL DEFAULT 'New',
    ai_summary TEXT,
    ai_recommendations TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS onboardings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Pending',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TEXT,

    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS onboarding_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    onboarding_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    category TEXT,
    assigned_to TEXT,
    status TEXT NOT NULL DEFAULT 'Pending',

    FOREIGN KEY (onboarding_id) REFERENCES onboardings(id)
);