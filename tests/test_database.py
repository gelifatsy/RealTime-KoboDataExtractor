import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.db_connection import Base, get_db
from app.database.models import KoboSubmission, Client, BusinessInfo, SurveyMetadata
from fastapi.testclient import TestClient
import os

# Set up a test database URL
TEST_DATABASE_URL = os.getenv("LOCAL_DATABASE_URL_TEST")

# Create a new engine and session for testing
engine = create_engine(TEST_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables for the test database
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    # Set up a new session for each test
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

def test_kobo_submission(db):
    # Arrange: Set up test data
    new_submission = KoboSubmission(
        id=1,  # Assuming ID is set manually for simplicity
        formhub_uuid="a7eb959a-da4c-485b-8334-ee761ab1e4a7",
        instanceID="uuid:5c59e249-b88e-4742-abb6-942f79627cb6",
        submission_time="2024-08-24T07:45:34",
        starttime="2024-08-24T09:44:06.712+02:00",
        endtime="2024-08-24T09:44:39.156+02:00",
        cd_survey_date="2024-08-24",
        geolocation=[None, None],
        status="submitted_via_web",
        tags=[],
        notes=[],
        validation_status={},
        submitted_by=None,
        version="vBfco72yRxvHQun3cF8HPK",
        sec_a_unique_id="unique-id",
        sec_c_client_name="Test Client",
        sec_c_client_id_manifest="123-456-789",
        sec_c_location="Test Location",
        sec_c_clients_phone="1234567890",
        sec_c_phoneno_alt_number="0987654321",
        sec_c_clients_phone_smart_feature="Smart phone",
        sec_c_gender="Male",
        sec_c_age=30,
        sec_c_nationality="Test Nationality",
        sec_c_strata="Test Strata",
        sec_c_disability="No",
        sec_c_education="College",
        sec_c_client_status="New clients",
        sec_c_sole_income_earner="Yes",
        sec_c_howrespble_pple=3,
        sec_a_cd_biz_country_name="Test Country",
        sec_a_cd_biz_region_name="Test Region",
        sec_b_bda_name="Test BDA",
        sec_b_cd_cohort="Cohort 1",
        sec_b_cd_program="Program Name",
        group_mx5fl16_cd_biz_status="Idea stage",
        group_mx5fl16_bd_biz_operating="yes"
    )
    db.add(new_submission)
    db.commit()

    # Act: Query the database
    submission = db.query(KoboSubmission).filter_by(id=1).first()

    # Assert: Check the result
    assert submission is not None
    assert submission.sec_c_client_name == "Test Client"
    assert submission.sec_c_age == 30

