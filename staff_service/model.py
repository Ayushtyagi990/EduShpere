from  sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from datetime import datetime, date

class Staff(SQLModel, table = True):
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    email : str | None = Field(default = None)
    phone : int | None = Field(default = None)
    dob : date | None = Field(default = None)
    gender : str | None = Field(default = None)
    blood_group : str | None = Field(default = None)
    department_id : int | None = Field(default = None)
    designation_id : int | None = Field(default = None)
    degree : str | None = Field(default = None)
    specialization : str | None = Field(default = None)
    experience : int | None = Field(default = None)
    university : str | None = Field(default = None)
    passing_year : int | None = Field(default = None)
    percentage : float | None = Field(default = None)
    user_id : int 
    address_id : int 
    status: str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)
