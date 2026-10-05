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
from model import (
    ExamType,
    Examination,
    ExamSchedule,
    StudentMark,
    Result,
    GradeScale,
)
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


def grade_from_percentage(session: Session, percentage: float):
    """Look up the GradeScale row whose range contains this percentage."""
    scales = session.exec(select(GradeScale)).all()
    for scale in scales:
        if scale.min_percentage is None or scale.max_percentage is None:
            continue
        if scale.min_percentage <= percentage <= scale.max_percentage:
            return scale
    return None


# --------------------------------------------------------------------------
# ExamType
# --------------------------------------------------------------------------
@app.post("/exam-type")
def create_exam_type(
    exam_type: ExamType,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    exam_type.created_at = datetime.now()
    exam_type.updated_at = datetime.now()
    session.add(exam_type)
    session.commit()
    session.refresh(exam_type)
    return exam_type


@app.get("/exam-type")
def get_exam_types(session: Session = Depends(get_session)):
    return session.exec(select(ExamType)).all()


@app.get("/exam-type/{exam_type_id}")
def get_exam_type_by_id(exam_type_id: int, session: Session = Depends(get_session)):
    exam_type = session.get(ExamType, exam_type_id)
    if not exam_type:
        raise HTTPException(status_code=404, detail="Exam type not found")
    return exam_type


@app.put("/exam-type/{exam_type_id}")
def update_exam_type_by_id(exam_type_id: int, data: ExamType, session: Session = Depends(get_session)):
    exam_type = session.get(ExamType, exam_type_id)
    if not exam_type:
        raise HTTPException(status_code=404, detail="Exam type not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(exam_type, key, value)
    exam_type.updated_at = datetime.now()

    session.commit()
    session.refresh(exam_type)
    return exam_type


@app.delete("/exam-type/{exam_type_id}", status_code=204)
def delete_exam_type_by_id(exam_type_id: int, session: Session = Depends(get_session)):
    exam_type = session.get(ExamType, exam_type_id)
    if not exam_type:
        raise HTTPException(status_code=404, detail="Exam type not found")
    session.delete(exam_type)
    session.commit()
    return {"details": f"exam type {exam_type_id} deleted"}


# --------------------------------------------------------------------------
# Examination
# --------------------------------------------------------------------------
@app.post("/examination")
def create_examination(
    examination: Examination,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    exam_type = session.get(ExamType, examination.examtype_id)
    if not exam_type:
        raise HTTPException(status_code=404, detail="Exam type not found")

    examination.created_at = datetime.now()
    examination.updated_at = datetime.now()
    session.add(examination)
    session.commit()
    session.refresh(examination)
    return examination


@app.get("/examination")
def get_examinations(session: Session = Depends(get_session)):
    return session.exec(select(Examination)).all()


@app.get("/examination/{examination_id}")
def get_examination_by_id(examination_id: int, session: Session = Depends(get_session)):
    examination = session.get(Examination, examination_id)
    if not examination:
        raise HTTPException(status_code=404, detail="Examination not found")
    return examination


@app.put("/examination/{examination_id}")
def update_examination_by_id(examination_id: int, data: Examination, session: Session = Depends(get_session)):
    examination = session.get(Examination, examination_id)
    if not examination:
        raise HTTPException(status_code=404, detail="Examination not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(examination, key, value)
    examination.updated_at = datetime.now()

    session.commit()
    session.refresh(examination)
    return examination


@app.delete("/examination/{examination_id}", status_code=204)
def delete_examination_by_id(examination_id: int, session: Session = Depends(get_session)):
    examination = session.get(Examination, examination_id)
    if not examination:
        raise HTTPException(status_code=404, detail="Examination not found")
    session.delete(examination)
    session.commit()
    return {"details": f"examination {examination_id} deleted"}


# --------------------------------------------------------------------------
# ExamSchedule
# --------------------------------------------------------------------------
@app.post("/exam-schedule")
def create_exam_schedule(
    exam_schedule: ExamSchedule,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    examination = session.get(Examination, exam_schedule.examination_id)
    if not examination:
        raise HTTPException(status_code=404, detail="Examination not found")

    exam_schedule.created_at = datetime.now()
    exam_schedule.updated_at = datetime.now()
    session.add(exam_schedule)
    session.commit()
    session.refresh(exam_schedule)
    return exam_schedule


@app.get("/exam-schedule")
def get_exam_schedules(session: Session = Depends(get_session)):
    return session.exec(select(ExamSchedule)).all()


@app.get("/exam-schedule/{exam_schedule_id}")
def get_exam_schedule_by_id(exam_schedule_id: int, session: Session = Depends(get_session)):
    exam_schedule = session.get(ExamSchedule, exam_schedule_id)
    if not exam_schedule:
        raise HTTPException(status_code=404, detail="Exam schedule not found")
    return exam_schedule


@app.put("/exam-schedule/{exam_schedule_id}")
def update_exam_schedule_by_id(exam_schedule_id: int, data: ExamSchedule, session: Session = Depends(get_session)):
    exam_schedule = session.get(ExamSchedule, exam_schedule_id)
    if not exam_schedule:
        raise HTTPException(status_code=404, detail="Exam schedule not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(exam_schedule, key, value)
    exam_schedule.updated_at = datetime.now()

    session.commit()
    session.refresh(exam_schedule)
    return exam_schedule


@app.delete("/exam-schedule/{exam_schedule_id}", status_code=204)
def delete_exam_schedule_by_id(exam_schedule_id: int, session: Session = Depends(get_session)):
    exam_schedule = session.get(ExamSchedule, exam_schedule_id)
    if not exam_schedule:
        raise HTTPException(status_code=404, detail="Exam schedule not found")
    session.delete(exam_schedule)
    session.commit()
    return {"details": f"exam schedule {exam_schedule_id} deleted"}


# --------------------------------------------------------------------------
# StudentMark
# --------------------------------------------------------------------------
@app.post("/student-mark")
def create_student_mark(
    student_mark: StudentMark,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    exam_schedule = session.get(ExamSchedule, student_mark.examschedule_id)
    if not exam_schedule:
        raise HTTPException(status_code=404, detail="Exam schedule not found")

    if student_mark.marks_obtained is None:
        raise HTTPException(status_code=400, detail="marks_obtained is required")

    student_mark.total_marks = student_mark.total_marks or exam_schedule.total_marks
    student_mark.created_at = datetime.now()
    student_mark.updated_at = datetime.now()

    if student_mark.total_marks:
        percentage = (student_mark.marks_obtained / student_mark.total_marks) * 100
        scale = grade_from_percentage(session, percentage)
        student_mark.grade = student_mark.grade or (scale.grade if scale else None)

        passing_marks = exam_schedule.passing_marks
        if passing_marks is not None:
            student_mark.result_status = (
                "pass" if student_mark.marks_obtained >= passing_marks else "fail"
            )

    session.add(student_mark)
    try:
        session.commit()
        session.refresh(student_mark)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to record marks with these details")
    return student_mark


@app.get("/student-mark")
def get_student_marks(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    marks = session.exec(select(StudentMark)).all()
    return {"user": payload, "student_marks": marks}


@app.get("/student-mark/{student_mark_id}")
def get_student_mark_by_id(student_mark_id: int, session: Session = Depends(get_session)):
    mark = session.get(StudentMark, student_mark_id)
    if not mark:
        raise HTTPException(status_code=404, detail="Student mark not found")
    return mark


@app.get("/student-mark/student/{student_id}")
def get_student_marks_by_student(student_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(StudentMark).where(StudentMark.student_id == student_id)
    ).all()


@app.put("/student-mark/{student_mark_id}")
def update_student_mark_by_id(student_mark_id: int, data: StudentMark, session: Session = Depends(get_session)):
    mark = session.get(StudentMark, student_mark_id)
    if not mark:
        raise HTTPException(status_code=404, detail="Student mark not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(mark, key, value)
    mark.updated_at = datetime.now()

    session.commit()
    session.refresh(mark)
    return mark


@app.delete("/student-mark/{student_mark_id}", status_code=204)
def delete_student_mark_by_id(student_mark_id: int, session: Session = Depends(get_session)):
    mark = session.get(StudentMark, student_mark_id)
    if not mark:
        raise HTTPException(status_code=404, detail="Student mark not found")
    session.delete(mark)
    session.commit()
    return {"details": f"student mark {student_mark_id} deleted"}


# --------------------------------------------------------------------------
# Result
# --------------------------------------------------------------------------
@app.post("/result")
def create_result(
    result: Result,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    examination = session.get(Examination, result.examination_id)
    if not examination:
        raise HTTPException(status_code=404, detail="Examination not found")

    result.created_at = datetime.now()
    result.updated_at = datetime.now()

    if result.marks_obtained is not None and result.total_marks:
        percentage = (result.marks_obtained / result.total_marks) * 100
        scale = grade_from_percentage(session, percentage)
        result.grade = result.grade or (scale.grade if scale else None)
        if result.cgpa is None and scale:
            result.cgpa = scale.grade_point

    session.add(result)
    try:
        session.commit()
        session.refresh(result)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to create result with these details")
    return result


@app.get("/result")
def get_results(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    results = session.exec(select(Result)).all()
    return {"user": payload, "results": results}


@app.get("/result/{result_id}")
def get_result_by_id(result_id: int, session: Session = Depends(get_session)):
    result = session.get(Result, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result


@app.get("/result/student/{student_id}")
def get_results_by_student(student_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Result).where(Result.student_id == student_id)).all()


@app.put("/result/{result_id}")
def update_result_by_id(result_id: int, data: Result, session: Session = Depends(get_session)):
    result = session.get(Result, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(result, key, value)
    result.updated_at = datetime.now()

    session.commit()
    session.refresh(result)
    return result


@app.delete("/result/{result_id}", status_code=204)
def delete_result_by_id(result_id: int, session: Session = Depends(get_session)):
    result = session.get(Result, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    session.delete(result)
    session.commit()
    return {"details": f"result {result_id} deleted"}


# --------------------------------------------------------------------------
# GradeScale
# --------------------------------------------------------------------------
@app.post("/grade-scale")
def create_grade_scale(
    grade_scale: GradeScale,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    grade_scale.created_at = datetime.now()
    grade_scale.updated_at = datetime.now()
    session.add(grade_scale)
    session.commit()
    session.refresh(grade_scale)
    return grade_scale


@app.get("/grade-scale")
def get_grade_scales(session: Session = Depends(get_session)):
    return session.exec(select(GradeScale)).all()


@app.get("/grade-scale/{grade_scale_id}")
def get_grade_scale_by_id(grade_scale_id: int, session: Session = Depends(get_session)):
    grade_scale = session.get(GradeScale, grade_scale_id)
    if not grade_scale:
        raise HTTPException(status_code=404, detail="Grade scale not found")
    return grade_scale


@app.put("/grade-scale/{grade_scale_id}")
def update_grade_scale_by_id(grade_scale_id: int, data: GradeScale, session: Session = Depends(get_session)):
    grade_scale = session.get(GradeScale, grade_scale_id)
    if not grade_scale:
        raise HTTPException(status_code=404, detail="Grade scale not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(grade_scale, key, value)
    grade_scale.updated_at = datetime.now()

    session.commit()
    session.refresh(grade_scale)
    return grade_scale


@app.delete("/grade-scale/{grade_scale_id}", status_code=204)
def delete_grade_scale_by_id(grade_scale_id: int, session: Session = Depends(get_session)):
    grade_scale = session.get(GradeScale, grade_scale_id)
    if not grade_scale:
        raise HTTPException(status_code=404, detail="Grade scale not found")
    session.delete(grade_scale)
    session.commit()
    return {"details": f"grade scale {grade_scale_id} deleted"}