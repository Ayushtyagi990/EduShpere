from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from common.auth_middleware import JWTMiddleware
from model import TimeSlot, Timetable, Classroom, Holiday, TimetableVersion
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

DEFAULT_LOAN_DAYS = 14
FINE_PER_DAY = 5.0


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return payload


# --------------------------------------------------------------------------
#-----------------------------------------------------------
@app.post("/timeSlot")
def create_timeSlot(
    timeSlot: TimeSlot,payload: dict = Depends(verify_token),  session: Session = Depends(get_session),
):
    timeSlot.created_at = datetime.now()
    timeSlot.updated_at = datetime.now()
    session.add(timeSlot)
    session.commit()
    session.refresh(timeSlot)
    return timeSlot


@app.get("/timeSlot")
def get_timeSlot(session: Session = Depends(get_session)):
    return session.exec(select(TimeSlot)).all()


@app.get("/timeSlot/{timeSlot_id}")
def get_timeSlot_by_id(timeSlot_id: int, session: Session = Depends(get_session)):
    timeSlot = session.get(TimeSlot, timeSlot_id)
    if not timeSlot:
        raise HTTPException(status_code=404, detail="timeSlot not found")
    return timeSlot


@app.put("/timeSlot/{timeSlot_id}")
def update_timeSlot_by_id(timeSlot_id: int, data:TimeSlot, session: Session = Depends(get_session)):
    timeSlot = session.get(TimeSlot, timeSlot_id)
    if not timeSlot:
        raise HTTPException(status_code=404, detail="timeSlot not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(timeSlot, key, value)
    timeSlot.updated_at = datetime.now()

    session.commit()
    session.refresh(timeSlot)
    return timeSlot


@app.delete("/timeSlot/{timeSlot_id}", status_code=204)
def delete_timeSlot_by_id(timeSlot_id: int, session: Session = Depends(get_session)):
    timeSlot = session.get(TimeSlot, timeSlot_id)
    if not timeSlot:
        raise HTTPException(status_code=404, detail="timeSlot not found")
    session.delete(timeSlot)
    session.commit()
    return {"details": f" {timeSlot_id} deleted"}



@app.post("/timetable")
def create_timetable(
    timetable: Timetable,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    timetable.created_at = datetime.now()
    timetable.updated_at = datetime.now()
    session.add(timetable)
    session.commit()
    session.refresh(timetable)
    return timetable


@app.get("/timetable")
def get_timetable(session: Session = Depends(get_session)):
    return session.exec(select(Timetable)).all()


@app.get("/timetable/{timetable_id}")
def get_timetable_by_id(timetable_id: int, session: Session = Depends(get_session)):
    timetable = session.get(Timetable, timetable_id)
    if not timetable:
        raise HTTPException(status_code=404, detail="timetable not found")
    return timetable


@app.put("/timetable/{timetable_id}")
def update_timetable_by_id(timetable_id: int, data: Timetable, session: Session = Depends(get_session)):
    timetable = session.get(Timetable, timetable_id)
    if not timetable:
        raise HTTPException(status_code=404, detail="timetable not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(timetable, key, value)
    timetable.updated_at = datetime.now()

    session.commit()
    session.refresh(timetable)
    return timetable


@app.delete("/timetable/{timetable_id}", status_code=204)
def delete_timetable_by_id(timetable_id: int, session: Session = Depends(get_session)):
    timetable = session.get(Timetable, timetable_id)
    if not timetable:
        raise HTTPException(status_code=404, detail="timetable not found")
    session.delete(timetable)
    session.commit()
    return {"details": f"timetable {timetable_id} deleted"}



@app.post("/classroom")
def create_classroom(
    classroom: Classroom,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    classroom.created_at = datetime.now()
    classroom.updated_at = datetime.now()
    session.add(classroom)
    session.commit()
    session.refresh(classroom)
    return classroom


@app.get("/classroom")
def get_classroom(session: Session = Depends(get_session)):
    return session.exec(select(Classroom)).all()


@app.get("/classroom/{classroom_id}")
def get_classroom_by_id(classroom_id: int, session: Session = Depends(get_session)):
    classroom = session.get(Classroom,classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="classroom not found")
    return classroom


@app.put("/classroom/{classroom_id}")
def update_classroom_by_id(classroom_id: int, data: Classroom, session: Session = Depends(get_session)):
    classroom = session.get(Classroom, classroom_id)
    if not classroom:
        raise HTTPException(status_code=404, detail="classroom not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(classroom, key, value)
    classroom.updated_at = datetime.now()

    session.commit()
    session.refresh(classroom)
    return classroom


@app.delete("/classroom/{classroom_id}", status_code=204)
def delete_classroom_by_id(classroom_id: int, session: Session = Depends(get_session)):
    classroom = session.get(Classroom, classroom_id)
    if not classroom :
        raise HTTPException(status_code=404, detail="classroom not found")
    session.delete(classroom)
    session.commit()
    return {"details": f"classroom {classroom_id} deleted"}



@app.post("/holiday")
def create_holiday(
    holiday: Holiday,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    holiday.created_at = datetime.now()
    holiday.updated_at = datetime.now()
    session.add(holiday)
    session.commit()
    session.refresh(holiday)
    return holiday


