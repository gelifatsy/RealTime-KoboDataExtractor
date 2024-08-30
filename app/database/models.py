
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from .db_connection import Base

class KoboSubmission(Base):
    __tablename__ = 'kobo_submissions'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    _id = Column(Integer, unique=True, nullable=False)
    form_uuid = Column(PG_UUID(as_uuid=True), nullable=False)
    instance_id = Column(PG_UUID(as_uuid=True), nullable=False)
    submission_time = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    survey_date = Column(Date, nullable=False)
    _geolocation = Column(JSON)
    _status = Column(String(50))
    _tags = Column(JSON)
    _notes = Column(JSON)
    _validation_status = Column(JSON)
    _submitted_by = Column(String(100))
    version = Column(String(50))

    # Relationships
    clients = relationship("Client", back_populates="submission")
    business_infos = relationship("BusinessInfo", back_populates="submission")
    survey_metadatas = relationship("SurveyMetadata", back_populates="submission")

class Client(Base):
    __tablename__ = 'clients'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    unique_id = Column(String(50), unique=True, nullable=False)
    client_name = Column(String(100), nullable=False)
    client_id_manifest = Column(String(50))
    location = Column(String(100))
    client_phone = Column(String(20))
    alt_phone = Column(String(20))
    phone_type = Column(String(50))
    gender = Column(String(10))
    age = Column(Integer)
    nationality = Column(String(50))
    strata = Column(String(100))
    disability = Column(Boolean, default=False)
    education = Column(String(100))
    client_status = Column(String(50))
    sole_income_earner = Column(Boolean, default=False)
    responsible_people = Column(Integer)

    # Foreign Key
    submission_id = Column(Integer, ForeignKey('public.kobo_submissions.id'), nullable=False)

    # Relationships
    submission = relationship("KoboSubmission", back_populates="clients")

class BusinessInfo(Base):
    __tablename__ = 'business_info'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String(100))
    region_name = Column(String(100))
    bda_name = Column(String(100))
    cohort = Column(String(50))
    program = Column(String(50))
    biz_status = Column(String(50))
    biz_operating = Column(Boolean, default=False)

    # Foreign Key
    submission_id = Column(Integer, ForeignKey('public.kobo_submissions.id'), nullable=False)

    # Relationships
    submission = relationship("KoboSubmission", back_populates="business_infos")

class SurveyMetadata(Base):
    __tablename__ = 'survey_metadata'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    form_uuid = Column(PG_UUID(as_uuid=True), nullable=False)
    instance_id = Column(PG_UUID(as_uuid=True), nullable=False)
    form_version = Column(String(50))

    # Foreign Key
    submission_id = Column(Integer, ForeignKey('public.kobo_submissions.id'), nullable=False)

    # Relationships
    submission = relationship("KoboSubmission", back_populates="survey_metadatas")

    def __repr__(self):
        return f"<SurveyMetadata(id={self.id}, form_uuid={self.form_uuid}, instance_id={self.instance_id})>"