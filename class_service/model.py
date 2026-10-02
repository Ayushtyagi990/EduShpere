from  sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date


class Class(SQLModel, table=True):
    __tablename__ = "class"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class Section(SQLModel, table=True):
    __tablename__ = "section"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    class_id: int | None = Field(foreign_key="class.id")
    class_: Class = Relationship()
    capacity: int | None = Field(default=None)
    description: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)



class Subject(SQLModel, table=True):
    __tablename__ = "subject"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    code: str | None = Field(default=None)
    class_id: int | None = Field(foreign_key="class.id")
    class_: Class = Relationship()
    description: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class TeacherAssignment(SQLModel, table=True):
    __tablename__ = "teacher_assignment"
    id: int | None = Field(default=None, primary_key=True)
    teacher_id: int 
    subject_id: int | None = Field(foreign_key="subject.id")
    subject: Subject = Relationship()
    section_id: int | None = Field(foreign_key="section.id")
    section: Section = Relationship()
    academic_year_id: int
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class StudentEnrollment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_id: int
    class_id: int | None = Field(foreign_key="class.id")
    class_: Class = Relationship()
    section_id: int | None = Field(foreign_key="section.id")
    section: Section = Relationship()
    academic_year_id: int
    enrollment_date: date | None = Field(default=None)
    status: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)