from  sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time



class ExamType(SQLModel, table = True):
    __tablename__ = "examtype"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    description : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Examination(SQLModel, table = True):
    __tablename__ = "examination"
    id : int | None = Field(primary_key = True)
    examtype_id : int  = Field(foreign_key  = "examtype.id")
    examtype : ExamType = Relationship()
    academic_year_id : int | None = Field(default = None)
    semester_id : int | None = Field(default = None)
    department_id : int | None = Field(default = None)
    program_id : int | None = Field(default = None)
    section_id : int | None = Field(default = None)
    subject_id : int | None = Field(default = None)
    exam_date : date | None = Field(default = None)
    title : str | None = Field(default = None)
    start_time : time | None = Field(default = None)
    end_time : time | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class ExamSchedule(SQLModel, table = True):
    __tablename__ = "examschedule"
    id : int | None = Field(primary_key = True)
    examination_id : int  = Field(foreign_key  = "examination.id")
    examination : Examination = Relationship()
    subject_id : int
    faculty_id : int
    classroom_id : int
    exam_date : date | None = Field(default = None)
    start_time : time | None = Field(default = None)
    total_marks : int | None = Field(default = None)
    passing_marks : int | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class StudentMark(SQLModel, table = True):
    __tablename__ = "studentmarks"
    id : int | None = Field(primary_key = True)
    examschedule_id : int  = Field(foreign_key  = "examschedule.id")
    examination : Examination = Relationship()
    subject_id : int
    student_id : int
    marks_obtained : float | None = Field(default = None)
    total_marks : float | None = Field(default = None)
    grade : str | None = Field(default = None)
    result_status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class Result(SQLModel, table = True):
    __tablename__ = "result"
    id : int | None = Field(primary_key = True)
    student_id : int
    examination_id : int  = Field(foreign_key  = "examination.id")
    examination : Examination = Relationship()
    marks_obtained : float | None = Field(default = None)
    total_marks : float | None = Field(default = None)
    cgpa : float | None = Field(default = None)
    grade : str | None = Field(default = None)
    result_status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class GradeScale(SQLModel, table = True):
    __tablename__ = "gradescale"
    id : int | None = Field(primary_key = True)
    grade : str | None = Field(default = None)
    min_percentage : float | None = Field(default = None)
    max_percentage : float | None = Field(default = None)
    grade_point : float | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)



    




    