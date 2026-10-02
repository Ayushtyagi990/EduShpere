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
from model import LeaveType, LeaveRequest, LeaveApprovalHistory
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
# LeaveType
# --------------------------------------------------------------------------
@app.post("/leave-type")
def create_leave_type(
    leave_type: LeaveType,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    leave_type.created_at = datetime.now()
    leave_type.updated_at = datetime.now()
    session.add(leave_type)
    session.commit()
    session.refresh(leave_type)
    return leave_type


@app.get("/leave-type")
def get_leave_types(session: Session = Depends(get_session)):
    return session.exec(select(LeaveType)).all()


@app.get("/leave-type/{leave_type_id}")
def get_leave_type_by_id(leave_type_id: int, session: Session = Depends(get_session)):
    leave_type = session.get(LeaveType, leave_type_id)
    if not leave_type:
        raise HTTPException(status_code=404, detail="Leave type not found")
    return leave_type


@app.put("/leave-type/{leave_type_id}")
def update_leave_type_by_id(leave_type_id: int, data: LeaveType, session: Session = Depends(get_session)):
    leave_type = session.get(LeaveType, leave_type_id)
    if not leave_type:
        raise HTTPException(status_code=404, detail="Leave type not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(leave_type, key, value)
    leave_type.updated_at = datetime.now()

    session.commit()
    session.refresh(leave_type)
    return leave_type


@app.delete("/leave-type/{leave_type_id}", status_code=204)
def delete_leave_type_by_id(leave_type_id: int, session: Session = Depends(get_session)):
    leave_type = session.get(LeaveType, leave_type_id)
    if not leave_type:
        raise HTTPException(status_code=404, detail="Leave type not found")
    session.delete(leave_type)
    session.commit()
    return {"details": f"leave type {leave_type_id} deleted"}


# --------------------------------------------------------------------------
# LeaveRequest
# --------------------------------------------------------------------------
@app.post("/leave-request")
def create_leave_request(
    leave_request: LeaveRequest,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    leave_type = session.get(LeaveType, leave_request.leave_type_id)
    if not leave_type:
        raise HTTPException(status_code=404, detail="Leave type not found")

    if leave_request.start_date and leave_request.end_date:
        if leave_request.end_date < leave_request.start_date:
            raise HTTPException(status_code=400, detail="end_date cannot be before start_date")

        requested_days = (leave_request.end_date - leave_request.start_date).days + 1
        if leave_type.max_days is not None and requested_days > leave_type.max_days:
            raise HTTPException(
                status_code=400,
                detail=f"Requested {requested_days} days exceeds the {leave_type.max_days}-day limit for this leave type",
            )

    leave_request.user_id = leave_request.user_id or payload.get("id")
    leave_request.status = leave_request.status or "pending"
    leave_request.created_at = datetime.now()
    leave_request.updated_at = datetime.now()

    session.add(leave_request)
    try:
        session.commit()
        session.refresh(leave_request)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to create leave request with these details")
    return leave_request


@app.get("/leave-request")
def get_leave_requests(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    leave_requests = session.exec(select(LeaveRequest)).all()
    return {"user": payload, "leave_requests": leave_requests}


@app.get("/leave-request/{leave_request_id}")
def get_leave_request_by_id(leave_request_id: int, session: Session = Depends(get_session)):
    leave_request = session.get(LeaveRequest, leave_request_id)
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return leave_request


@app.get("/leave-request/user/{user_id}")
def get_leave_requests_by_user(user_id: int, session: Session = Depends(get_session)):
    return session.exec(select(LeaveRequest).where(LeaveRequest.user_id == user_id)).all()


@app.put("/leave-request/{leave_request_id}")
def update_leave_request_by_id(leave_request_id: int, data: LeaveRequest, session: Session = Depends(get_session)):
    leave_request = session.get(LeaveRequest, leave_request_id)
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(leave_request, key, value)
    leave_request.updated_at = datetime.now()

    session.commit()
    session.refresh(leave_request)
    return leave_request


@app.delete("/leave-request/{leave_request_id}", status_code=204)
def delete_leave_request_by_id(leave_request_id: int, session: Session = Depends(get_session)):
    leave_request = session.get(LeaveRequest, leave_request_id)
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    session.delete(leave_request)
    session.commit()
    return {"details": f"leave request {leave_request_id} deleted"}


# --------------------------------------------------------------------------
# LeaveApprovalHistory
# --------------------------------------------------------------------------
VALID_ACTIONS = {"approved", "rejected"}


@app.post("/leave-approval-history")
def create_leave_approval_history(
    leave_approval_history: LeaveApprovalHistory,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    leave_request = session.get(LeaveRequest, leave_approval_history.leave_request_id)
    if not leave_request:
        raise HTTPException(status_code=404, detail="Leave request not found")

    if leave_request.status != "pending":
        raise HTTPException(
            status_code=409,
            detail=f"Leave request is already '{leave_request.status}' and cannot be acted on again",
        )

    if leave_approval_history.action not in VALID_ACTIONS:
        raise HTTPException(status_code=400, detail=f"action must be one of {sorted(VALID_ACTIONS)}")

    leave_approval_history.approver_id = leave_approval_history.approver_id or payload.get("id")
    leave_approval_history.action_date = leave_approval_history.action_date or datetime.now()
    leave_approval_history.created_at = datetime.now()
    leave_approval_history.updated_at = datetime.now()

    session.add(leave_approval_history)
    try:
        session.commit()
        session.refresh(leave_approval_history)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to record approval action with these details")

    # The approval action is the thing that actually moves the leave request forward.
    leave_request.status = leave_approval_history.action
    leave_request.updated_at = datetime.now()
    session.add(leave_request)
    session.commit()

    return leave_approval_history


@app.get("/leave-approval-history")
def get_leave_approval_history(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    history = session.exec(select(LeaveApprovalHistory)).all()
    return {"user": payload, "leave_approval_history": history}


@app.get("/leave-approval-history/{leave_approval_history_id}")
def get_leave_approval_history_by_id(leave_approval_history_id: int, session: Session = Depends(get_session)):
    record = session.get(LeaveApprovalHistory, leave_approval_history_id)
    if not record:
        raise HTTPException(status_code=404, detail="Leave approval history record not found")
    return record


@app.get("/leave-approval-history/leave-request/{leave_request_id}")
def get_leave_approval_history_by_request(leave_request_id: int, session: Session = Depends(get_session)):
    return session.exec(
        select(LeaveApprovalHistory)
        .where(LeaveApprovalHistory.leave_request_id == leave_request_id)
        .order_by(LeaveApprovalHistory.action_date)
    ).all()


@app.delete("/leave-approval-history/{leave_approval_history_id}", status_code=204)
def delete_leave_approval_history_by_id(leave_approval_history_id: int, session: Session = Depends(get_session)):
    record = session.get(LeaveApprovalHistory, leave_approval_history_id)
    if not record:
        raise HTTPException(status_code=404, detail="Leave approval history record not found")
    session.delete(record)
    session.commit()
    return {"details": f"leave approval history {leave_approval_history_id} deleted"}