from  sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from datetime import datetime, date, time


class TimeSlot(SQLModel, table = True):
    """ storing TimeSlot information """
    id : int | None =  Field(primary_key = True)
    period_no : int | None = Field(default = None)
    slot_name : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class Timetable(SQLModel, table = True):
    __tablename__ = "timetables"
    id : int | None = Field(primary_key = True)
    academic_year_id : int | None =  Field(default = None)
    semester_id : int | None = Field(default = None)
    department_id :int | None = Field(default = None)
    program_id : int | None = Field(default = None)
    section_id : int | None = Field(default = None)
    subject_id : int | None = Field(default = None)
    faculty_id  : int | None = Field(default = None)
    classroom_id :  int | None = Field(default = None)
    day_of_week :  str | None = Field(default = None)
    start_time : time | None = Field(default = None)
    end_time : time  | None = Field(default = None)
    period_no : int | None = Field(default = None)
    is_lab : bool | None = Field(default = None)
    remarks : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)



class Classroom(SQLModel, table = True):
    """ storing Classroom information """
    __tablename__ = "classrooms"
    id : int | None = Field(primary_key = True)
    room_no : int | None = Field(default = None)
    building : str | None = Field(default = None)
    floor : int  | None = Field(default = None)
    capcity : int | None = Field(default = None)
    room_type : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Holiday(SQLModel, table = True):
    """ storing Holiday information """
    __tablename__ = "holidays"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)
    
class TimetableVersion(SQLModel, table = True):
    """ storing TimetableVersion information """
    __tablename__ = "timetable_versions"
    id : int | None = Field(primary_key = True)
    academic_year_id : int | None =  Field(default = None)
    semester_id : int | None = Field(default = None)
    department_id :int | None = Field(default = None)
    program_id : int | None = Field(default = None)
    section_id : int | None = Field(default = None)
    version_no : int | None = Field(default = None)
    is_active : bool | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)