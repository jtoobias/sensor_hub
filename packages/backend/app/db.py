from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .settings import settings

#All DB plumbing lives here.

# Create SQLAlchemy engine (connection pool)
engine = create_engine(
    settings.database_url,
    echo=False,  # set True to see SQL queries
)

# Factory for DB sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Base class for ORM models
Base = declarative_base()
