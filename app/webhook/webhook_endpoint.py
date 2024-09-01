from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db_connection import SessionLocal
from app.database.models import KoboSubmission, Client, BusinessInfo, SurveyMetadata
from uuid import UUID
import datetime
from typing import List

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/webhook")
async def webhook_endpoint(request: Request, db: Session = Depends(get_db)):
    try:
        payload = await request.json()
        print(f"Received webhook data: {payload}")

        # Extract data from payload
        submission_data = payload
        client_data = submission_data
        business_info_data = submission_data
        survey_metadata_data = submission_data

        # Log extracted data for verification
        print(f"Submission Data: {submission_data}")
        print(f"Client Data: {client_data}")
        print(f"Business Info Data: {business_info_data}")
        print(f"Survey Metadata Data: {survey_metadata_data}")

        # Create KoboSubmission instance
        new_submission = KoboSubmission(
            _id=submission_data.get("_id"),
            form_uuid=UUID(submission_data.get("formhub/uuid")) if submission_data.get("formhub/uuid") else None,
            instance_id=UUID(submission_data.get("meta/instanceID")) if submission_data.get("meta/instanceID") else None,
            submission_time=submission_data.get("_submission_time") or datetime.datetime.now(),
            start_time=submission_data.get("starttime") or datetime.datetime.now(),
            end_time=submission_data.get("endtime") or datetime.datetime.now(),
            survey_date=submission_data.get("cd_survey_date") or datetime.date.today(),
            _geolocation=str(submission_data.get("_geolocation")),
            _status=submission_data.get("_status"),
            _tags=str(submission_data.get("_tags")),
            _notes=str(submission_data.get("_notes")),
            _validation_status=str(submission_data.get("_validation_status")),
            _submitted_by=submission_data.get("_submitted_by"),
            version=submission_data.get("__version__")
        )
        
        db.add(new_submission)
        db.commit()
        db.refresh(new_submission)  # Refresh to get the ID
        print("New submission saved successfully")

        # Create and associate Client instance
        if client_data:
            new_client = Client(
                unique_id=client_data.get("sec_a/unique_id"),
                client_name=client_data.get("sec_c/cd_client_name"),
                client_id_manifest=client_data.get("sec_c/cd_client_id_manifest"),
                location=client_data.get("sec_c/cd_location"),
                client_phone=client_data.get("sec_c/cd_clients_phone"),
                alt_phone=client_data.get("sec_c/cd_phoneno_alt_number"),
                phone_type=client_data.get("sec_c/cd_clients_phone_smart_feature"),
                gender=client_data.get("sec_c/cd_gender"),
                age=client_data.get("sec_c/cd_age"),
                nationality=client_data.get("sec_c/cd_nationality"),
                strata=client_data.get("sec_c/cd_strata"),
                disability=True if client_data.get("sec_c/cd_disability") == "Yes" else False,
                education=client_data.get("sec_c/cd_education"),
                client_status=client_data.get("sec_c/cd_client_status"),
                sole_income_earner=True if client_data.get("sec_c/cd_sole_income_earner") == "Yes" else False,
                responsible_people=int(client_data.get("sec_c/cd_howrespble_pple")),
                submission_id=new_submission.id  # Associate with submission
            )
            db.add(new_client)
            db.commit()
            print("Client data saved successfully")

        # Create and associate BusinessInfo instance
        if business_info_data:
            new_business_info = BusinessInfo(
                country_name=business_info_data.get("sec_a/cd_biz_country_name"),
                region_name=business_info_data.get("sec_a/cd_biz_region_name"),
                bda_name=business_info_data.get("sec_b/bda_name"),
                cohort=business_info_data.get("sec_b/cd_cohort"),
                program=business_info_data.get("sec_b/cd_program"),
                biz_status=business_info_data.get("group_mx5fl16/cd_biz_status"),
                biz_operating=True if business_info_data.get("group_mx5fl16/bd_biz_operating") == "yes" else False,
                submission_id=new_submission.id  # Associate with submission
            )
            db.add(new_business_info)
            db.commit()
            print("BusinessInfo data saved successfully")

        # Create and associate SurveyMetadata instance
        if survey_metadata_data:
            new_survey_metadata = SurveyMetadata(
                form_uuid=UUID(survey_metadata_data.get("formhub/uuid")) if survey_metadata_data.get("formhub/uuid") else None,
                instance_id=UUID(survey_metadata_data.get("meta/instanceID")) if survey_metadata_data.get("meta/instanceID") else None,
                form_version=survey_metadata_data.get("__version__"),
                submission_id=new_submission.id  # Associate with submission
            )
            db.add(new_survey_metadata)
            db.commit()
            print("SurveyMetadata data saved successfully")

        return {"status": "success", "message": "Webhook data received and saved"}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/submissions", response_model=List[KoboSubmission])
def get_submissions(db: Session = Depends(get_db)):
    try:
        submissions = db.query(KoboSubmission).all()
        return submissions
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
