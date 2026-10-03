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
from model import Staff
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
# STAFF
# ============================================================

@app.post("/staff")
def create_staff(
    staff: Staff,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    # Check user_id
    if not staff.user_id:
        raise HTTPException(
            status_code=400,
            detail="user_id is required",
        )

    # Check address_id
    if not staff.address_id:
        raise HTTPException(
            status_code=400,
            detail="address_id is required",
        )

    staff.created_at = datetime.now()
    staff.updated_at = datetime.now()

    session.add(staff)

    try:
        session.commit()
        session.refresh(staff)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create staff",
        )

    return staff


# ============================================================
# GET ALL STAFF
# ============================================================

@app.get("/staff")
def get_staff(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    staff = session.exec(
        select(Staff)
    ).all()

    return {
        "user": payload,
        "staff": staff,
    }


# ============================================================
# GET STAFF BY ID
# ============================================================

@app.get("/staff/{staff_id}")
def get_staff_by_id(
    staff_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    staff = session.get(
        Staff,
        staff_id,
    )

    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff not found",
        )

    return staff


# ============================================================
# UPDATE STAFF
# ============================================================

@app.put("/staff/{staff_id}")
def update_staff(
    staff_id: int,
    data: Staff,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    staff = session.get(
        Staff,
        staff_id,
    )

    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(staff, key, value)

    staff.updated_at = datetime.now()

    session.add(staff)

    try:
        session.commit()
        session.refresh(staff)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update staff",
        )

    return staff


# ============================================================
# DELETE STAFF
# ============================================================

@app.delete("/staff/{staff_id}")
def delete_staff(
    staff_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    staff = session.get(
        Staff,
        staff_id,
    )

    if not staff:
        raise HTTPException(
            status_code=404,
            detail="Staff not found",
        )

    session.delete(staff)
    session.commit()

    return {
        "details": f"staff {staff_id} deleted"
    }