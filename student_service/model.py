from  sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from datetime import datetime, date


class Student(SQLModel, table = True):
    """ storing student information """
    __tablename__ = "student"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    roll_no : str | None = Field(default = None)
    enrollment_no : str | None = Field(default = None)
    email : str | None = Field(default = None)
    phone : int | None = Field(default = None)
    dob : date | None = Field(default = None)
    gender : str | None = Field(default = None)
    blood_group : str | None = Field(default = None)
    user_id : int
    address_id : int 
    admission_date : date | None = Field(default = None)
    status : str | None = Field(default = None)
    college_id : int | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Guardian(SQLModel, table = True):
    """ storing guardian information """
    __tablename__ = "guardian"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    email : str | None = Field(default = None)
    phone : int | None = Field(default = None)
    relation : str | None = Field(default = None)
    occupation: str | None = Field(default = None)
    student_id : int
    address_id : int
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class StudentDocument(SQLModel, table = True):
    """ storing student documents """
    __tablename__ = "student_documents"
    id : int | None = Field(primary_key = True)
    student_id : int
    document_type : str | None = Field(default = None)
    document_no : str | None = Field(default = None)
    status: str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class StudentEnrollment(SQLModel, table=True):
    __tablename__ = "student_enrollment"
    id: int | None = Field(default=None, primary_key=True)
    student_id: int
    class_id: int
    section_id: int
    academic_year: int | None = Field(default=None)
    enrollment_date: date | None = Field(default=None)
    status: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)