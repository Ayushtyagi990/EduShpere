from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from common.auth_middleware import JWTMiddleware

from model import (
    Class,
    Section,
    Subject,
    SubjectType,
    TeacherAssignment,
    AcademicYear,
    AcademicTerm,
    AcademicSession,
    Department,
    Campus,
    AcademicCalendar,
    AcademicHoliday,
)

from database import get_session

from jose import jwt, JWTError


# ============================================================
# SECURITY
# ============================================================

security = HTTPBearer()

SECRET_KEY = "priyanshu"
ALGORITHM = "HS256"


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
)

app.add_middleware(JWTMiddleware)


# ============================================================
# JWT VERIFICATION
# ============================================================

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token",
        )


# ============================================================
# CLASS
# ============================================================

@app.post("/class")
def create_class(
    data: Class,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data.created_at = datetime.now()
    data.updated_at = datetime.now()

    session.add(data)

    try:
        session.commit()
        session.refresh(data)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create class",
        )

    return data


@app.get("/class")
def get_classes(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    classes = session.exec(
        select(Class)
    ).all()

    return {
        "user": payload,
        "classes": classes,
    }


@app.get("/class/{class_id}")
def get_class_by_id(
    class_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(Class, class_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Class not found",
        )

    return data


@app.put("/class/{class_id}")
def update_class(
    class_id: int,
    data: Class,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(Class, class_id)

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Class not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    existing.updated_at = datetime.now()

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/class/{class_id}")
def delete_class(
    class_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(Class, class_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Class not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"class {class_id} deleted"
    }


# ============================================================
# SECTION
# ============================================================

@app.post("/section")
def create_section(
    data: Section,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if data.class_id is not None:
        class_data = session.get(Class, data.class_id)

        if not class_data:
            raise HTTPException(
                status_code=404,
                detail="Class not found",
            )

    data.created_at = datetime.now()
    data.updated_at = datetime.now()

    session.add(data)

    try:
        session.commit()
        session.refresh(data)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create section",
        )

    return data


@app.get("/section")
def get_sections(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    sections = session.exec(
        select(Section)
    ).all()

    return {
        "user": payload,
        "sections": sections,
    }


@app.get("/section/{section_id}")
def get_section_by_id(
    section_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(Section, section_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Section not found",
        )

    return data


@app.put("/section/{section_id}")
def update_section(
    section_id: int,
    data: Section,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(Section, section_id)

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Section not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    existing.updated_at = datetime.now()

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/section/{section_id}")
def delete_section(
    section_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(Section, section_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Section not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"section {section_id} deleted"
    }


# ============================================================
# SUBJECT
# ============================================================

@app.post("/subject")
def create_subject(
    data: Subject,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data.created_at = datetime.now()
    data.updated_at = datetime.now()

    session.add(data)

    try:
        session.commit()
        session.refresh(data)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create subject",
        )

    return data


@app.get("/subject")
def get_subjects(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    subjects = session.exec(
        select(Subject)
    ).all()

    return {
        "user": payload,
        "subjects": subjects,
    }


@app.get("/subject/{subject_id}")
def get_subject_by_id(
    subject_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(Subject, subject_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Subject not found",
        )

    return data


@app.put("/subject/{subject_id}")
def update_subject(
    subject_id: int,
    data: Subject,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(Subject, subject_id)

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Subject not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    existing.updated_at = datetime.now()

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/subject/{subject_id}")
def delete_subject(
    subject_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(Subject, subject_id)

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Subject not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"subject {subject_id} deleted"
    }


# ============================================================
# SUBJECT TYPE
# ============================================================

@app.post("/subject-type")
def create_subject_type(
    data: SubjectType,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data.created_at = datetime.now()
    data.updated_at = datetime.now()

    session.add(data)
    session.commit()
    session.refresh(data)

    return data


@app.get("/subject-type")
def get_subject_types(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.exec(
        select(SubjectType)
    ).all()

    return {
        "user": payload,
        "subject_types": data,
    }


@app.get("/subject-type/{subject_type_id}")
def get_subject_type_by_id(
    subject_type_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        SubjectType,
        subject_type_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Subject type not found",
        )

    return data


@app.put("/subject-type/{subject_type_id}")
def update_subject_type(
    subject_type_id: int,
    data: SubjectType,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(
        SubjectType,
        subject_type_id,
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Subject type not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    existing.updated_at = datetime.now()

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/subject-type/{subject_type_id}")
def delete_subject_type(
    subject_type_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        SubjectType,
        subject_type_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Subject type not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"subject type {subject_type_id} deleted"
    }


# ============================================================
# TEACHER ASSIGNMENT
# ============================================================

@app.post("/teacher-assignment")
def create_teacher_assignment(
    data: TeacherAssignment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if data.subject_id is not None:
        subject = session.get(
            Subject,
            data.subject_id,
        )

        if not subject:
            raise HTTPException(
                status_code=404,
                detail="Subject not found",
            )

    if data.section_id is not None:
        section = session.get(
            Section,
            data.section_id,
        )

        if not section:
            raise HTTPException(
                status_code=404,
                detail="Section not found",
            )

    data.created_at = datetime.now()
    data.updated_at = datetime.now()

    session.add(data)

    try:
        session.commit()
        session.refresh(data)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create teacher assignment",
        )

    return data


@app.get("/teacher-assignment")
def get_teacher_assignments(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    assignments = session.exec(
        select(TeacherAssignment)
    ).all()

    return {
        "user": payload,
        "teacher_assignments": assignments,
    }


@app.get("/teacher-assignment/{assignment_id}")
def get_teacher_assignment_by_id(
    assignment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        TeacherAssignment,
        assignment_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Teacher assignment not found",
        )

    return data


@app.put("/teacher-assignment/{assignment_id}")
def update_teacher_assignment(
    assignment_id: int,
    data: TeacherAssignment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(
        TeacherAssignment,
        assignment_id,
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Teacher assignment not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    existing.updated_at = datetime.now()

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/teacher-assignment/{assignment_id}")
def delete_teacher_assignment(
    assignment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        TeacherAssignment,
        assignment_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Teacher assignment not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"teacher assignment {assignment_id} deleted"
    }


# ============================================================
# ACADEMIC YEAR
# ============================================================

@app.post("/academic-year")
def create_academic_year(
    data: AcademicYear,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data.created_at = datetime.now()
    data.updated_at = datetime.now()

    session.add(data)
    session.commit()
    session.refresh(data)

    return data


@app.get("/academic-year")
def get_academic_years(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.exec(
        select(AcademicYear)
    ).all()

    return {
        "user": payload,
        "academic_years": data,
    }


@app.get("/academic-year/{academic_year_id}")
def get_academic_year_by_id(
    academic_year_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        AcademicYear,
        academic_year_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Academic year not found",
        )

    return data


@app.put("/academic-year/{academic_year_id}")
def update_academic_year(
    academic_year_id: int,
    data: AcademicYear,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(
        AcademicYear,
        academic_year_id,
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Academic year not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    existing.updated_at = datetime.now()

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/academic-year/{academic_year_id}")
def delete_academic_year(
    academic_year_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        AcademicYear,
        academic_year_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Academic year not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"academic year {academic_year_id} deleted"
    }


# ============================================================
# ACADEMIC TERM
# ============================================================

@app.post("/academic-term")
def create_academic_term(
    data: AcademicTerm,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if data.academic_year_id is not None:
        academic_year = session.get(
            AcademicYear,
            data.academic_year_id,
        )

        if not academic_year:
            raise HTTPException(
                status_code=404,
                detail="Academic year not found",
            )

    data.created_at = datetime.now()
    data.updated_at = datetime.now()

    session.add(data)
    session.commit()
    session.refresh(data)

    return data


@app.get("/academic-term")
def get_academic_terms(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.exec(
        select(AcademicTerm)
    ).all()

    return {
        "user": payload,
        "academic_terms": data,
    }


@app.get("/academic-term/{academic_term_id}")
def get_academic_term_by_id(
    academic_term_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        AcademicTerm,
        academic_term_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Academic term not found",
        )

    return data


@app.put("/academic-term/{academic_term_id}")
def update_academic_term(
    academic_term_id: int,
    data: AcademicTerm,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(
        AcademicTerm,
        academic_term_id,
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Academic term not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    existing.updated_at = datetime.now()

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/academic-term/{academic_term_id}")
def delete_academic_term(
    academic_term_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        AcademicTerm,
        academic_term_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Academic term not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"academic term {academic_term_id} deleted"
    }


# ============================================================
# ACADEMIC SESSION
# ============================================================

@app.post("/academic-session")
def create_academic_session(
    data: AcademicSession,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if data.academic_year_id is not None:
        academic_year = session.get(
            AcademicYear,
            data.academic_year_id,
        )

        if not academic_year:
            raise HTTPException(
                status_code=404,
                detail="Academic year not found",
            )

    if data.academic_term_id is not None:
        academic_term = session.get(
            AcademicTerm,
            data.academic_term_id,
        )

        if not academic_term:
            raise HTTPException(
                status_code=404,
                detail="Academic term not found",
            )

    data.created_at = datetime.now()
    data.updated_at = datetime.now()

    session.add(data)
    session.commit()
    session.refresh(data)

    return data


@app.get("/academic-session")
def get_academic_sessions(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.exec(
        select(AcademicSession)
    ).all()

    return {
        "user": payload,
        "academic_sessions": data,
    }


@app.get("/academic-session/{academic_session_id}")
def get_academic_session_by_id(
    academic_session_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        AcademicSession,
        academic_session_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Academic session not found",
        )

    return data


@app.put("/academic-session/{academic_session_id}")
def update_academic_session(
    academic_session_id: int,
    data: AcademicSession,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(
        AcademicSession,
        academic_session_id,
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Academic session not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    existing.updated_at = datetime.now()

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/academic-session/{academic_session_id}")
def delete_academic_session(
    academic_session_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        AcademicSession,
        academic_session_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Academic session not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"academic session {academic_session_id} deleted"
    }


# ============================================================
# DEPARTMENT
# ============================================================

@app.post("/department")
def create_department(
    data: Department,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data.created_at = datetime.now()
    data.updated_at = datetime.now()

    session.add(data)

    try:
        session.commit()
        session.refresh(data)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create department",
        )

    return data


@app.get("/department")
def get_departments(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.exec(
        select(Department)
    ).all()

    return {
        "user": payload,
        "departments": data,
    }


@app.get("/department/{department_id}")
def get_department_by_id(
    department_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        Department,
        department_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )

    return data


@app.put("/department/{department_id}")
def update_department(
    department_id: int,
    data: Department,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(
        Department,
        department_id,
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    existing.updated_at = datetime.now()

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/department/{department_id}")
def delete_department(
    department_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        Department,
        department_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Department not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"department {department_id} deleted"
    }


# ============================================================
# CAMPUS
# ============================================================

@app.post("/campus")
def create_campus(
    data: Campus,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data.status = data.status or "ACTIVE"

    session.add(data)

    try:
        session.commit()
        session.refresh(data)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Campus email already exists or campus creation failed",
        )

    return data


@app.get("/campus")
def get_campuses(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.exec(
        select(Campus)
    ).all()

    return {
        "user": payload,
        "campuses": data,
    }




@app.get("/campus/{campus_id}")
def get_campus_by_id(
    campus_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        Campus,
        campus_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Campus not found",
        )

    return data


@app.put("/campus/{campus_id}")
def update_campus(
    campus_id: int,
    data: Campus,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(
        Campus,
        campus_id,
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Campus not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    session.add(existing)

    try:
        session.commit()
        session.refresh(existing)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Campus email already exists",
        )

    return existing


@app.delete("/campus/{campus_id}")
def delete_campus(
    campus_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        Campus,
        campus_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Campus not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"campus {campus_id} deleted"
    }


# ============================================================
# ACADEMIC CALENDAR
# ============================================================

@app.post("/academic-calendar")
def create_academic_calendar(
    data: AcademicCalendar,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if data.academic_year_id is not None:
        academic_year = session.get(
            AcademicYear,
            data.academic_year_id,
        )

        if not academic_year:
            raise HTTPException(
                status_code=404,
                detail="Academic year not found",
            )

    session.add(data)
    session.commit()
    session.refresh(data)

    return data


@app.get("/academic-calendar")
def get_academic_calendars(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.exec(
        select(AcademicCalendar)
    ).all()

    return {
        "user": payload,
        "academic_calendars": data,
    }


@app.get("/academic-calendar/{calendar_id}")
def get_academic_calendar_by_id(
    calendar_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        AcademicCalendar,
        calendar_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Academic calendar not found",
        )

    return data


@app.put("/academic-calendar/{calendar_id}")
def update_academic_calendar(
    calendar_id: int,
    data: AcademicCalendar,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(
        AcademicCalendar,
        calendar_id,
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Academic calendar not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/academic-calendar/{calendar_id}")
def delete_academic_calendar(
    calendar_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        AcademicCalendar,
        calendar_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Academic calendar not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"academic calendar {calendar_id} deleted"
    }


# ============================================================
# ACADEMIC HOLIDAY
# ============================================================

@app.post("/academic-holiday")
def create_academic_holiday(
    data: AcademicHoliday,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if data.academic_year_id is not None:
        academic_year = session.get(
            AcademicYear,
            data.academic_year_id,
        )

        if not academic_year:
            raise HTTPException(
                status_code=404,
                detail="Academic year not found",
            )

    session.add(data)
    session.commit()
    session.refresh(data)

    return data


@app.get("/academic-holiday")
def get_academic_holidays(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.exec(
        select(AcademicHoliday)
    ).all()

    return {
        "user": payload,
        "academic_holidays": data,
    }


@app.get("/academic-holiday/{holiday_id}")
def get_academic_holiday_by_id(
    holiday_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        AcademicHoliday,
        holiday_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Academic holiday not found",
        )

    return data


@app.put("/academic-holiday/{holiday_id}")
def update_academic_holiday(
    holiday_id: int,
    data: AcademicHoliday,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing = session.get(
        AcademicHoliday,
        holiday_id,
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Academic holiday not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(existing, key, value)

    session.add(existing)
    session.commit()
    session.refresh(existing)

    return existing


@app.delete("/academic-holiday/{holiday_id}")
def delete_academic_holiday(
    holiday_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    data = session.get(
        AcademicHoliday,
        holiday_id,
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="Academic holiday not found",
        )

    session.delete(data)
    session.commit()

    return {
        "details": f"academic holiday {holiday_id} deleted"
    }