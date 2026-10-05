from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, Session, select
from contextlib import asynccontextmanager
from datetime import datetime, date
from decimal import Decimal

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from common.auth_middleware import JWTMiddleware
from payroll_service.model import (
    SalaryHead,
    SalaryStructure,
    EmployeeSalary,
    Allowance,
    Deduction,
    Payslip,
    SalaryPayment,
    EmployeeLoan,
    LoanRecovery,
    BankLetter,
)
from database import get_session, create_db_and_tables
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()

# Same signing key/algorithm as the users service, since tokens are issued
# there and only verified here.
SECRET_KEY = os.getenv("SECRET_KEY", "priyanshu")
ALGORITHM = "HS256"


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(JWTMiddleware)

ZERO = Decimal("0")
PROTECTED_FIELDS = {"id", "created_at"}

@app.on_event("startup")
def startup():
    create_db_and_tables()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return payload


def commit_or_409(session: Session, message: str):
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail=message)


def head_amount(row, basic: Decimal) -> Decimal:
    """Amount of an allowance/deduction row, or its percentage of the basic salary."""
    if row.amount is not None:
        return row.amount
    if row.percentage is not None:
        return (basic * row.percentage / Decimal(100)).quantize(Decimal("0.01"))
    return ZERO


def calculate_heads(session: Session, employeesalary_id: int, basic: Decimal):
    """Returns (total_allowance, total_deduction) of one employee salary."""
    allowances = session.exec(
        select(Allowance).where(Allowance.employeesalary_id == employeesalary_id)
    ).all()
    deductions = session.exec(
        select(Deduction).where(Deduction.employeesalary_id == employeesalary_id)
    ).all()
    total_allowance = sum((head_amount(a, basic) for a in allowances), ZERO)
    total_deduction = sum((head_amount(d, basic) for d in deductions), ZERO)
    return total_allowance, total_deduction


def refresh_employee_salary_totals(session: Session, employee_salary: EmployeeSalary):
    """Keeps gross/total deduction/net of an employee salary in sync with its heads."""
    session.flush()
    basic = employee_salary.basic_salary or ZERO
    total_allowance, total_deduction = calculate_heads(session, employee_salary.id, basic)
    employee_salary.gross_salary = basic + total_allowance
    employee_salary.total_deduction = total_deduction
    employee_salary.net_salary = employee_salary.gross_salary - total_deduction
    employee_salary.updated_at = datetime.now()
    session.add(employee_salary)


def refresh_payslip_status(session: Session, payslip: Payslip):
    """paid / partially_paid / generated, based on the payments made so far."""
    session.flush()
    paid_total = session.exec(
        select(func.coalesce(func.sum(SalaryPayment.amount), 0)).where(
            SalaryPayment.payslip_id == payslip.id
        )
    ).one()
    if paid_total >= (payslip.net_salary or ZERO) and paid_total > 0:
        payslip.status = "paid"
    elif paid_total > 0:
        payslip.status = "partially_paid"
    else:
        payslip.status = "generated"
    payslip.updated_at = datetime.now()
    session.add(payslip)


