from  sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time

class AttendanceSession(SQLModel, table = True):
    __tablename__ = "AttendanceSession"
    id : int | None = Field(primary_key = True)
    timetable_id : int 
    academic_year_id : int 
    semester_id : int
    department_id : int
    program_id : int
    section_id : int
    subject_id : int
    faculty_id : int
    attendance_date : date | None = Field(default = None)
    period_no : int | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)




class StudentAttendance(SQLModel, table = True):
    __tablename__ = "StudentAttendance"
    id : int | None = Field(primary_key = True)
    attendance_session_id : int 
    student_id : int
    check_in_time : time | None = Field(default = None)
    remarks : str | None = Field(default = None)
    status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class AttendanceSummary(SQLModel, table = True):
    __tablename__ = "AttendanceSummary"
    id : int | None = Field(primary_key = True)
    student_id : int
    academic_year_id : int 
    semester_id : int
    department_id : int
    program_id : int
    section_id : int
    subject_id : int
    total_classes_held : int | None = Field(default = None)
    total_classes_attended : int | None = Field(default = None)
    attendance_percentage : float | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)