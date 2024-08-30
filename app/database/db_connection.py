#Import libraries
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get the database URL from the environment variable
DATABASE_URL = os.getenv('DATABASE_URL')
logger.info(f"Using database URL: {DATABASE_URL}")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)
logger.info("Database engine created successfully.")

# Create a configured "Session" class
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
logger.info("SessionLocal configured successfully.")

# Base class for our models to inherit
Base = declarative_base()

# Dependency to get the database session (useful in web frameworks like FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()