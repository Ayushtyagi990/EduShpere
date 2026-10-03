from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from decimal import Decimal


class SalaryHead(SQLModel, table=True):
    __tablename__ = "salaryhead"

    id: int | None = Field(primary_key=True)
    name: str | None = Field(default=None)
    code: str | None = Field(default=None)
    type: str | None = Field(default=None)
    description: str | None = Field(default=None)
    is_taxable: bool | None = Field(default=True)
    status: bool | None = Field(default=True)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class SalaryStructure(SQLModel, table=True):
    __tablename__ = "salarystructure"

    id: int | None = Field(primary_key=True)
    name: str | None = Field(default=None)
    code: str | None = Field(default=None)
    basic_salary: Decimal | None = Field(default=None)
    effective_from: date | None = Field(default=None)
    effective_to: date | None = Field(default=None)
    status: bool | None = Field(default=True)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class EmployeeSalary(SQLModel, table=True):
    __tablename__ = "employeesalary"

    id: int | None = Field(primary_key=True)
    staff_id: int | None = Field(default=None)
    salarystructure_id: int = Field(foreign_key="salarystructure.id")
    salarystructure: SalaryStructure = Relationship()
    basic_salary: Decimal | None = Field(default=None)
    gross_salary: Decimal | None = Field(default=None)
    total_deduction: Decimal | None = Field(default=None)
    net_salary: Decimal | None = Field(default=None)
    effective_from: date | None = Field(default=None)
    status: bool | None = Field(default=True)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class Allowance(SQLModel, table=True):
    __tablename__ = "allowance"

    id: int | None = Field(primary_key=True)
    employeesalary_id: int = Field(foreign_key="employeesalary.id")
    employeesalary: EmployeeSalary = Relationship()
    salaryhead_id: int = Field(foreign_key="salaryhead.id")
    salaryhead: SalaryHead = Relationship()
    amount: Decimal | None = Field(default=None)
    percentage: Decimal | None = Field(default=None)
    remarks: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class Deduction(SQLModel, table=True):
    __tablename__ = "deduction"

    id: int | None = Field(primary_key=True)
    employeesalary_id: int = Field(foreign_key="employeesalary.id")
    employeesalary: EmployeeSalary = Relationship()
    salaryhead_id: int = Field(foreign_key="salaryhead.id")
    salaryhead: SalaryHead = Relationship()
    amount: Decimal | None = Field(default=None)
    percentage: Decimal | None = Field(default=None)
    remarks: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class Payslip(SQLModel, table=True):
    __tablename__ = "payslip"

    id: int | None = Field(primary_key=True)
    employeesalary_id: int = Field(foreign_key="employeesalary.id")
    employeesalary: EmployeeSalary = Relationship()
    month: int | None = Field(default=None)
    year: int | None = Field(default=None)
    basic_salary: Decimal | None = Field(default=None)
    total_allowance: Decimal | None = Field(default=None)
    gross_salary: Decimal | None = Field(default=None)
    total_deduction: Decimal | None = Field(default=None)
    net_salary: Decimal | None = Field(default=None)
    status: str | None = Field(default=None)
    remarks: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class SalaryPayment(SQLModel, table=True):
    __tablename__ = "salarypayment"

    id: int | None = Field(primary_key=True)
    payslip_id: int = Field(foreign_key="payslip.id")
    payslip: Payslip = Relationship()
    payment_date: date | None = Field(default=None)
    payment_mode: str | None = Field(default=None)
    transaction_no: str | None = Field(default=None)
    bank_name: str | None = Field(default=None)
    amount: Decimal | None = Field(default=None)
    remarks: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class EmployeeLoan(SQLModel, table=True):
    __tablename__ = "employeeloan"

    id: int | None = Field(primary_key=True)
    staff_id: int | None = Field(default=None)
    loan_type: str | None = Field(default=None)
    principal_amount: Decimal | None = Field(default=None)
    installment_amount: Decimal | None = Field(default=None)
    total_installment: int | None = Field(default=None)
    remaining_installment: int | None = Field(default=None)
    start_date: date | None = Field(default=None)
    end_date: date | None = Field(default=None)
    status: str | None = Field(default=None)
    remarks: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class LoanRecovery(SQLModel, table=True):
    __tablename__ = "loanrecovery"

    id: int | None = Field(primary_key=True)
    employeeloan_id: int = Field(foreign_key="employeeloan.id")
    employeeloan: EmployeeLoan = Relationship()
    payslip_id: int = Field(foreign_key="payslip.id")
    payslip: Payslip = Relationship()
    installment_no: int | None = Field(default=None)
    recovery_date: date | None = Field(default=None)
    amount: Decimal | None = Field(default=None)
    remarks: str | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class BankLetter(SQLModel, table=True):
    __tablename__ = "bankletter"

    id: int | None = Field(primary_key=True)
    month: int | None = Field(default=None)
    year: int | None = Field(default=None)
    bank_name: str | None = Field(default=None)
    total_employee: int | None = Field(default=None)
    total_amount: Decimal | None = Field(default=None)
    file_name: str | None = Field(default=None)
    file_path: str | None = Field(default=None)
    generated_by: int | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)