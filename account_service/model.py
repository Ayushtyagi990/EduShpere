from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date


class FeeCategory(SQLModel, table = True):
    """ storing fee category information """
    __tablename__ = "feecategory"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    description : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class FeeStructure(SQLModel, table = True):
    """ storing fee structure information """
    __tablename__ = "feestructure"
    id : int | None = Field(primary_key = True)
    feecategory_id : int | None = Field(foreign_key = "feecategory.id")
    feecategory : FeeCategory | None = Relationship()
    amount : float | None = Field(default = None)
    academic_year_id : int
    program_id : int
    due_date : date | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Student_fee(SQLModel, table = True):
    """ storing student fee information """
    __tablename__ = "student_fee"
    id : int | None = Field(primary_key = True)
    student_id : int
    feestructure_id : int | None = Field( foreign_key = "feestructure.id")
    feestructure : FeeStructure  = Relationship()
    total_amount : float | None = Field(default = None)
    discount_amount : float | None = Field(default = None)
    paid_amount : float | None = Field(default = None)
    balance_amount : float | None = Field(default = None)
    status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Payment(SQLModel, table = True):
    """ storing payment information """
    __tablename__ = "payment"
    id : int | None = Field( primary_key = True)
    student_fee_id : int | None = Field(foreign_key = "student_fee.id")
    student_fee : Student_fee  = Relationship()
    amount : float | None = Field(default = None)
    methods : str | None = Field(default = None)
    transaction_id : str | None = Field(default = None)
    status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Scholarship(SQLModel, table = True):
    """ storing scholarship information """
    __tablename__ = "scholarship"
    id : int | None = Field( primary_key = True)
    name : str | None = Field(default = None)
    description : str | None = Field(default = None)
    amount : float | None = Field(default = None)
    academic_year_id : int
    program_id : int
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Fine(SQLModel, table = True):
    """ storing fine information """
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
    """ storing receipt information """
    __tablename__ = "receipts"
    id : int | None = Field( primary_key = True)
    payment_id : int | None = Field(foreign_key = "payment.id")
    payment : Payment  = Relationship()
    number : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)