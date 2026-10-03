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
    Student,
    Guardian,
    StudentDocument,
    StudentEnrollment,
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
# STUDENT
# ============================================================

@app.post("/student")
def create_student(
    student: Student,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    # Check user_id
    if not student.user_id:
        raise HTTPException(
            status_code=400,
            detail="user_id is required",
        )

    # Check address_id
    if not student.address_id:
        raise HTTPException(
            status_code=400,
            detail="address_id is required",
        )

    student.created_at = datetime.now()
    student.updated_at = datetime.now()

    session.add(student)

    try:
        session.commit()
        session.refresh(student)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create student",
        )

    return student


# ============================================================
# GET ALL STUDENTS
# ============================================================

@app.get("/student")
def get_students(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    students = session.exec(
        select(Student)
    ).all()

    return {
        "user": payload,
        "students": students,
    }


# ============================================================
# GET STUDENT BY ID
# ============================================================

@app.get("/student/{student_id}")
def get_student_by_id(
    student_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    student = session.get(
        Student,
        student_id,
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    return student


# ============================================================
# UPDATE STUDENT
# ============================================================

@app.put("/student/{student_id}")
def update_student(
    student_id: int,
    data: Student,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    student = session.get(
        Student,
        student_id,
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(student, key, value)

    student.updated_at = datetime.now()

    session.add(student)

    try:
        session.commit()
        session.refresh(student)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update student",
        )

    return student


# ============================================================
# DELETE STUDENT
# ============================================================

@app.delete("/student/{student_id}")
def delete_student(
    student_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    student = session.get(
        Student,
        student_id,
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found",
        )

    session.delete(student)
    session.commit()

    return {
        "details": f"student {student_id} deleted"
    }


# ============================================================
# GUARDIAN
# ============================================================

@app.post("/guardian")
def create_guardian(
    guardian: Guardian,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    # Check student_id
    if not guardian.student_id:
        raise HTTPException(
            status_code=400,
            detail="student_id is required",
        )

    # Check address_id
    if not guardian.address_id:
        raise HTTPException(
            status_code=400,
            detail="address_id is required",
        )

    guardian.created_at = datetime.now()
    guardian.updated_at = datetime.now()

    session.add(guardian)

    try:
        session.commit()
        session.refresh(guardian)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create guardian",
        )

    return guardian


# ============================================================
# GET ALL GUARDIANS
# ============================================================

@app.get("/guardian")
def get_guardians(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    guardians = session.exec(
        select(Guardian)
    ).all()

    return {
        "user": payload,
        "guardians": guardians,
    }


# ============================================================
# GET GUARDIAN BY ID
# ============================================================

@app.get("/guardian/{guardian_id}")
def get_guardian_by_id(
    guardian_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    guardian = session.get(
        Guardian,
        guardian_id,
    )

    if not guardian:
        raise HTTPException(
            status_code=404,
            detail="Guardian not found",
        )

    return guardian


# ============================================================
# UPDATE GUARDIAN
# ============================================================

@app.put("/guardian/{guardian_id}")
def update_guardian(
    guardian_id: int,
    data: Guardian,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    guardian = session.get(
        Guardian,
        guardian_id,
    )

    if not guardian:
        raise HTTPException(
            status_code=404,
            detail="Guardian not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(guardian, key, value)

    guardian.updated_at = datetime.now()

    session.add(guardian)

    try:
        session.commit()
        session.refresh(guardian)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update guardian",
        )

    return guardian


# ============================================================
# DELETE GUARDIAN
# ============================================================

@app.delete("/guardian/{guardian_id}")
def delete_guardian(
    guardian_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    guardian = session.get(
        Guardian,
        guardian_id,
    )

    if not guardian:
        raise HTTPException(
            status_code=404,
            detail="Guardian not found",
        )

    session.delete(guardian)
    session.commit()

    return {
        "details": f"guardian {guardian_id} deleted"
    }


# ============================================================
# STUDENT DOCUMENT
# ============================================================

@app.post("/student-document")
def create_student_document(
    document: StudentDocument,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    # Check student_id
    if not document.student_id:
        raise HTTPException(
            status_code=400,
            detail="student_id is required",
        )

    document.created_at = datetime.now()
    document.updated_at = datetime.now()

    session.add(document)

    try:
        session.commit()
        session.refresh(document)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create student document",
        )

    return document


# ============================================================
# GET ALL STUDENT DOCUMENTS
# ============================================================

@app.get("/student-document")
def get_student_documents(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    documents = session.exec(
        select(StudentDocument)
    ).all()

    return {
        "user": payload,
        "student_documents": documents,
    }


# ============================================================
# GET STUDENT DOCUMENT BY ID
# ============================================================

@app.get("/student-document/{document_id}")
def get_student_document_by_id(
    document_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    document = session.get(
        StudentDocument,
        document_id,
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Student document not found",
        )

    return document


# ============================================================
# UPDATE STUDENT DOCUMENT
# ============================================================

@app.put("/student-document/{document_id}")
def update_student_document(
    document_id: int,
    data: StudentDocument,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    document = session.get(
        StudentDocument,
        document_id,
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Student document not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(document, key, value)

    document.updated_at = datetime.now()

    session.add(document)

    try:
        session.commit()
        session.refresh(document)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update student document",
        )

    return document


# ============================================================
# DELETE STUDENT DOCUMENT
# ============================================================

@app.delete("/student-document/{document_id}")
def delete_student_document(
    document_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    document = session.get(
        StudentDocument,
        document_id,
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Student document not found",
        )

    session.delete(document)
    session.commit()

    return {
        "details": f"student document {document_id} deleted"
    }


# ============================================================
# STUDENT ENROLLMENT
# ============================================================

@app.post("/student-enrollment")
def create_student_enrollment(
    enrollment: StudentEnrollment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    # Check student_id
    if not enrollment.student_id:
        raise HTTPException(
            status_code=400,
            detail="student_id is required",
        )

    # Check class_id
    if not enrollment.class_id:
        raise HTTPException(
            status_code=400,
            detail="class_id is required",
        )

    # Check section_id
    if not enrollment.section_id:
        raise HTTPException(
            status_code=400,
            detail="section_id is required",
        )

    enrollment.created_at = datetime.now()
    enrollment.updated_at = datetime.now()

    session.add(enrollment)

    try:
        session.commit()
        session.refresh(enrollment)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create student enrollment",
        )

    return enrollment


# ============================================================
# GET ALL STUDENT ENROLLMENTS
# ============================================================

@app.get("/student-enrollment")
def get_student_enrollments(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    enrollments = session.exec(
        select(StudentEnrollment)
    ).all()

    return {
        "user": payload,
        "student_enrollments": enrollments,
    }


# ============================================================
# GET STUDENT ENROLLMENT BY ID
# ============================================================

@app.get("/student-enrollment/{enrollment_id}")
def get_student_enrollment_by_id(
    enrollment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    enrollment = session.get(
        StudentEnrollment,
        enrollment_id,
    )

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Student enrollment not found",
        )

    return enrollment


# ============================================================
# UPDATE STUDENT ENROLLMENT
# ============================================================

@app.put("/student-enrollment/{enrollment_id}")
def update_student_enrollment(
    enrollment_id: int,
    data: StudentEnrollment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    enrollment = session.get(
        StudentEnrollment,
        enrollment_id,
    )

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Student enrollment not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(enrollment, key, value)

    enrollment.updated_at = datetime.now()

    session.add(enrollment)

    try:
        session.commit()
        session.refresh(enrollment)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update student enrollment",
        )

    return enrollment


# ============================================================
# DELETE STUDENT ENROLLMENT
# ============================================================

@app.delete("/student-enrollment/{enrollment_id}")
def delete_student_enrollment(
    enrollment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    enrollment = session.get(
        StudentEnrollment,
        enrollment_id,
    )

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Student enrollment not found",
        )

    session.delete(enrollment)
    session.commit()

    return {
        "details": f"student enrollment {enrollment_id} deleted"
    }