from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from database.connection import DbConnection, Base

# ✅ Create SQLAlchemy engine from connection class
engine = DbConnection.connection()

# ✅ Create tables using SQLAlchemy Base metadata
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

# ✅ SessionLocal factory
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Annotated dependency for routes
SessionDep = Annotated[Session, Depends(get_db)]