# --------------------------------------------------------------------------
# SalaryHead
# --------------------------------------------------------------------------
@app.post("/salary-head")
def create_salary_head(
    salary_head: SalaryHead,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if salary_head.code:
        exists = session.exec(
            select(SalaryHead).where(SalaryHead.code == salary_head.code)
        ).first()
        if exists:
            raise HTTPException(status_code=409, detail="Salary head code already exists")

    salary_head.created_at = datetime.now()
    salary_head.updated_at = datetime.now()
    session.add(salary_head)
    session.commit()
    session.refresh(salary_head)
    return salary_head


@app.get("/salary-head")
def get_salary_heads(session: Session = Depends(get_session)):
    return session.exec(select(SalaryHead)).all()


@app.get("/salary-head/{salary_head_id}")
def get_salary_head_by_id(salary_head_id: int, session: Session = Depends(get_session)):
    salary_head = session.get(SalaryHead, salary_head_id)
    if not salary_head:
        raise HTTPException(status_code=404, detail="Salary head not found")
    return salary_head


@app.put("/salary-head/{salary_head_id}")
def update_salary_head_by_id(
    salary_head_id: int,
    data: SalaryHead,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    salary_head = session.get(SalaryHead, salary_head_id)
    if not salary_head:
        raise HTTPException(status_code=404, detail="Salary head not found")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(salary_head, key, value)
    salary_head.updated_at = datetime.now()

    session.add(salary_head)
    session.commit()
    session.refresh(salary_head)
    return salary_head


@app.delete("/salary-head/{salary_head_id}", status_code=204)
def delete_salary_head_by_id(
    salary_head_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    salary_head = session.get(SalaryHead, salary_head_id)
    if not salary_head:
        raise HTTPException(status_code=404, detail="Salary head not found")
    session.delete(salary_head)
    commit_or_409(session, "Salary head is used in allowances or deductions")


# --------------------------------------------------------------------------
# SalaryStructure
# --------------------------------------------------------------------------
@app.post("/salary-structure")
def create_salary_structure(
    salary_structure: SalaryStructure,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if (
        salary_structure.effective_from
        and salary_structure.effective_to
        and salary_structure.effective_from > salary_structure.effective_to
    ):
        raise HTTPException(status_code=400, detail="effective_from must be before effective_to")

    salary_structure.created_at = datetime.now()
    salary_structure.updated_at = datetime.now()
    session.add(salary_structure)
    session.commit()
    session.refresh(salary_structure)
    return salary_structure


@app.get("/salary-structure")
def get_salary_structures(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    return session.exec(select(SalaryStructure)).all()


@app.get("/salary-structure/{salary_structure_id}")
def get_salary_structure_by_id(
    salary_structure_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    salary_structure = session.get(SalaryStructure, salary_structure_id)
    if not salary_structure:
        raise HTTPException(status_code=404, detail="Salary structure not found")
    return salary_structure


@app.put("/salary-structure/{salary_structure_id}")
def update_salary_structure_by_id(
    salary_structure_id: int,
    data: SalaryStructure,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    salary_structure = session.get(SalaryStructure, salary_structure_id)
    if not salary_structure:
        raise HTTPException(status_code=404, detail="Salary structure not found")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(salary_structure, key, value)
    salary_structure.updated_at = datetime.now()

    session.add(salary_structure)
    session.commit()
    session.refresh(salary_structure)
    return salary_structure


@app.delete("/salary-structure/{salary_structure_id}", status_code=204)
def delete_salary_structure_by_id(
    salary_structure_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    salary_structure = session.get(SalaryStructure, salary_structure_id)
    if not salary_structure:
        raise HTTPException(status_code=404, detail="Salary structure not found")
    session.delete(salary_structure)
    commit_or_409(session, "Salary structure is used by employee salaries")


# --------------------------------------------------------------------------
# EmployeeSalary
# --------------------------------------------------------------------------
@app.post("/employee-salary")
def create_employee_salary(
    employee_salary: EmployeeSalary,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if employee_salary.staff_id is None:
        raise HTTPException(status_code=400, detail="staff_id is required")

    salary_structure = session.get(SalaryStructure, employee_salary.salarystructure_id)
    if not salary_structure:
        raise HTTPException(status_code=404, detail="Salary structure not found")
    if salary_structure.status is False:
        raise HTTPException(status_code=400, detail="Salary structure is not active")

    active = session.exec(
        select(EmployeeSalary).where(
            EmployeeSalary.staff_id == employee_salary.staff_id,
            EmployeeSalary.status == True,  # noqa: E712
        )
    ).first()
    if active:
        raise HTTPException(
            status_code=409, detail="This staff member already has an active salary"
        )

    # Basic salary comes from the structure unless it is given explicitly.
    employee_salary.basic_salary = employee_salary.basic_salary or salary_structure.basic_salary
    basic = employee_salary.basic_salary or ZERO
    employee_salary.gross_salary = basic
    employee_salary.total_deduction = ZERO
    employee_salary.net_salary = basic
    employee_salary.effective_from = employee_salary.effective_from or date.today()
    employee_salary.created_at = datetime.now()
    employee_salary.updated_at = datetime.now()

    session.add(employee_salary)
    commit_or_409(session, "Unable to create employee salary with these details")
    session.refresh(employee_salary)
    return employee_salary


@app.get("/employee-salary")
def get_employee_salaries(
    staff_id: int | None = None,
    status: bool | None = None,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    query = select(EmployeeSalary)
    if staff_id is not None:
        query = query.where(EmployeeSalary.staff_id == staff_id)
    if status is not None:
        query = query.where(EmployeeSalary.status == status)
    return session.exec(query).all()


@app.get("/employee-salary/{employee_salary_id}")
def get_employee_salary_by_id(
    employee_salary_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    employee_salary = session.get(EmployeeSalary, employee_salary_id)
    if not employee_salary:
        raise HTTPException(status_code=404, detail="Employee salary not found")
    return employee_salary


@app.put("/employee-salary/{employee_salary_id}")
def update_employee_salary_by_id(
    employee_salary_id: int,
    data: EmployeeSalary,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    employee_salary = session.get(EmployeeSalary, employee_salary_id)
    if not employee_salary:
        raise HTTPException(status_code=404, detail="Employee salary not found")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(employee_salary, key, value)
    refresh_employee_salary_totals(session, employee_salary)

    commit_or_409(session, "Unable to update employee salary with these details")
    session.refresh(employee_salary)
    return employee_salary


@app.post("/employee-salary/{employee_salary_id}/recalculate")
def recalculate_employee_salary(
    employee_salary_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    """Recomputes gross, total deduction and net from the allowances and deductions."""
    employee_salary = session.get(EmployeeSalary, employee_salary_id)
    if not employee_salary:
        raise HTTPException(status_code=404, detail="Employee salary not found")

    refresh_employee_salary_totals(session, employee_salary)
    session.commit()
    session.refresh(employee_salary)
    return employee_salary


@app.delete("/employee-salary/{employee_salary_id}", status_code=204)
def delete_employee_salary_by_id(
    employee_salary_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    employee_salary = session.get(EmployeeSalary, employee_salary_id)
    if not employee_salary:
        raise HTTPException(status_code=404, detail="Employee salary not found")
    session.delete(employee_salary)
    commit_or_409(
        session, "Employee salary has allowances, deductions or payslips, set status to false instead"
    )


# --------------------------------------------------------------------------
# Allowance
# --------------------------------------------------------------------------
@app.post("/allowance")
def create_allowance(
    allowance: Allowance,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    employee_salary = session.get(EmployeeSalary, allowance.employeesalary_id)
    if not employee_salary:
        raise HTTPException(status_code=404, detail="Employee salary not found")
    salary_head = session.get(SalaryHead, allowance.salaryhead_id)
    if not salary_head:
        raise HTTPException(status_code=404, detail="Salary head not found")
    if allowance.amount is None and allowance.percentage is None:
        raise HTTPException(status_code=400, detail="amount or percentage is required")

    allowance.created_at = datetime.now()
    allowance.updated_at = datetime.now()
    session.add(allowance)
    refresh_employee_salary_totals(session, employee_salary)

    commit_or_409(session, "Unable to create allowance with these details")
    session.refresh(allowance)
    return allowance


@app.get("/allowance")
def get_allowances(
    employeesalary_id: int | None = None,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    query = select(Allowance)
    if employeesalary_id is not None:
        query = query.where(Allowance.employeesalary_id == employeesalary_id)
    return session.exec(query).all()


@app.get("/allowance/{allowance_id}")
def get_allowance_by_id(
    allowance_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    allowance = session.get(Allowance, allowance_id)
    if not allowance:
        raise HTTPException(status_code=404, detail="Allowance not found")
    return allowance


@app.put("/allowance/{allowance_id}")
def update_allowance_by_id(
    allowance_id: int,
    data: Allowance,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    allowance = session.get(Allowance, allowance_id)
    if not allowance:
        raise HTTPException(status_code=404, detail="Allowance not found")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(allowance, key, value)
    allowance.updated_at = datetime.now()
    session.add(allowance)

    employee_salary = session.get(EmployeeSalary, allowance.employeesalary_id)
    if employee_salary:
        refresh_employee_salary_totals(session, employee_salary)

    commit_or_409(session, "Unable to update allowance with these details")
    session.refresh(allowance)
    return allowance


@app.delete("/allowance/{allowance_id}", status_code=204)
def delete_allowance_by_id(
    allowance_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    allowance = session.get(Allowance, allowance_id)
    if not allowance:
        raise HTTPException(status_code=404, detail="Allowance not found")
    employee_salary = session.get(EmployeeSalary, allowance.employeesalary_id)
    session.delete(allowance)
    if employee_salary:
        refresh_employee_salary_totals(session, employee_salary)
    session.commit()


# --------------------------------------------------------------------------
# Deduction
# --------------------------------------------------------------------------
@app.post("/deduction")
def create_deduction(
    deduction: Deduction,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    employee_salary = session.get(EmployeeSalary, deduction.employeesalary_id)
    if not employee_salary:
        raise HTTPException(status_code=404, detail="Employee salary not found")
    salary_head = session.get(SalaryHead, deduction.salaryhead_id)
    if not salary_head:
        raise HTTPException(status_code=404, detail="Salary head not found")
    if deduction.amount is None and deduction.percentage is None:
        raise HTTPException(status_code=400, detail="amount or percentage is required")

    deduction.created_at = datetime.now()
    deduction.updated_at = datetime.now()
    session.add(deduction)
    refresh_employee_salary_totals(session, employee_salary)

    commit_or_409(session, "Unable to create deduction with these details")
    session.refresh(deduction)
    return deduction


@app.get("/deduction")
def get_deductions(
    employeesalary_id: int | None = None,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    query = select(Deduction)
    if employeesalary_id is not None:
        query = query.where(Deduction.employeesalary_id == employeesalary_id)
    return session.exec(query).all()


@app.get("/deduction/{deduction_id}")
def get_deduction_by_id(
    deduction_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    deduction = session.get(Deduction, deduction_id)
    if not deduction:
        raise HTTPException(status_code=404, detail="Deduction not found")
    return deduction


@app.put("/deduction/{deduction_id}")
def update_deduction_by_id(
    deduction_id: int,
    data: Deduction,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    deduction = session.get(Deduction, deduction_id)
    if not deduction:
        raise HTTPException(status_code=404, detail="Deduction not found")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(deduction, key, value)
    deduction.updated_at = datetime.now()
    session.add(deduction)

    employee_salary = session.get(EmployeeSalary, deduction.employeesalary_id)
    if employee_salary:
        refresh_employee_salary_totals(session, employee_salary)

    commit_or_409(session, "Unable to update deduction with these details")
    session.refresh(deduction)
    return deduction


@app.delete("/deduction/{deduction_id}", status_code=204)
def delete_deduction_by_id(
    deduction_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    deduction = session.get(Deduction, deduction_id)
    if not deduction:
        raise HTTPException(status_code=404, detail="Deduction not found")
    employee_salary = session.get(EmployeeSalary, deduction.employeesalary_id)
    session.delete(deduction)
    if employee_salary:
        refresh_employee_salary_totals(session, employee_salary)
    session.commit()


# --------------------------------------------------------------------------
# Payslip
# --------------------------------------------------------------------------
class PayslipGenerate(SQLModel):
    employeesalary_id: int
    month: int
    year: int
    remarks: str | None = None


@app.post("/payslip/generate")
def generate_payslip(
    data: PayslipGenerate,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    """Basic + allowances - deductions - one installment of every running loan."""
    if not 1 <= data.month <= 12:
        raise HTTPException(status_code=400, detail="month must be between 1 and 12")

    employee_salary = session.get(EmployeeSalary, data.employeesalary_id)
    if not employee_salary:
        raise HTTPException(status_code=404, detail="Employee salary not found")
    if employee_salary.status is False:
        raise HTTPException(status_code=400, detail="Employee salary is not active")

    exists = session.exec(
        select(Payslip).where(
            Payslip.employeesalary_id == data.employeesalary_id,
            Payslip.month == data.month,
            Payslip.year == data.year,
        )
    ).first()
    if exists:
        raise HTTPException(status_code=409, detail="Payslip is already generated for this month")

    basic = employee_salary.basic_salary or ZERO
    total_allowance, total_deduction = calculate_heads(session, employee_salary.id, basic)

    loans = []
    if employee_salary.staff_id is not None:
        loans = session.exec(
            select(EmployeeLoan).where(
                EmployeeLoan.staff_id == employee_salary.staff_id,
                EmployeeLoan.status == "active",
                EmployeeLoan.remaining_installment > 0,
            )
        ).all()
    for loan in loans:
        total_deduction += loan.installment_amount or ZERO

    gross = basic + total_allowance
    net = gross - total_deduction
    if net < 0:
        raise HTTPException(status_code=400, detail="Deductions are more than the gross salary")

    payslip = Payslip(
        employeesalary_id=employee_salary.id,
        month=data.month,
        year=data.year,
        basic_salary=basic,
        total_allowance=total_allowance,
        gross_salary=gross,
        total_deduction=total_deduction,
        net_salary=net,
        status="generated",
        remarks=data.remarks,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(payslip)
    session.flush()  # payslip.id is needed for the loan recovery rows

    for loan in loans:
        done = (loan.total_installment or 0) - (loan.remaining_installment or 0)
        session.add(
            LoanRecovery(
                employeeloan_id=loan.id,
                payslip_id=payslip.id,
                installment_no=done + 1,
                recovery_date=date.today(),
                amount=loan.installment_amount or ZERO,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )
        loan.remaining_installment = (loan.remaining_installment or 0) - 1
        if loan.remaining_installment <= 0:
            loan.status = "closed"
        loan.updated_at = datetime.now()
        session.add(loan)

    commit_or_409(session, "Unable to generate payslip")
    session.refresh(payslip)
    return payslip


@app.get("/payslip")
def get_payslips(
    employeesalary_id: int | None = None,
    month: int | None = None,
    year: int | None = None,
    status: str | None = None,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    query = select(Payslip)
    if employeesalary_id is not None:
        query = query.where(Payslip.employeesalary_id == employeesalary_id)
    if month is not None:
        query = query.where(Payslip.month == month)
    if year is not None:
        query = query.where(Payslip.year == year)
    if status:
        query = query.where(Payslip.status == status)
    return session.exec(query).all()


@app.get("/payslip/{payslip_id}")
def get_payslip_by_id(
    payslip_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    payslip = session.get(Payslip, payslip_id)
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")
    return payslip


@app.get("/payslip/staff/{staff_id}")
def get_payslips_by_staff(
    staff_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    return session.exec(
        select(Payslip)
        .join(EmployeeSalary, EmployeeSalary.id == Payslip.employeesalary_id)
        .where(EmployeeSalary.staff_id == staff_id)
        .order_by(Payslip.year.desc(), Payslip.month.desc())
    ).all()


@app.put("/payslip/{payslip_id}")
def update_payslip_by_id(
    payslip_id: int,
    data: Payslip,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    payslip = session.get(Payslip, payslip_id)
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(payslip, key, value)
    payslip.updated_at = datetime.now()

    session.add(payslip)
    session.commit()
    session.refresh(payslip)
    return payslip


@app.delete("/payslip/{payslip_id}", status_code=204)
def delete_payslip_by_id(
    payslip_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    payslip = session.get(Payslip, payslip_id)
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")
    session.delete(payslip)
    commit_or_409(session, "Payslip has salary payments or loan recoveries")


# --------------------------------------------------------------------------
# SalaryPayment
# --------------------------------------------------------------------------
@app.post("/salary-payment")
def create_salary_payment(
    salary_payment: SalaryPayment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    payslip = session.get(Payslip, salary_payment.payslip_id)
    if not payslip:
        raise HTTPException(status_code=404, detail="Payslip not found")
    if payslip.status == "paid":
        raise HTTPException(status_code=409, detail="This payslip is already paid")
    if salary_payment.amount is None or salary_payment.amount <= 0:
        raise HTTPException(status_code=400, detail="amount must be greater than 0")

    salary_payment.payment_date = salary_payment.payment_date or date.today()
    salary_payment.created_at = datetime.now()
    salary_payment.updated_at = datetime.now()
    session.add(salary_payment)
    refresh_payslip_status(session, payslip)

    commit_or_409(session, "Unable to create salary payment with these details")
    session.refresh(salary_payment)
    return salary_payment


@app.get("/salary-payment")
def get_salary_payments(
    payslip_id: int | None = None,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    query = select(SalaryPayment)
    if payslip_id is not None:
        query = query.where(SalaryPayment.payslip_id == payslip_id)
    return session.exec(query).all()


@app.get("/salary-payment/{salary_payment_id}")
def get_salary_payment_by_id(
    salary_payment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    salary_payment = session.get(SalaryPayment, salary_payment_id)
    if not salary_payment:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    return salary_payment


@app.put("/salary-payment/{salary_payment_id}")
def update_salary_payment_by_id(
    salary_payment_id: int,
    data: SalaryPayment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    salary_payment = session.get(SalaryPayment, salary_payment_id)
    if not salary_payment:
        raise HTTPException(status_code=404, detail="Salary payment not found")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(salary_payment, key, value)
    salary_payment.updated_at = datetime.now()
    session.add(salary_payment)

    payslip = session.get(Payslip, salary_payment.payslip_id)
    if payslip:
        refresh_payslip_status(session, payslip)

    commit_or_409(session, "Unable to update salary payment with these details")
    session.refresh(salary_payment)
    return salary_payment


@app.delete("/salary-payment/{salary_payment_id}", status_code=204)
def delete_salary_payment_by_id(
    salary_payment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    salary_payment = session.get(SalaryPayment, salary_payment_id)
    if not salary_payment:
        raise HTTPException(status_code=404, detail="Salary payment not found")
    payslip = session.get(Payslip, salary_payment.payslip_id)
    session.delete(salary_payment)
    if payslip:
        refresh_payslip_status(session, payslip)
    session.commit()


# --------------------------------------------------------------------------
# EmployeeLoan
# --------------------------------------------------------------------------
@app.post("/employee-loan")
def create_employee_loan(
    employee_loan: EmployeeLoan,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if employee_loan.staff_id is None:
        raise HTTPException(status_code=400, detail="staff_id is required")
    if not employee_loan.installment_amount or employee_loan.installment_amount <= 0:
        raise HTTPException(status_code=400, detail="installment_amount must be greater than 0")
    if not employee_loan.total_installment or employee_loan.total_installment <= 0:
        raise HTTPException(status_code=400, detail="total_installment must be greater than 0")

    employee_loan.remaining_installment = (
        employee_loan.remaining_installment
        if employee_loan.remaining_installment is not None
        else employee_loan.total_installment
    )
    employee_loan.start_date = employee_loan.start_date or date.today()
    employee_loan.status = employee_loan.status or "active"
    employee_loan.created_at = datetime.now()
    employee_loan.updated_at = datetime.now()

    session.add(employee_loan)
    session.commit()
    session.refresh(employee_loan)
    return employee_loan


@app.get("/employee-loan")
def get_employee_loans(
    staff_id: int | None = None,
    status: str | None = None,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    query = select(EmployeeLoan)
    if staff_id is not None:
        query = query.where(EmployeeLoan.staff_id == staff_id)
    if status:
        query = query.where(EmployeeLoan.status == status)
    return session.exec(query).all()


@app.get("/employee-loan/{employee_loan_id}")
def get_employee_loan_by_id(
    employee_loan_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    employee_loan = session.get(EmployeeLoan, employee_loan_id)
    if not employee_loan:
        raise HTTPException(status_code=404, detail="Employee loan not found")
    return employee_loan


@app.put("/employee-loan/{employee_loan_id}")
def update_employee_loan_by_id(
    employee_loan_id: int,
    data: EmployeeLoan,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    employee_loan = session.get(EmployeeLoan, employee_loan_id)
    if not employee_loan:
        raise HTTPException(status_code=404, detail="Employee loan not found")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(employee_loan, key, value)
    employee_loan.updated_at = datetime.now()

    session.add(employee_loan)
    session.commit()
    session.refresh(employee_loan)
    return employee_loan


@app.delete("/employee-loan/{employee_loan_id}", status_code=204)
def delete_employee_loan_by_id(
    employee_loan_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    employee_loan = session.get(EmployeeLoan, employee_loan_id)
    if not employee_loan:
        raise HTTPException(status_code=404, detail="Employee loan not found")
    session.delete(employee_loan)
    commit_or_409(session, "Employee loan has recoveries, set status to closed instead")


# --------------------------------------------------------------------------
# LoanRecovery (rows are created by /payslip/generate)
# --------------------------------------------------------------------------
@app.get("/loan-recovery")
def get_loan_recoveries(
    employeeloan_id: int | None = None,
    payslip_id: int | None = None,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    query = select(LoanRecovery)
    if employeeloan_id is not None:
        query = query.where(LoanRecovery.employeeloan_id == employeeloan_id)
    if payslip_id is not None:
        query = query.where(LoanRecovery.payslip_id == payslip_id)
    return session.exec(query).all()


@app.get("/loan-recovery/{loan_recovery_id}")
def get_loan_recovery_by_id(
    loan_recovery_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    loan_recovery = session.get(LoanRecovery, loan_recovery_id)
    if not loan_recovery:
        raise HTTPException(status_code=404, detail="Loan recovery not found")
    return loan_recovery


# --------------------------------------------------------------------------
# BankLetter
# --------------------------------------------------------------------------
@app.post("/bank-letter")
def create_bank_letter(
    bank_letter: BankLetter,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    if bank_letter.month is not None and not 1 <= bank_letter.month <= 12:
        raise HTTPException(status_code=400, detail="month must be between 1 and 12")

    bank_letter.generated_by = bank_letter.generated_by or payload.get("id")
    bank_letter.created_at = datetime.now()
    bank_letter.updated_at = datetime.now()
    session.add(bank_letter)
    session.commit()
    session.refresh(bank_letter)
    return bank_letter


@app.get("/bank-letter")
def get_bank_letters(
    month: int | None = None,
    year: int | None = None,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    query = select(BankLetter)
    if month is not None:
        query = query.where(BankLetter.month == month)
    if year is not None:
        query = query.where(BankLetter.year == year)
    return session.exec(query).all()


@app.get("/bank-letter/{bank_letter_id}")
def get_bank_letter_by_id(
    bank_letter_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    bank_letter = session.get(BankLetter, bank_letter_id)
    if not bank_letter:
        raise HTTPException(status_code=404, detail="Bank letter not found")
    return bank_letter


@app.put("/bank-letter/{bank_letter_id}")
def update_bank_letter_by_id(
    bank_letter_id: int,
    data: BankLetter,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    bank_letter = session.get(BankLetter, bank_letter_id)
    if not bank_letter:
        raise HTTPException(status_code=404, detail="Bank letter not found")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(bank_letter, key, value)
    bank_letter.updated_at = datetime.now()

    session.add(bank_letter)
    session.commit()
    session.refresh(bank_letter)
    return bank_letter


@app.delete("/bank-letter/{bank_letter_id}", status_code=204)
def delete_bank_letter_by_id(
    bank_letter_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    bank_letter = session.get(BankLetter, bank_letter_id)
    if not bank_letter:
        raise HTTPException(status_code=404, detail="Bank letter not found")
    session.delete(bank_letter)
    session.commit()