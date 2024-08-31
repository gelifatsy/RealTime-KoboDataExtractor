# app/webhook/webhook_endpoint.py

from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.db_connection import SessionLocal
from app.database.models import KoboSubmission, Client, BusinessInfo, SurveyMetadata
import datetime

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
        submission_data = payload.get("submission", {})
        client_data = payload.get("client", {})
        business_info_data = payload.get("business_info", {})
        survey_metadata_data = payload.get("survey_metadata", {})

        # Create KoboSubmission instance
        new_submission = KoboSubmission(
            _id=submission_data.get("_id"),
            form_uuid=submission_data.get("formhub/uuid"),
            instance_id=submission_data.get("meta/instanceID"),
            submission_time=submission_data.get("submission_time", datetime.datetime.now()),
            start_time=submission_data.get("starttime", datetime.datetime.now()),
            end_time=submission_data.get("endtime", datetime.datetime.now()),
            survey_date=submission_data.get("cd_survey_date", datetime.date.today()),
            _geolocation=submission_data.get("_geolocation"),
            _status=submission_data.get("_status"),
            _tags=submission_data.get("_tags"),
            _notes=submission_data.get("_notes"),
            _validation_status=submission_data.get("_validation_status"),
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
                unique_id=client_data.get("unique_id"),
                client_name=client_data.get("client_name"),
                location=client_data.get("location"),
                client_phone=client_data.get("client_phone"),
                alt_phone=client_data.get("alt_phone"),
                phone_type=client_data.get("phone_type"),
                gender=client_data.get("gender"),
                age=client_data.get("age"),
                nationality=client_data.get("nationality"),
                strata=client_data.get("strata"),
                disability=client_data.get("disability"),
                education=client_data.get("education"),
                client_status=client_data.get("client_status"),
                sole_income_earner=client_data.get("sole_income_earner"),
                responsible_people=client_data.get("responsible_people"),
                submission_id=new_submission.id  # Associate with submission
            )
            db.add(new_client)
            db.commit()
            print("Client data saved successfully")

        # Create and associate BusinessInfo instance
        if business_info_data:
            new_business_info = BusinessInfo(
                country_name=business_info_data.get("country_name"),
                region_name=business_info_data.get("region_name"),
                bda_name=business_info_data.get("bda_name"),
                cohort=business_info_data.get("cohort"),
                program=business_info_data.get("program"),
                biz_status=business_info_data.get("biz_status"),
                biz_operating=business_info_data.get("biz_operating", False),
                submission_id=new_submission.id  # Associate with submission
            )
            db.add(new_business_info)
            db.commit()
            print("BusinessInfo data saved successfully")

        # Create and associate SurveyMetadata instance
        if survey_metadata_data:
            new_survey_metadata = SurveyMetadata(
                form_uuid=survey_metadata_data.get("form_uuid"),
                instance_id=survey_metadata_data.get("instance_id"),
                form_version=survey_metadata_data.get("form_version"),
                submission_id=new_submission.id  # Associate with submission
            )
            db.add(new_survey_metadata)
            db.commit()
            print("SurveyMetadata data saved successfully")

        return {"status": "success", "message": "Webhook data received and saved"}

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
