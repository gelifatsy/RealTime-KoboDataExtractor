# app/database/create_tables.py

import os
import sys
from sqlalchemy.exc import SQLAlchemyError

# Add the parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from database.db_connection import engine, Base
from database.models import KoboSubmission, Client, BusinessInfo, SurveyMetadata

def create_tables():
    try:
        # Print registered tables
        print(f"Registered tables: {Base.metadata.tables.keys()}")

        # Create tables
        Base.metadata.create_all(bind=engine)

        print("Tables created successfully.")

        # Verify tables in the database
        from sqlalchemy import inspect
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names(schema='public')
        print(f"Existing tables in database: {existing_tables}")

        # Verify foreign keys
        for table_name in existing_tables:
            foreign_keys = inspector.get_foreign_keys(table_name, schema='public')
            print(f"Foreign keys for {table_name}: {foreign_keys}")

    except SQLAlchemyError as e:
        print(f"An error occurred while creating tables: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    create_tables()
