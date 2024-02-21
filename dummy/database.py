from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from .settings import environment_vars 

SQLALCHEMY_DATABASE_URL = f"postgresql://{environment_vars.db_user}:{environment_vars.db_password}@{environment_vars.db_host}/{environment_vars.db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        