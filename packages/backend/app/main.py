from .db import engine
from .models import Base


def init_db() -> None:
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def main() -> None:
    print("Starting backend...")
    init_db()
    print("Database initialized.")


if __name__ == "__main__":
    main()
