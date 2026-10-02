from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import uuid

import sys
import os

sys.path.append(
     os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from common.auth_middleware import JWTMiddleware
from model import (
    FeeCategory,
    FeeStructure,
    Student_fee,
    Payment,
    Scholarship,
    Fine,
    Receipt,
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


# --------------------------------------------------------------------------
# FeeCategory
# --------------------------------------------------------------------------
@app.post("/fee-category")
def create_fee_category(
    fee_category: FeeCategory,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    fee_category.created_at = datetime.now()
    fee_category.updated_at = datetime.now()
    session.add(fee_category)
    session.commit()
    session.refresh(fee_category)
    return fee_category


@app.get("/fee-category")
def get_fee_categories(session: Session = Depends(get_session)):
    return session.exec(select(FeeCategory)).all()


@app.get("/fee-category/{fee_category_id}")
def get_fee_category_by_id(fee_category_id: int, session: Session = Depends(get_session)):
    fee_category = session.get(FeeCategory, fee_category_id)
    if not fee_category:
        raise HTTPException(status_code=404, detail="Fee category not found")
    return fee_category


@app.put("/fee-category/{fee_category_id}")
def update_fee_category_by_id(fee_category_id: int, data: FeeCategory, session: Session = Depends(get_session)):
    fee_category = session.get(FeeCategory, fee_category_id)
    if not fee_category:
        raise HTTPException(status_code=404, detail="Fee category not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(fee_category, key, value)
    fee_category.updated_at = datetime.now()

    session.commit()
    session.refresh(fee_category)
    return fee_category


@app.delete("/fee-category/{fee_category_id}", status_code=204)
def delete_fee_category_by_id(fee_category_id: int, session: Session = Depends(get_session)):
    fee_category = session.get(FeeCategory, fee_category_id)
    if not fee_category:
        raise HTTPException(status_code=404, detail="Fee category not found")
    session.delete(fee_category)
    session.commit()
    return {"details": f"fee category {fee_category_id} deleted"}


# --------------------------------------------------------------------------
# FeeStructure
# --------------------------------------------------------------------------
@app.post("/fee-structure")
def create_fee_structure(
    fee_structure: FeeStructure,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    category = session.get(FeeCategory, fee_structure.feeCategory_id)
    if not category:
        raise HTTPException(status_code=404, detail="Fee category not found")

    fee_structure.created_at = datetime.now()
    fee_structure.updated_at = datetime.now()
    session.add(fee_structure)
    session.commit()
    session.refresh(fee_structure)
    return fee_structure


@app.get("/fee-structure")
def get_fee_structures(session: Session = Depends(get_session)):
    return session.exec(select(FeeStructure)).all()


@app.get("/fee-structure/{fee_structure_id}")
def get_fee_structure_by_id(fee_structure_id: int, session: Session = Depends(get_session)):
    fee_structure = session.get(FeeStructure, fee_structure_id)
    if not fee_structure:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    return fee_structure


@app.put("/fee-structure/{fee_structure_id}")
def update_fee_structure_by_id(fee_structure_id: int, data: FeeStructure, session: Session = Depends(get_session)):
    fee_structure = session.get(FeeStructure, fee_structure_id)
    if not fee_structure:
        raise HTTPException(status_code=404, detail="Fee structure not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(fee_structure, key, value)
    fee_structure.updated_at = datetime.now()

    session.commit()
    session.refresh(fee_structure)
    return fee_structure


@app.delete("/fee-structure/{fee_structure_id}", status_code=204)
def delete_fee_structure_by_id(fee_structure_id: int, session: Session = Depends(get_session)):
    fee_structure = session.get(FeeStructure, fee_structure_id)
    if not fee_structure:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    session.delete(fee_structure)
    session.commit()
    return {"details": f"fee structure {fee_structure_id} deleted"}


# --------------------------------------------------------------------------
# Student_fee
# --------------------------------------------------------------------------
@app.post("/student-fee")
def create_student_fee(
    student_fee: Student_fee,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    fee_structure = session.get(FeeStructure, student_fee.feestructure_id)
    if not fee_structure:
        raise HTTPException(status_code=404, detail="Fee structure not found")

    # Default total/balance from the fee structure amount when not supplied.
    if student_fee.total_amount is None:
        student_fee.total_amount = fee_structure.amount
    student_fee.discount_amount = student_fee.discount_amount or 0
    student_fee.paid_amount = student_fee.paid_amount or 0
    student_fee.balance_amount = (
        (student_fee.total_amount or 0)
        - student_fee.discount_amount
        - student_fee.paid_amount
    )
    student_fee.status = "paid" if student_fee.balance_amount <= 0 else "pending"

    student_fee.created_at = datetime.now()
    student_fee.updated_at = datetime.now()
    session.add(student_fee)
    session.commit()
    session.refresh(student_fee)
    return student_fee


@app.get("/student-fee")
def get_student_fees(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    student_fees = session.exec(select(Student_fee)).all()
    return {"user": payload, "student_fees": student_fees}


@app.get("/student-fee/{student_fee_id}")
def get_student_fee_by_id(student_fee_id: int, session: Session = Depends(get_session)):
    student_fee = session.get(Student_fee, student_fee_id)
    if not student_fee:
        raise HTTPException(status_code=404, detail="Student fee not found")
    return student_fee


@app.put("/student-fee/{student_fee_id}")
def update_student_fee_by_id(student_fee_id: int, data: Student_fee, session: Session = Depends(get_session)):
    student_fee = session.get(Student_fee, student_fee_id)
    if not student_fee:
        raise HTTPException(status_code=404, detail="Student fee not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(student_fee, key, value)
    student_fee.updated_at = datetime.now()

    session.commit()
    session.refresh(student_fee)
    return student_fee


@app.delete("/student-fee/{student_fee_id}", status_code=204)
def delete_student_fee_by_id(student_fee_id: int, session: Session = Depends(get_session)):
    student_fee = session.get(Student_fee, student_fee_id)
    if not student_fee:
        raise HTTPException(status_code=404, detail="Student fee not found")
    session.delete(student_fee)
    session.commit()
    return {"details": f"student fee {student_fee_id} deleted"}


# --------------------------------------------------------------------------
# Payment
# --------------------------------------------------------------------------
@app.post("/payment")
def create_payment(
    payment: Payment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    student_fee = session.get(Student_fee, payment.student_fee_id)
    if not student_fee:
        raise HTTPException(status_code=404, detail="Student fee not found")

    if payment.amount is None or payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Payment amount must be greater than zero")

    payment.status = payment.status or "success"
    payment.created_at = datetime.now()
    payment.updated_at = datetime.now()

    session.add(payment)
    try:
        session.commit()
        session.refresh(payment)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to record payment with these details")

    # Roll the payment into the linked student fee's balance.
    student_fee.paid_amount = (student_fee.paid_amount or 0) + payment.amount
    student_fee.balance_amount = (
        (student_fee.total_amount or 0)
        - (student_fee.discount_amount or 0)
        - student_fee.paid_amount
    )
    student_fee.status = (
        "paid" if student_fee.balance_amount <= 0
        else "partial" if student_fee.paid_amount > 0
        else "pending"
    )
    student_fee.updated_at = datetime.now()
    session.add(student_fee)
    session.commit()

    # Auto-generate a receipt for every successful payment.
    if payment.status == "success":
        receipt = Receipt(
            Payment_id=payment.id,
            number=f"RCPT-{uuid.uuid4().hex[:10].upper()}",
            reated_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(receipt)
        session.commit()

    return payment


@app.get("/payment")
def get_payments(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    payments = session.exec(select(Payment)).all()
    return {"user": payload, "payments": payments}


@app.get("/payment/{payment_id}")
def get_payment_by_id(payment_id: int, session: Session = Depends(get_session)):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@app.put("/payment/{payment_id}")
def update_payment_by_id(payment_id: int, data: Payment, session: Session = Depends(get_session)):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(payment, key, value)
    payment.updated_at = datetime.now()

    session.commit()
    session.refresh(payment)
    return payment


@app.delete("/payment/{payment_id}", status_code=204)
def delete_payment_by_id(payment_id: int, session: Session = Depends(get_session)):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    session.delete(payment)
    session.commit()
    return {"details": f"payment {payment_id} deleted"}


# --------------------------------------------------------------------------
# Scholarship
# --------------------------------------------------------------------------
@app.post("/scholarship")
def create_scholarship(
    scholarship: Scholarship,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    scholarship.created_at = datetime.now()
    scholarship.updated_at = datetime.now()
    session.add(scholarship)
    session.commit()
    session.refresh(scholarship)
    return scholarship


@app.get("/scholarship")
def get_scholarships(session: Session = Depends(get_session)):
    return session.exec(select(Scholarship)).all()


@app.get("/scholarship/{scholarship_id}")
def get_scholarship_by_id(scholarship_id: int, session: Session = Depends(get_session)):
    scholarship = session.get(Scholarship, scholarship_id)
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    return scholarship


@app.put("/scholarship/{scholarship_id}")
def update_scholarship_by_id(scholarship_id: int, data: Scholarship, session: Session = Depends(get_session)):
    scholarship = session.get(Scholarship, scholarship_id)
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(scholarship, key, value)
    scholarship.updated_at = datetime.now()

    session.commit()
    session.refresh(scholarship)
    return scholarship


@app.delete("/scholarship/{scholarship_id}", status_code=204)
def delete_scholarship_by_id(scholarship_id: int, session: Session = Depends(get_session)):
    scholarship = session.get(Scholarship, scholarship_id)
    if not scholarship:
        raise HTTPException(status_code=404, detail="Scholarship not found")
    session.delete(scholarship)
    session.commit()
    return {"details": f"scholarship {scholarship_id} deleted"}


# --------------------------------------------------------------------------
# Fine
# --------------------------------------------------------------------------
@app.post("/fine")
def create_fine(
    fine: Fine,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    fine.created_at = datetime.now()
    fine.updated_at = datetime.now()
    session.add(fine)
    session.commit()
    session.refresh(fine)
    return fine


@app.get("/fine")
def get_fines(session: Session = Depends(get_session)):
    return session.exec(select(Fine)).all()


@app.get("/fine/{fine_id}")
def get_fine_by_id(fine_id: int, session: Session = Depends(get_session)):
    fine = session.get(Fine, fine_id)
    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    return fine


@app.put("/fine/{fine_id}")
def update_fine_by_id(fine_id: int, data: Fine, session: Session = Depends(get_session)):
    fine = session.get(Fine, fine_id)
    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(fine, key, value)
    fine.updated_at = datetime.now()

    session.commit()
    session.refresh(fine)
    return fine


@app.delete("/fine/{fine_id}", status_code=204)
def delete_fine_by_id(fine_id: int, session: Session = Depends(get_session)):
    fine = session.get(Fine, fine_id)
    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    session.delete(fine)
    session.commit()
    return {"details": f"fine {fine_id} deleted"}


# --------------------------------------------------------------------------
# Receipt
# --------------------------------------------------------------------------
@app.get("/receipt")
def get_receipts(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    receipts = session.exec(select(Receipt)).all()
    return {"user": payload, "receipts": receipts}


@app.get("/receipt/{receipt_id}")
def get_receipt_by_id(receipt_id: int, session: Session = Depends(get_session)):
    receipt = session.get(Receipt, receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt


@app.delete("/receipt/{receipt_id}", status_code=204)
def delete_receipt_by_id(receipt_id: int, session: Session = Depends(get_session)):
    receipt = session.get(Receipt, receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    session.delete(receipt)
    session.commit()
    return {"details": f"receipt {receipt_id} deleted"}