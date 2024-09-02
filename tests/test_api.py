# tests/test_api.py

import pytest
import uuid
from fastapi.testclient import TestClient
from app.webhook.webhook_endpoint import app
from app.database.db_connection import SessionLocal
from app.database.models import KoboSubmission, Client, BusinessInfo, SurveyMetadata

client = TestClient(app)

def cleanup_test_data(unique_id):
    # Function to delete test data with a specific unique_id
    db = SessionLocal()
    try:
        # Find the kobo_submission_id using the unique_id
        submission_to_delete = db.query(KoboSubmission).filter(KoboSubmission._id == unique_id).first()
        if submission_to_delete:
            # Delete from related tables (clients, business_info, survey_metadata) for the specific kobo_submission_id
            db.query(Client).filter(Client.submission_id == submission_to_delete.id).delete(synchronize_session=False)
            db.query(BusinessInfo).filter(BusinessInfo.submission_id == submission_to_delete.id).delete(synchronize_session=False)
            db.query(SurveyMetadata).filter(SurveyMetadata.submission_id == submission_to_delete.id).delete(synchronize_session=False)
            
            # Then delete from kobo_submissions table
            db.query(KoboSubmission).filter(KoboSubmission._id == unique_id).delete(synchronize_session=False)
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"An error occurred while cleaning up test data: {e}")
    finally:
        db.close()

@pytest.fixture(autouse=True)
def run_around_tests():
    unique_id = uuid.uuid4().int % 100000  # Generate a unique integer ID
    cleanup_test_data(unique_id)  # Clean up any pre-existing test data
    yield unique_id
    cleanup_test_data(unique_id)  # Clean up after the test

def test_webhook_post_valid_data(run_around_tests):
    unique_id = run_around_tests  # Get the unique ID from the fixture
    client_unique_id = f"SS{unique_id}"  # Generate a unique client unique_id for each test run
    
    response = client.post(
        "/webhook",
        json={
            "_id": unique_id,  # Use the unique integer value for id
            "formhub/uuid": "a7eb959a-da4c-485b-8334-ee761ab1e4a7",
            "meta/instanceID": "uuid:5c59e249-b88e-4742-abb6-942f79627cb6",
            "_submission_time": "2024-08-24T07:45:34",
            "starttime": "2024-08-24T09:44:06.712+02:00",
            "endtime": "2024-08-24T09:44:39.156+02:00",
            "cd_survey_date": "2024-08-24",
            "_geolocation": [None, None],
            "_status": "submitted_via_web",
            "_tags": [],
            "_notes": [],
            "_validation_status": {},
            "_submitted_by": None,
            "__version__": "vBfco72yRxvHQun3cF8HPK",
            "sec_a/unique_id": client_unique_id,  # Use a unique value for client unique_id
            "sec_c/cd_client_name": "Test Client",
            "sec_c/cd_client_id_manifest": "123-456-789",
            "sec_c/cd_location": "Test Location",
            "sec_c/cd_clients_phone": "1234567890",
            "sec_c/cd_phoneno_alt_number": "0987654321",
            "sec_c/cd_clients_phone_smart_feature": "Smart phone",
            "sec_c/cd_gender": "Male",
            "sec_c/cd_age": 30,
            "sec_c/cd_nationality": "Test Nationality",
            "sec_c/cd_strata": "Test Strata",
            "sec_c/cd_disability": "No",
            "sec_c/cd_education": "College",
            "sec_c/cd_client_status": "New clients",
            "sec_c/cd_sole_income_earner": "Yes",
            "sec_c/cd_howrespble_pple": "3",
            "sec_a/cd_biz_country_name": "Test Country",
            "sec_a/cd_biz_region_name": "Test Region",
            "sec_b/bda_name": "Test BDA",
            "sec_b/cd_cohort": "Cohort 1",
            "sec_b/cd_program": "Program Name",
            "group_mx5fl16/cd_biz_status": "Idea stage",
            "group_mx5fl16/bd_biz_operating": "yes"
        }
    )
    
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Webhook data received and saved"}
