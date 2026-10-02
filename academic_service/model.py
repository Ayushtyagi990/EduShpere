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
    description: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class SubjectType(SQLModel, table=True):
    __tablename__ = "subjecttype"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    status: str | None = Field(default=None)
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


class AcademicYear(SQLModel, table=True):
    __tablename__ = "academicyear"
    id: int | None = Field(primary_key = True)
    name: str | None = Field(default = None)
    start_date: date | None = Field(default=None)
    end_date: date | None = Field(default=None)
    status: str | None = Field(default = None)
    created_at: datetime | None = Field(default = None)
    updated_at: datetime | None = Field(default = None)


class AcademicTerm(SQLModel, table=True):
    __tablename__ = "academicterm"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    term_number: int | None = Field(default=None)
    academic_year_id: int | None = Field(foreign_key="academicyear.id")
    academic_year_id: AcademicYear = Relationship()
    start_date: date | None = Field(default=None)
    end_date: date | None = Field(default=None)
    status: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)



class AcademicSession(SQLModel, table=True):
    __tablename__ = "academicsession"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    academic_year_id: int | None = Field(foreign_key="academicyear.id")
    academic_year_id: AcademicYear = Relationship()
    academic_term_id: int | None = Field(foreign_key="academicterm.id")
    academic_term_id: AcademicTerm = Relationship()
    start_date: date | None = Field(default=None)
    end_date: date | None = Field(default=None)
    status: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)



class Department(SQLModel, table=True):
    __tablename__ = "department"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    code: str | None = Field(default=None)
    description: str | None = Field(default=None)
    hod_user_id: int = Field(foreign_key="user.id")
    status: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)



class Campus(SQLModel, table=True):
    __tablename__ = "campus"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    code: str | None = Field(default=None)
    address_id: int = Field(foreign_key="address.id")
    phone: str | None = Field(default=None)
    email : str | None = Field(index = True, unique = True)
    status: str | None = Field(default=None)



class AcademicCalendar(SQLModel, table=True):
    __tablename__ = "academiccalendar"
    id: int | None = Field(default=None, primary_key=True)
    academic_year_id: int | None = Field(foreign_key="academicyear.id")
    academic_year: AcademicYear = Relationship() 
    title: str | None = Field(default=None)
    event_type: str | None = Field(default=None) 
    start_date: date | None = Field(default=None) 
    end_date: date | None = Field(default=None)  
    description: str | None = Field(default=None)
    status: str | None = Field(default=None)



class AcademicHoliday(SQLModel, table=True):
    __tablename__ = "academicholiday"
    id: int | None = Field(default=None, primary_key=True)
    academic_year_id: int | None = Field(foreign_key="academicyear.id")
    name: str | None = Field(default=None)
    holiday_date: date | None = Field(default=None)
    holiday_type: str | None = Field(default=None)
    description: str | None = Field(default=None)
    status: str | None = Field(default=None)
    