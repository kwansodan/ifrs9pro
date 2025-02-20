from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your database URL
DATABASE_URL = "mysql://sql7760763:khtrGtc)9))mxQ7p@localhost:3306/sql7760763"


# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
