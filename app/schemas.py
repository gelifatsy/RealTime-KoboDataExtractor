# app/schemas.py

from pydantic import BaseModel, Field
from typing import Optional, List
import datetime
from uuid import UUID

# KoboSubmission Schema
class KoboSubmissionSchema(BaseModel):
    id: Optional[int]  # Auto-generated primary key, not required on creation
    _id: int
    form_uuid: Optional[UUID]
    instance_id: Optional[UUID]
    submission_time: datetime.datetime
    start_time: datetime.datetime
    end_time: datetime.datetime
    survey_date: datetime.date
    _geolocation: Optional[str]
    _status: Optional[str]
    _tags: Optional[str]
    _notes: Optional[str]
    _validation_status: Optional[str]
    _submitted_by: Optional[str]
    version: Optional[str]

    class Config:
        orm_mode = True  # This will allow Pydantic to serialize SQLAlchemy objects


# Client Schema
class ClientSchema(BaseModel):
    id: Optional[int]  # Auto-generated primary key, not required on creation
    unique_id: str
    client_name: str
    client_id_manifest: Optional[str]
    location: Optional[str]
    client_phone: Optional[str]
    alt_phone: Optional[str]
    phone_type: Optional[str]
    gender: Optional[str]
    age: Optional[int]
    nationality: Optional[str]
    strata: Optional[str]
    disability: Optional[bool]
    education: Optional[str]
    client_status: Optional[str]
    sole_income_earner: Optional[bool]
    responsible_people: Optional[int]
    submission_id: int  # Foreign key to associate with KoboSubmission

    class Config:
        orm_mode = True


# BusinessInfo Schema
class BusinessInfoSchema(BaseModel):
    id: Optional[int]  # Auto-generated primary key, not required on creation
    country_name: Optional[str]
    region_name: Optional[str]
    bda_name: Optional[str]
    cohort: Optional[str]
    program: Optional[str]
    biz_status: Optional[str]
    biz_operating: Optional[bool]
    submission_id: int  # Foreign key to associate with KoboSubmission

    class Config:
        orm_mode = True


# SurveyMetadata Schema
class SurveyMetadataSchema(BaseModel):
    id: Optional[int]  # Auto-generated primary key, not required on creation
    form_uuid: Optional[UUID]
    instance_id: Optional[UUID]
    form_version: Optional[str]
    submission_id: int  # Foreign key to associate with KoboSubmission

    class Config:
        orm_mode = True


# Schema for List Responses (Optional)
class KoboSubmissionListSchema(BaseModel):
    submissions: List[KoboSubmissionSchema]

    class Config:
        orm_mode = True


class ClientListSchema(BaseModel):
    clients: List[ClientSchema]

    class Config:
        orm_mode = True


class BusinessInfoListSchema(BaseModel):
    business_infos: List[BusinessInfoSchema]

    class Config:
        orm_mode = True


class SurveyMetadataListSchema(BaseModel):
    survey_metadatas: List[SurveyMetadataSchema]

    class Config:
        orm_mode = True
