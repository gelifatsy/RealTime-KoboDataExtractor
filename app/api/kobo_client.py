import os
import sys
import uuid
from typing import List, Dict, Any
from typing import Generator, Any

# Add current directory
sys.path.append(os.getcwd())

# Add parent directory
sys.path.append(os.path.dirname(os.getcwd()))

import requests
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.db_connection import SessionLocal, engine, Base
from app.database.models import KoboSubmission, Client, BusinessInfo, SurveyMetadata

# Load environment variables from .env file
load_dotenv()

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# Fetch configuration from environment variables
KOBO_API_URL = os.getenv("KOBO_API_URL")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
DJANGO_LANGUAGE = os.getenv("DJANGO_LANGUAGE", "en")
PAGE_SIZE = int(os.getenv("PAGE_SIZE", 100))

HEADERS = {
    'Authorization': f'Token {AUTH_TOKEN}',
    'Cookie': f'django_language={DJANGO_LANGUAGE}'
}

def fetch_data_from_kobo(page_size: int = PAGE_SIZE) -> Generator[Dict[str, Any], None, None]:
    """
    Fetches data from KoboToolbox API and handles large datasets using pagination.

    Args:
        page_size (int): The number of records to fetch per page (default is set by PAGE_SIZE).

    Yields:
        dict: Each record fetched from the KoboToolbox API.
    """
    next_url = KOBO_API_URL  # Start with the initial URL
    params = {
        'page_size': page_size
    }

    while next_url:
        try:
            response = requests.get(next_url, headers=HEADERS, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            
            for record in data['results']:
                yield record  # Yield each record individually to handle data in a streaming manner

            # Check if there is a next page
            next_url = data.get('next')
            if next_url:
                print(f"Fetching next page: {next_url}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

def clean_uuid(uuid_string: str) -> uuid.UUID:
    """
    Cleans and validates a UUID string.

    Args:
        uuid_string (str): The UUID string to clean and validate.

    Returns:
        uuid.UUID: A valid UUID object.

    Raises:
        ValueError: If the UUID is invalid after cleaning.
    """
    if uuid_string.startswith('uuid:'):
        uuid_string = uuid_string[5:]
    try:
        return uuid.UUID(uuid_string)
    except ValueError:
        raise ValueError(f"Invalid UUID: {uuid_string}")

def store_data_to_db(db: Session, record: Dict[str, Any]) -> None:
    """
    Stores a single record into the database.

    Args:
        db (Session): SQLAlchemy session object.
        record (dict): A dictionary containing a single record from KoboToolbox API.
    """
    try:
        # Check if submission already exists
        if db.query(KoboSubmission).filter(KoboSubmission._id == record['_id']).first():
            print(f"Skipping duplicate submission with _id: {record['_id']}")
            return

        # Clean and validate UUIDs
        form_uuid = clean_uuid(record.get('formhub/uuid', ''))
        instance_id = clean_uuid(record.get('meta/instanceID', ''))

        # Insert into KoboSubmission
        submission = KoboSubmission(
            _id=record['_id'],
            form_uuid=form_uuid,
            instance_id=instance_id,
            submission_time=record.get('_submission_time'),
            start_time=record.get('starttime'),
            end_time=record.get('endtime'),
            survey_date=record.get('cd_survey_date'),
            _geolocation=record.get('_geolocation'),
            _status=record.get('_status'),
            _tags=record.get('_tags'),
            _notes=record.get('_notes'),
            _validation_status=record.get('_validation_status'),
            _submitted_by=record.get('_submitted_by'),
            version=record.get('__version__')
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)

        # Insert into Client
        if 'sec_a/unique_id' in record:
            client = Client(
                unique_id=record.get('sec_a/unique_id'),
                client_name=record.get('sec_c/cd_client_name'),
                client_id_manifest=record.get('sec_c/cd_client_id_manifest'),
                location=record.get('sec_c/cd_location'),
                client_phone=record.get('sec_c/cd_clients_phone'),
                alt_phone=record.get('sec_c/cd_phoneno_alt_number'),
                phone_type=record.get('sec_c/cd_clients_phone_smart_feature'),
                gender=record.get('sec_c/cd_gender'),
                age=record.get('sec_c/cd_age'),
                nationality=record.get('sec_c/cd_nationality'),
                strata=record.get('sec_c/cd_strata'),
                disability=record.get('sec_c/cd_disability') == 'Yes',
                education=record.get('sec_c/cd_education'),
                client_status=record.get('sec_c/cd_client_status'),
                sole_income_earner=record.get('sec_c/cd_sole_income_earner') == 'Yes',
                responsible_people=record.get('sec_c/cd_howrespble_pple'),
                submission_id=submission.id
            )
            db.add(client)
            db.commit()

        # Insert into BusinessInfo
        if 'sec_a/cd_biz_country_name' in record:
            business_info = BusinessInfo(
                country_name=record.get('sec_a/cd_biz_country_name'),
                region_name=record.get('sec_a/cd_biz_region_name'),
                bda_name=record.get('sec_b/bda_name'),
                cohort=record.get('sec_b/cd_cohort'),
                program=record.get('sec_b/cd_program'),
                biz_status=record.get('group_mx5fl16/cd_biz_status'),
                biz_operating=record.get('group_mx5fl16/bd_biz_operating') == 'yes',
                submission_id=submission.id
            )
            db.add(business_info)
            db.commit()

        # Insert into SurveyMetadata
        metadata = SurveyMetadata(
            form_uuid=form_uuid,
            instance_id=instance_id,
            form_version=record.get('__version__'),
            submission_id=submission.id
        )
        db.add(metadata)
        db.commit()

    except IntegrityError as e:
        db.rollback()
        print(f"Integrity error while inserting record {record['_id']}: {e}")
    except Exception as e:
        db.rollback()
        print(f"An error occurred while inserting record {record['_id']}: {e}")


def process_and_store_data():
    """
    Process data in a streaming fashion and store it into the database.
    """
    record_count = 0

    print("Fetching data from KoboToolbox...\n")

    # Start a database session
    db = SessionLocal()

    try:
        for record in fetch_data_from_kobo():
            store_data_to_db(db, record)
            record_count += 1
            print(f"Processed record {record_count}: {record['_id']}")

            # Uncomment the following lines if you want to limit the number of records processed
            # if record_count >= 5:  # Adjust this limit as needed
            #     break

    finally:
        db.close()

    print(f"\nTotal records processed: {record_count}")

# if __name__ == "__main__":
#     process_and_store_data()