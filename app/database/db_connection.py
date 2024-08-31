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

# Determine if we're in production or development
IS_PRODUCTION = os.getenv("ENVIRONMENT", "development") == "production"

# Get the appropriate database URL
if IS_PRODUCTION:
    DATABASE_URL = os.getenv("PRODUCTION_DATABASE_URL")
    logger.info("Using production database.")
else:
    DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")
    logger.info("Using local database.")

logger.info(f"Using database URL: {DATABASE_URL}")

# Ensure the DATABASE_URL is using the correct protocol
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

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