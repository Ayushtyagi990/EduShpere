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
    Pension,
    PensionScheme,
    PensionContribution,
    PensionCalculation,
    PensionRequest,
    PensionApproval,
    PensionPayment,
    PensionAdjustment,
    PensionNominee,
    PensionBeneficiary,
    PensionDocument,
    PensionStatusHistory,
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
# PENSION
# ============================================================

@app.post("/pension")
def create_pension(
    pension: Pension,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not pension.employee_id:
        raise HTTPException(
            status_code=400,
            detail="employee_id is required",
        )

    if pension.scheme_id:
        scheme = session.get(
            PensionScheme,
            pension.scheme_id,
        )

        if not scheme:
            raise HTTPException(
                status_code=404,
                detail="Pension scheme not found",
            )

    pension.created_at = datetime.now()
    pension.updated_at = datetime.now()

    session.add(pension)

    try:
        session.commit()
        session.refresh(pension)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension",
        )

    return pension


@app.get("/pension")
def get_pensions(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    pensions = session.exec(
        select(Pension)
    ).all()

    return {
        "user": payload,
        "pensions": pensions,
    }


@app.get("/pension/{pension_id}")
def get_pension_by_id(
    pension_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    pension = session.get(
        Pension,
        pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
        )

    return pension


@app.put("/pension/{pension_id}")
def update_pension(
    pension_id: int,
    data: Pension,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    pension = session.get(
        Pension,
        pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(pension, key, value)

    pension.updated_at = datetime.now()

    session.add(pension)

    try:
        session.commit()
        session.refresh(pension)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension",
        )

    return pension


@app.delete("/pension/{pension_id}")
def delete_pension(
    pension_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    pension = session.get(
        Pension,
        pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
        )

    session.delete(pension)
    session.commit()

    return {
        "details": f"pension {pension_id} deleted"
    }


# ============================================================
# PENSION SCHEME
# ============================================================

@app.post("/pension-scheme")
def create_pension_scheme(
    scheme: PensionScheme,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not scheme.name:
        raise HTTPException(
            status_code=400,
            detail="name is required",
        )

    scheme.created_at = datetime.now()
    scheme.updated_at = datetime.now()

    session.add(scheme)

    try:
        session.commit()
        session.refresh(scheme)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension scheme",
        )

    return scheme


@app.get("/pension-scheme")
def get_pension_schemes(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    schemes = session.exec(
        select(PensionScheme)
    ).all()

    return {
        "user": payload,
        "pension_schemes": schemes,
    }


@app.get("/pension-scheme/{scheme_id}")
def get_pension_scheme_by_id(
    scheme_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    scheme = session.get(
        PensionScheme,
        scheme_id,
    )

    if not scheme:
        raise HTTPException(
            status_code=404,
            detail="Pension scheme not found",
        )

    return scheme


@app.put("/pension-scheme/{scheme_id}")
def update_pension_scheme(
    scheme_id: int,
    data: PensionScheme,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    scheme = session.get(
        PensionScheme,
        scheme_id,
    )

    if not scheme:
        raise HTTPException(
            status_code=404,
            detail="Pension scheme not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(scheme, key, value)

    scheme.updated_at = datetime.now()

    session.add(scheme)

    try:
        session.commit()
        session.refresh(scheme)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension scheme",
        )

    return scheme


@app.delete("/pension-scheme/{scheme_id}")
def delete_pension_scheme(
    scheme_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    scheme = session.get(
        PensionScheme,
        scheme_id,
    )

    if not scheme:
        raise HTTPException(
            status_code=404,
            detail="Pension scheme not found",
        )

    session.delete(scheme)
    session.commit()

    return {
        "details": f"pension scheme {scheme_id} deleted"
    }


# ============================================================
# PENSION CONTRIBUTION
# ============================================================

@app.post("/pension-contribution")
def create_pension_contribution(
    contribution: PensionContribution,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not contribution.pension_id:
        raise HTTPException(
            status_code=400,
            detail="pension_id is required",
        )

    if not contribution.employee_id:
        raise HTTPException(
            status_code=400,
            detail="employee_id is required",
        )

    pension = session.get(
        Pension,
        contribution.pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
        )

    contribution.created_at = datetime.now()
    contribution.updated_at = datetime.now()

    session.add(contribution)

    try:
        session.commit()
        session.refresh(contribution)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension contribution",
        )

    return contribution


@app.get("/pension-contribution")
def get_pension_contributions(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    contributions = session.exec(
        select(PensionContribution)
    ).all()

    return {
        "user": payload,
        "pension_contributions": contributions,
    }


@app.get("/pension-contribution/{contribution_id}")
def get_pension_contribution_by_id(
    contribution_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    contribution = session.get(
        PensionContribution,
        contribution_id,
    )

    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="Pension contribution not found",
        )

    return contribution


@app.put("/pension-contribution/{contribution_id}")
def update_pension_contribution(
    contribution_id: int,
    data: PensionContribution,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    contribution = session.get(
        PensionContribution,
        contribution_id,
    )

    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="Pension contribution not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(contribution, key, value)

    contribution.updated_at = datetime.now()

    session.add(contribution)

    try:
        session.commit()
        session.refresh(contribution)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension contribution",
        )

    return contribution


@app.delete("/pension-contribution/{contribution_id}")
def delete_pension_contribution(
    contribution_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    contribution = session.get(
        PensionContribution,
        contribution_id,
    )

    if not contribution:
        raise HTTPException(
            status_code=404,
            detail="Pension contribution not found",
        )

    session.delete(contribution)
    session.commit()

    return {
        "details": f"pension contribution {contribution_id} deleted"
    }


# ============================================================
# PENSION CALCULATION
# ============================================================

@app.post("/pension-calculation")
def create_pension_calculation(
    calculation: PensionCalculation,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not calculation.pension_id:
        raise HTTPException(
            status_code=400,
            detail="pension_id is required",
        )

    pension = session.get(
        Pension,
        calculation.pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
        )

    calculation.created_at = datetime.now()
    calculation.updated_at = datetime.now()

    session.add(calculation)

    try:
        session.commit()
        session.refresh(calculation)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension calculation",
        )

    return calculation


@app.get("/pension-calculation")
def get_pension_calculations(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    calculations = session.exec(
        select(PensionCalculation)
    ).all()

    return {
        "user": payload,
        "pension_calculations": calculations,
    }


@app.get("/pension-calculation/{calculation_id}")
def get_pension_calculation_by_id(
    calculation_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    calculation = session.get(
        PensionCalculation,
        calculation_id,
    )

    if not calculation:
        raise HTTPException(
            status_code=404,
            detail="Pension calculation not found",
        )

    return calculation


@app.put("/pension-calculation/{calculation_id}")
def update_pension_calculation(
    calculation_id: int,
    data: PensionCalculation,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    calculation = session.get(
        PensionCalculation,
        calculation_id,
    )

    if not calculation:
        raise HTTPException(
            status_code=404,
            detail="Pension calculation not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(calculation, key, value)

    calculation.updated_at = datetime.now()

    session.add(calculation)

    try:
        session.commit()
        session.refresh(calculation)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension calculation",
        )

    return calculation


@app.delete("/pension-calculation/{calculation_id}")
def delete_pension_calculation(
    calculation_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    calculation = session.get(
        PensionCalculation,
        calculation_id,
    )

    if not calculation:
        raise HTTPException(
            status_code=404,
            detail="Pension calculation not found",
        )

    session.delete(calculation)
    session.commit()

    return {
        "details": f"pension calculation {calculation_id} deleted"
    }


# ============================================================
# PENSION REQUEST
# ============================================================

@app.post("/pension-request")
def create_pension_request(
    request: PensionRequest,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not request.employee_id:
        raise HTTPException(
            status_code=400,
            detail="employee_id is required",
        )

    if request.pension_id:
        pension = session.get(
            Pension,
            request.pension_id,
        )

        if not pension:
            raise HTTPException(
                status_code=404,
                detail="Pension not found",
            )

    request.created_at = datetime.now()
    request.updated_at = datetime.now()

    session.add(request)

    try:
        session.commit()
        session.refresh(request)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension request",
        )

    return request


@app.get("/pension-request")
def get_pension_requests(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    requests = session.exec(
        select(PensionRequest)
    ).all()

    return {
        "user": payload,
        "pension_requests": requests,
    }


@app.get("/pension-request/{request_id}")
def get_pension_request_by_id(
    request_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    request = session.get(
        PensionRequest,
        request_id,
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Pension request not found",
        )

    return request


@app.put("/pension-request/{request_id}")
def update_pension_request(
    request_id: int,
    data: PensionRequest,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    request = session.get(
        PensionRequest,
        request_id,
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Pension request not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(request, key, value)

    request.updated_at = datetime.now()

    session.add(request)

    try:
        session.commit()
        session.refresh(request)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension request",
        )

    return request


@app.delete("/pension-request/{request_id}")
def delete_pension_request(
    request_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    request = session.get(
        PensionRequest,
        request_id,
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Pension request not found",
        )

    session.delete(request)
    session.commit()

    return {
        "details": f"pension request {request_id} deleted"
    }


# ============================================================
# PENSION APPROVAL
# ============================================================

@app.post("/pension-approval")
def create_pension_approval(
    approval: PensionApproval,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not approval.pension_request_id:
        raise HTTPException(
            status_code=400,
            detail="pension_request_id is required",
        )

    if not approval.approver_user_id:
        raise HTTPException(
            status_code=400,
            detail="approver_user_id is required",
        )

    request = session.get(
        PensionRequest,
        approval.pension_request_id,
    )

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Pension request not found",
        )

    approval.created_at = datetime.now()
    approval.updated_at = datetime.now()

    session.add(approval)

    try:
        session.commit()
        session.refresh(approval)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension approval",
        )

    return approval


@app.get("/pension-approval")
def get_pension_approvals(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    approvals = session.exec(
        select(PensionApproval)
    ).all()

    return {
        "user": payload,
        "pension_approvals": approvals,
    }


@app.get("/pension-approval/{approval_id}")
def get_pension_approval_by_id(
    approval_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    approval = session.get(
        PensionApproval,
        approval_id,
    )

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Pension approval not found",
        )

    return approval


@app.put("/pension-approval/{approval_id}")
def update_pension_approval(
    approval_id: int,
    data: PensionApproval,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    approval = session.get(
        PensionApproval,
        approval_id,
    )

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Pension approval not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(approval, key, value)

    approval.updated_at = datetime.now()

    session.add(approval)

    try:
        session.commit()
        session.refresh(approval)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension approval",
        )

    return approval


@app.delete("/pension-approval/{approval_id}")
def delete_pension_approval(
    approval_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    approval = session.get(
        PensionApproval,
        approval_id,
    )

    if not approval:
        raise HTTPException(
            status_code=404,
            detail="Pension approval not found",
        )

    session.delete(approval)
    session.commit()

    return {
        "details": f"pension approval {approval_id} deleted"
    }


# ============================================================
# PENSION PAYMENT
# ============================================================

@app.post("/pension-payment")
def create_pension_payment(
    payment: PensionPayment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not payment.pension_id:
        raise HTTPException(
            status_code=400,
            detail="pension_id is required",
        )

    if not payment.employee_id:
        raise HTTPException(
            status_code=400,
            detail="employee_id is required",
        )

    pension = session.get(
        Pension,
        payment.pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
        )

    payment.created_at = datetime.now()
    payment.updated_at = datetime.now()

    session.add(payment)

    try:
        session.commit()
        session.refresh(payment)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension payment",
        )

    return payment


@app.get("/pension-payment")
def get_pension_payments(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    payments = session.exec(
        select(PensionPayment)
    ).all()

    return {
        "user": payload,
        "pension_payments": payments,
    }


@app.get("/pension-payment/{payment_id}")
def get_pension_payment_by_id(
    payment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    payment = session.get(
        PensionPayment,
        payment_id,
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Pension payment not found",
        )

    return payment


@app.put("/pension-payment/{payment_id}")
def update_pension_payment(
    payment_id: int,
    data: PensionPayment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    payment = session.get(
        PensionPayment,
        payment_id,
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Pension payment not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(payment, key, value)

    payment.updated_at = datetime.now()

    session.add(payment)

    try:
        session.commit()
        session.refresh(payment)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension payment",
        )

    return payment


@app.delete("/pension-payment/{payment_id}")
def delete_pension_payment(
    payment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    payment = session.get(
        PensionPayment,
        payment_id,
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Pension payment not found",
        )

    session.delete(payment)
    session.commit()

    return {
        "details": f"pension payment {payment_id} deleted"
    }


# ============================================================
# PENSION ADJUSTMENT
# ============================================================

@app.post("/pension-adjustment")
def create_pension_adjustment(
    adjustment: PensionAdjustment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not adjustment.pension_id:
        raise HTTPException(
            status_code=400,
            detail="pension_id is required",
        )

    if not adjustment.employee_id:
        raise HTTPException(
            status_code=400,
            detail="employee_id is required",
        )

    pension = session.get(
        Pension,
        adjustment.pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
        )

    adjustment.created_at = datetime.now()
    adjustment.updated_at = datetime.now()

    session.add(adjustment)

    try:
        session.commit()
        session.refresh(adjustment)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension adjustment",
        )

    return adjustment


@app.get("/pension-adjustment")
def get_pension_adjustments(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    adjustments = session.exec(
        select(PensionAdjustment)
    ).all()

    return {
        "user": payload,
        "pension_adjustments": adjustments,
    }


@app.get("/pension-adjustment/{adjustment_id}")
def get_pension_adjustment_by_id(
    adjustment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    adjustment = session.get(
        PensionAdjustment,
        adjustment_id,
    )

    if not adjustment:
        raise HTTPException(
            status_code=404,
            detail="Pension adjustment not found",
        )

    return adjustment


@app.put("/pension-adjustment/{adjustment_id}")
def update_pension_adjustment(
    adjustment_id: int,
    data: PensionAdjustment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    adjustment = session.get(
        PensionAdjustment,
        adjustment_id,
    )

    if not adjustment:
        raise HTTPException(
            status_code=404,
            detail="Pension adjustment not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(adjustment, key, value)

    adjustment.updated_at = datetime.now()

    session.add(adjustment)

    try:
        session.commit()
        session.refresh(adjustment)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension adjustment",
        )

    return adjustment


@app.delete("/pension-adjustment/{adjustment_id}")
def delete_pension_adjustment(
    adjustment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    adjustment = session.get(
        PensionAdjustment,
        adjustment_id,
    )

    if not adjustment:
        raise HTTPException(
            status_code=404,
            detail="Pension adjustment not found",
        )

    session.delete(adjustment)
    session.commit()

    return {
        "details": f"pension adjustment {adjustment_id} deleted"
    }


# ============================================================
# PENSION NOMINEE
# ============================================================

@app.post("/pension-nominee")
def create_pension_nominee(
    nominee: PensionNominee,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not nominee.pension_id:
        raise HTTPException(
            status_code=400,
            detail="pension_id is required",
        )

    if not nominee.employee_id:
        raise HTTPException(
            status_code=400,
            detail="employee_id is required",
        )

    if not nominee.address_id:
        raise HTTPException(
            status_code=400,
            detail="address_id is required",
        )

    pension = session.get(
        Pension,
        nominee.pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
        )

    nominee.created_at = datetime.now()
    nominee.updated_at = datetime.now()

    session.add(nominee)

    try:
        session.commit()
        session.refresh(nominee)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension nominee",
        )

    return nominee


@app.get("/pension-nominee")
def get_pension_nominees(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    nominees = session.exec(
        select(PensionNominee)
    ).all()

    return {
        "user": payload,
        "pension_nominees": nominees,
    }


@app.get("/pension-nominee/{nominee_id}")
def get_pension_nominee_by_id(
    nominee_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    nominee = session.get(
        PensionNominee,
        nominee_id,
    )

    if not nominee:
        raise HTTPException(
            status_code=404,
            detail="Pension nominee not found",
        )

    return nominee


@app.put("/pension-nominee/{nominee_id}")
def update_pension_nominee(
    nominee_id: int,
    data: PensionNominee,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    nominee = session.get(
        PensionNominee,
        nominee_id,
    )

    if not nominee:
        raise HTTPException(
            status_code=404,
            detail="Pension nominee not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(nominee, key, value)

    nominee.updated_at = datetime.now()

    session.add(nominee)

    try:
        session.commit()
        session.refresh(nominee)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension nominee",
        )

    return nominee


@app.delete("/pension-nominee/{nominee_id}")
def delete_pension_nominee(
    nominee_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    nominee = session.get(
        PensionNominee,
        nominee_id,
    )

    if not nominee:
        raise HTTPException(
            status_code=404,
            detail="Pension nominee not found",
        )

    session.delete(nominee)
    session.commit()

    return {
        "details": f"pension nominee {nominee_id} deleted"
    }


# ============================================================
# PENSION BENEFICIARY
# ============================================================

@app.post("/pension-beneficiary")
def create_pension_beneficiary(
    beneficiary: PensionBeneficiary,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not beneficiary.pension_id:
        raise HTTPException(
            status_code=400,
            detail="pension_id is required",
        )

    if not beneficiary.employee_id:
        raise HTTPException(
            status_code=400,
            detail="employee_id is required",
        )

    if not beneficiary.address_id:
        raise HTTPException(
            status_code=400,
            detail="address_id is required",
        )

    pension = session.get(
        Pension,
        beneficiary.pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
        )

    beneficiary.created_at = datetime.now()
    beneficiary.updated_at = datetime.now()

    session.add(beneficiary)

    try:
        session.commit()
        session.refresh(beneficiary)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension beneficiary",
        )

    return beneficiary


@app.get("/pension-beneficiary")
def get_pension_beneficiaries(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    beneficiaries = session.exec(
        select(PensionBeneficiary)
    ).all()

    return {
        "user": payload,
        "pension_beneficiaries": beneficiaries,
    }


@app.get("/pension-beneficiary/{beneficiary_id}")
def get_pension_beneficiary_by_id(
    beneficiary_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    beneficiary = session.get(
        PensionBeneficiary,
        beneficiary_id,
    )

    if not beneficiary:
        raise HTTPException(
            status_code=404,
            detail="Pension beneficiary not found",
        )

    return beneficiary


@app.put("/pension-beneficiary/{beneficiary_id}")
def update_pension_beneficiary(
    beneficiary_id: int,
    data: PensionBeneficiary,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    beneficiary = session.get(
        PensionBeneficiary,
        beneficiary_id,
    )

    if not beneficiary:
        raise HTTPException(
            status_code=404,
            detail="Pension beneficiary not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(beneficiary, key, value)

    beneficiary.updated_at = datetime.now()

    session.add(beneficiary)

    try:
        session.commit()
        session.refresh(beneficiary)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension beneficiary",
        )

    return beneficiary


@app.delete("/pension-beneficiary/{beneficiary_id}")
def delete_pension_beneficiary(
    beneficiary_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    beneficiary = session.get(
        PensionBeneficiary,
        beneficiary_id,
    )

    if not beneficiary:
        raise HTTPException(
            status_code=404,
            detail="Pension beneficiary not found",
        )

    session.delete(beneficiary)
    session.commit()

    return {
        "details": f"pension beneficiary {beneficiary_id} deleted"
    }


# ============================================================
# PENSION DOCUMENT
# ============================================================

@app.post("/pension-document")
def create_pension_document(
    document: PensionDocument,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not document.pension_id:
        raise HTTPException(
            status_code=400,
            detail="pension_id is required",
        )

    if not document.employee_id:
        raise HTTPException(
            status_code=400,
            detail="employee_id is required",
        )

    pension = session.get(
        Pension,
        document.pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
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
            detail="Unable to create pension document",
        )

    return document


@app.get("/pension-document")
def get_pension_documents(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    documents = session.exec(
        select(PensionDocument)
    ).all()

    return {
        "user": payload,
        "pension_documents": documents,
    }


@app.get("/pension-document/{document_id}")
def get_pension_document_by_id(
    document_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    document = session.get(
        PensionDocument,
        document_id,
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Pension document not found",
        )

    return document


@app.put("/pension-document/{document_id}")
def update_pension_document(
    document_id: int,
    data: PensionDocument,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    document = session.get(
        PensionDocument,
        document_id,
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Pension document not found",
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
            detail="Unable to update pension document",
        )

    return document


@app.delete("/pension-document/{document_id}")
def delete_pension_document(
    document_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    document = session.get(
        PensionDocument,
        document_id,
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Pension document not found",
        )

    session.delete(document)
    session.commit()

    return {
        "details": f"pension document {document_id} deleted"
    }


# ============================================================
# PENSION STATUS HISTORY
# ============================================================

@app.post("/pension-status-history")
def create_pension_status_history(
    history: PensionStatusHistory,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if not history.pension_id:
        raise HTTPException(
            status_code=400,
            detail="pension_id is required",
        )

    if not history.employee_id:
        raise HTTPException(
            status_code=400,
            detail="employee_id is required",
        )

    pension = session.get(
        Pension,
        history.pension_id,
    )

    if not pension:
        raise HTTPException(
            status_code=404,
            detail="Pension not found",
        )

    history.changed_at = datetime.now()
    history.created_at = datetime.now()

    session.add(history)

    try:
        session.commit()
        session.refresh(history)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create pension status history",
        )

    return history


@app.get("/pension-status-history")
def get_pension_status_histories(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    histories = session.exec(
        select(PensionStatusHistory)
    ).all()

    return {
        "user": payload,
        "pension_status_histories": histories,
    }


@app.get("/pension-status-history/{history_id}")
def get_pension_status_history_by_id(
    history_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    history = session.get(
        PensionStatusHistory,
        history_id,
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Pension status history not found",
        )

    return history


@app.put("/pension-status-history/{history_id}")
def update_pension_status_history(
    history_id: int,
    data: PensionStatusHistory,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    history = session.get(
        PensionStatusHistory,
        history_id,
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Pension status history not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(history, key, value)

    history.changed_at = datetime.now()

    session.add(history)

    try:
        session.commit()
        session.refresh(history)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update pension status history",
        )

    return history


@app.delete("/pension-status-history/{history_id}")
def delete_pension_status_history(
    history_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    history = session.get(
        PensionStatusHistory,
        history_id,
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail="Pension status history not found",
        )

    session.delete(history)
    session.commit()

    return {
        "details": f"pension status history {history_id} deleted"
    }