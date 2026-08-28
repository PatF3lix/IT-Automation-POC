from app.database import (
    initialize_database,
    seed_database,
    DATABASE_FILE
)


def reset_database():

    if DATABASE_FILE.exists():
        DATABASE_FILE.unlink()
        print("Existing database deleted.")

    initialize_database()
    seed_database()

    print(f"Database initialized: {DATABASE_FILE}")


if __name__ == "__main__":
    reset_database()