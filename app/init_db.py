import time

from app import app
from database import db
from api.model.models import Service, Incident, Team, EscalationPolicy


def initialize_database():
    """Initializes the database schema."""
    max_retries = 5
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            with app.app_context():
                db.drop_all()
                db.create_all()
            print("Database initialized successfully.")
            return
        except Exception as e:
            print(f"Error initializing database (attempt {attempt+1}/{max_retries}): {e}")
            time.sleep(retry_delay)

    print("Failed to initialize database after {} attempts.".format(max_retries))

if __name__ == "__main__":
    initialize_database()