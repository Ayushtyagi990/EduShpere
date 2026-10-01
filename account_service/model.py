from  sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date




class FeeCategory(SQLModel, table=True):
    __tablename__ = "feecategory"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    fee_structures: List["FeeStructure"] = Relationship(
        back_populates="feecategory"
    )


class FeeStructure(SQLModel, table=True):
    __tablename__ = "feestructure"

    id: Optional[int] = Field(default=None, primary_key=True)

    feecategory_id: Optional[int] = Field(
        default=None,
        foreign_key="feecategory.id"
    )

    feecategory: Optional[FeeCategory] = Relationship(
        back_populates="fee_structures"
    )

    amount: Optional[float] = None
    academic_year_id: int
    program_id: int
    due_date: Optional[date] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



class Student_fee(SQLModel, table = True):
    __tablename__ = "student_fee"
    id : int | None = Field(primary_key = True)
    student_id : int
    feestructure_id : int | None = Field(foreign_key  = "feestructure.id")
    feestructure : FeeStructure =  Relationship()
    total_amount :  float | None = Field(default = None)
    discount_amount:  float | None = Field(default = None)
    paid_amount :  float | None = Field(default = None)
    balance_amount : float | None = Field(default = None)
    status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Payment(SQLModel, table = True):
    __tablename__ = "payment"
    id : int | None = Field(primary_key = True)
    student_fee_id : int | None = Field(foreign_key  = "student_fee.id")
    student_fee_id : Student_fee = Relationship()
    amount : float | None = Field(default = None)
    methods : str | None = Field(default = None)
    transaction_id : str | None = Field(default = None)
    status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class Scholarship(SQLModel, table = True):
    __tablename__ = "scholarship"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    description : str | None = Field(default = None)
    amount : float | None = Field(default = None)
    academic_year_id : int
    program_id : int
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class Fine(SQLModel, table = True):
    __tablename__ = "fine"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    description : str | None = Field(default = None)
    amount : float | None = Field(default = None)
    academic_year_id : int
    program_id : int
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Receipt(SQLModel, table = True):
    __tablename__ = "receipts"
    id : int | None = Field(primary_key = True)
    Payment_id : int | None = Field(foreign_key  = "payment.id")
    Payment  :  Payment = Relationship()
    number : str | None = Field(default = None)
    reated_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)



