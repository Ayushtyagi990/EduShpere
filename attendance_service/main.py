from fastapi import FastAPI, Depends, HTTPException
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
from model import AttendanceSession, StudentAttendance, AttendanceSummary
from database import get_session
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()

# Same signing key/algorithm as the users service, since tokens are issued
# there and only verified here.
SECRET_KEY = "priyanshu"
ALGORITHM = "HS256"

app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc"
)

app.add_middleware(JWTMiddleware)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return payload


# --------------------------------------------------------------------------
# AttendanceSession
# --------------------------------------------------------------------------
@app.post("/attendance-session")
def create_attendance_session(
    attendance_session: AttendanceSession,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    attendance_session.created_at = datetime.now()
    attendance_session.updated_at = datetime.now()
    session.add(attendance_session)
    session.commit()
    session.refresh(attendance_session)
    return attendance_session


@app.get("/attendance-session")
def get_attendance_sessions(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    sessions = session.exec(select(AttendanceSession)).all()
    return {"user": payload, "attendance_sessions": sessions}


@app.get("/attendance-session/{attendance_session_id}")
def get_attendance_session_by_id(attendance_session_id: int, session: Session = Depends(get_session)):
    attendance_session = session.get(AttendanceSession, attendance_session_id)
    if not attendance_session:
        raise HTTPException(status_code=404, detail="Attendance session not found")
    return attendance_session


@app.put("/attendance-session/{attendance_session_id}")
def update_attendance_session_by_id(attendance_session_id: int, data: AttendanceSession, session: Session = Depends(get_session)):
    attendance_session = session.get(AttendanceSession, attendance_session_id)
    if not attendance_session:
        raise HTTPException(status_code=404, detail="Attendance session not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(attendance_session, key, value)
    attendance_session.updated_at = datetime.now()

    session.commit()
    session.refresh(attendance_session)
    return attendance_session


@app.delete("/attendance-session/{attendance_session_id}", status_code=204)
def delete_attendance_session_by_id(attendance_session_id: int, session: Session = Depends(get_session)):
    attendance_session = session.get(AttendanceSession, attendance_session_id)
    if not attendance_session:
        raise HTTPException(status_code=404, detail="Attendance session not found")
    session.delete(attendance_session)
    session.commit()
    return {"details": f"attendance session {attendance_session_id} deleted"}


# --------------------------------------------------------------------------
# StudentAttendance
# --------------------------------------------------------------------------
def _roll_up_summary(session: Session, attendance_session: AttendanceSession, student_id: int, status: str):
    """Find or create the AttendanceSummary row this record belongs to and
    recompute its totals and percentage."""
    summary = session.exec(
        select(AttendanceSummary).where(
            AttendanceSummary.student_id == student_id,
            AttendanceSummary.academic_year_id == attendance_session.academic_year_id,
            AttendanceSummary.semester_id == attendance_session.semester_id,
            AttendanceSummary.department_id == attendance_session.department_id,
            AttendanceSummary.program_id == attendance_session.program_id,
            AttendanceSummary.section_id == attendance_session.section_id,
            AttendanceSummary.subject_id == attendance_session.subject_id,
        )
    ).first()

    if not summary:
        summary = AttendanceSummary(
            student_id=student_id,
            academic_year_id=attendance_session.academic_year_id,
            semester_id=attendance_session.semester_id,
            department_id=attendance_session.department_id,
            program_id=attendance_session.program_id,
            section_id=attendance_session.section_id,
            subject_id=attendance_session.subject_id,
            total_classes_held=0,
            total_classes_attended=0,
            created_at=datetime.now(),
        )

    summary.total_classes_held = (summary.total_classes_held or 0) + 1
    if status == "present":
        summary.total_classes_attended = (summary.total_classes_attended or 0) + 1
    summary.attendance_percentage = round(
        (summary.total_classes_attended / summary.total_classes_held) * 100, 2
    )
    summary.updated_at = datetime.now()

    session.add(summary)
    session.commit()
    return summary


@app.post("/student-attendance")
def create_student_attendance(
    student_attendance: StudentAttendance,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    attendance_session = session.get(AttendanceSession, student_attendance.attendance_session_id)
    if not attendance_session:
        raise HTTPException(status_code=404, detail="Attendance session not found")

    student_attendance.status = student_attendance.status or "present"
    student_attendance.created_at = datetime.now()
    student_attendance.updated_at = datetime.now()

    session.add(student_attendance)
    try:
        session.commit()
        session.refresh(student_attendance)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to record attendance with these details")

    _roll_up_summary(
        session,
        attendance_session,
        student_attendance.student_id,
        student_attendance.status,
    )

    return student_attendance


@app.get("/student-attendance")
def get_student_attendance(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    records = session.exec(select(StudentAttendance)).all()
    return {"user": payload, "student_attendance": records}


@app.get("/student-attendance/{student_attendance_id}")
def get_student_attendance_by_id(student_attendance_id: int, session: Session = Depends(get_session)):
    record = session.get(StudentAttendance, student_attendance_id)
    if not record:
        raise HTTPException(status_code=404, detail="Student attendance record not found")
    return record


@app.put("/student-attendance/{student_attendance_id}")
def update_student_attendance_by_id(student_attendance_id: int, data: StudentAttendance, session: Session = Depends(get_session)):
    record = session.get(StudentAttendance, student_attendance_id)
    if not record:
        raise HTTPException(status_code=404, detail="Student attendance record not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    record.updated_at = datetime.now()

    session.commit()
    session.refresh(record)
    return record


@app.delete("/student-attendance/{student_attendance_id}", status_code=204)
def delete_student_attendance_by_id(student_attendance_id: int, session: Session = Depends(get_session)):
    record = session.get(StudentAttendance, student_attendance_id)
    if not record:
        raise HTTPException(status_code=404, detail="Student attendance record not found")
    session.delete(record)
    session.commit()
    return {"details": f"student attendance {student_attendance_id} deleted"}


# --------------------------------------------------------------------------
# AttendanceSummary
# --------------------------------------------------------------------------
@app.get("/attendance-summary")
def get_attendance_summaries(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    summaries = session.exec(select(AttendanceSummary)).all()
    return {"user": payload, "attendance_summaries": summaries}


@app.get("/attendance-summary/{attendance_summary_id}")
def get_attendance_summary_by_id(attendance_summary_id: int, session: Session = Depends(get_session)):
    summary = session.get(AttendanceSummary, attendance_summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Attendance summary not found")
    return summary


@app.get("/attendance-summary/student/{student_id}")
def get_attendance_summary_by_student(student_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(AttendanceSummary).where(AttendanceSummary.student_id == student_id)
    ).all()


@app.delete("/attendance-summary/{attendance_summary_id}", status_code=204)
def delete_attendance_summary_by_id(attendance_summary_id: int, session: Session = Depends(get_session)):
    summary = session.get(AttendanceSummary, attendance_summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Attendance summary not found")
    session.delete(summary)
    session.commit()
    return {"details": f"attendance summary {attendance_summary_id} deleted"}