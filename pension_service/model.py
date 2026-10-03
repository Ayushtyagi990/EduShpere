from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from datetime import datetime, date


# ============================================================
# PENSION
# ============================================================

class Pension(SQLModel, table=True):
    __tablename__ = "pension"

    id: int | None = Field(primary_key=True)

    employee_id: int
    pension_number: str | None = Field(default=None, index=True)
    pension_type: str | None = Field(default=None)

    scheme_id: int | None = Field(default=None)

    joining_date: date | None = Field(default=None)
    retirement_date: date | None = Field(default=None)

    last_basic_salary: float | None = Field(default=None)
    pensionable_salary: float | None = Field(default=None)
    pension_amount: float | None = Field(default=None)

    bank_account: str | None = Field(default=None)
    bank_name: str | None = Field(default=None)
    ifsc_code: str | None = Field(default=None)

    status: str | None = Field(default="ACTIVE")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION SCHEME
# ============================================================

class PensionScheme(SQLModel, table=True):
    __tablename__ = "pension_scheme"

    id: int | None = Field(primary_key=True)

    name: str
    code: str | None = Field(default=None, index=True)
    description: str | None = Field(default=None)

    employee_contribution_percent: float | None = Field(default=None)
    employer_contribution_percent: float | None = Field(default=None)

    minimum_service_years: int | None = Field(default=None)
    retirement_age: int | None = Field(default=None)

    status: str | None = Field(default="ACTIVE")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION CONTRIBUTION
# ============================================================

class PensionContribution(SQLModel, table=True):
    __tablename__ = "pension_contribution"

    id: int | None = Field(primary_key=True)

    pension_id: int
    employee_id: int

    contribution_month: date | None = Field(default=None)

    employee_contribution: float | None = Field(default=None)
    employer_contribution: float | None = Field(default=None)
    total_contribution: float | None = Field(default=None)

    salary_basis: float | None = Field(default=None)

    status: str | None = Field(default="PENDING")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION CALCULATION
# ============================================================

class PensionCalculation(SQLModel, table=True):
    __tablename__ = "pension_calculation"

    id: int | None = Field(primary_key=True)

    pension_id: int
    employee_id: int

    total_service_years: float | None = Field(default=None)

    last_basic_salary: float | None = Field(default=None)
    average_salary: float | None = Field(default=None)

    calculation_factor: float | None = Field(default=None)

    gross_pension: float | None = Field(default=None)
    deduction_amount: float | None = Field(default=None)
    net_pension: float | None = Field(default=None)

    calculation_date: date | None = Field(default=None)

    status: str | None = Field(default="CALCULATED")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION REQUEST
# ============================================================

class PensionRequest(SQLModel, table=True):
    __tablename__ = "pension_request"

    id: int | None = Field(primary_key=True)

    employee_id: int
    pension_id: int | None = Field(default=None)

    request_type: str | None = Field(default=None)
    request_date: date | None = Field(default=None)

    reason: str | None = Field(default=None)
    description: str | None = Field(default=None)

    status: str | None = Field(default="PENDING")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION APPROVAL
# ============================================================

class PensionApproval(SQLModel, table=True):
    __tablename__ = "pension_approval"

    id: int | None = Field(primary_key=True)

    pension_request_id: int
    approver_user_id: int

    approval_level: int | None = Field(default=None)

    decision: str | None = Field(default=None)

    comments: str | None = Field(default=None)

    approval_date: datetime | None = Field(default=None)

    status: str | None = Field(default="PENDING")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION PAYMENT
# ============================================================

class PensionPayment(SQLModel, table=True):
    __tablename__ = "pension_payment"

    id: int | None = Field(primary_key=True)

    pension_id: int
    employee_id: int

    payment_month: date | None = Field(default=None)

    pension_amount: float | None = Field(default=None)
    deduction_amount: float | None = Field(default=None)
    net_amount: float | None = Field(default=None)

    payment_date: date | None = Field(default=None)

    transaction_reference: str | None = Field(default=None)

    payment_method: str | None = Field(default=None)

    status: str | None = Field(default="PENDING")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION ADJUSTMENT
# ============================================================

class PensionAdjustment(SQLModel, table=True):
    __tablename__ = "pension_adjustment"

    id: int | None = Field(primary_key=True)

    pension_id: int
    employee_id: int

    adjustment_type: str | None = Field(default=None)

    amount: float | None = Field(default=None)

    reason: str | None = Field(default=None)

    effective_date: date | None = Field(default=None)

    approved_by: int | None = Field(default=None)

    status: str | None = Field(default="PENDING")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION NOMINEE
# ============================================================

class PensionNominee(SQLModel, table=True):
    __tablename__ = "pension_nominee"

    id: int | None = Field(primary_key=True)

    pension_id: int
    employee_id: int

    name: str
    relation: str | None = Field(default=None)

    date_of_birth: date | None = Field(default=None)

    phone: str | None = Field(default=None)
    email: str | None = Field(default=None)

    address_id: int 

    share_percentage: float | None = Field(default=None)

    is_primary: bool = Field(default=False)

    status: str | None = Field(default="ACTIVE")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION BENEFICIARY
# ============================================================

class PensionBeneficiary(SQLModel, table=True):
    __tablename__ = "pension_beneficiary"

    id: int | None = Field(primary_key=True)

    pension_id: int
    employee_id: int

    name: str
    relation: str | None = Field(default=None)

    date_of_birth: date | None = Field(default=None)

    phone: str | None = Field(default=None)
    email: str | None = Field(default=None)

    address_id: int 

    percentage: float | None = Field(default=None)

    effective_from: date | None = Field(default=None)
    effective_to: date | None = Field(default=None)

    status: str | None = Field(default="ACTIVE")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION DOCUMENT
# ============================================================

class PensionDocument(SQLModel, table=True):
    __tablename__ = "pension_document"

    id: int | None = Field(primary_key=True)

    pension_id: int
    employee_id: int

    document_type: str | None = Field(default=None)
    document_number: str | None = Field(default=None)

    file_name: str | None = Field(default=None)
    file_url: str | None = Field(default=None)

    issue_date: date | None = Field(default=None)
    expiry_date: date | None = Field(default=None)

    status: str | None = Field(default="ACTIVE")

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


# ============================================================
# PENSION STATUS HISTORY
# ============================================================

class PensionStatusHistory(SQLModel, table=True):
    __tablename__ = "pension_status_history"

    id: int | None = Field(primary_key=True)

    pension_id: int
    employee_id: int

    old_status: str | None = Field(default=None)
    new_status: str | None = Field(default=None)

    reason: str | None = Field(default=None)

    changed_by: int | None = Field(default=None)

    changed_at: datetime | None = Field(default=None)

    metadata: dict | None = Field(
        default=None,
        sa_column=Column(JSON)
    )

    created_at: datetime | None = Field(default=None)