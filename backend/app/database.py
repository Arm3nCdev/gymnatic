from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# We'll use SQLite for local dev if Postgres isn't running, but the user requested Postgres.
# For now, let's configure a default Postgres URL that they can change via env vars.
# PostgreSQL 16/17 (Wait for user confirmation, but using standard psycopg2 URL)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/gymbro"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
