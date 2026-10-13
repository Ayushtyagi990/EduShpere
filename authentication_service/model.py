from  sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from datetime import datetime, date, timezone
from decimal import Decimal

class Address(SQLModel, table = True):
    """ storing address information """
    __tablename__ = "address"
    id : int | None =  Field(primary_key = True)
    name : str | None = Field(default = None)
    city : str | None = Field(default = None)
    pincode : int | None = Field(default = None)
    latitude : float | None = Field(default = None)
    longitude : float | None = Field(default = None)
    created_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    

class Rolecode(SQLModel, table = True):
    """ storing rolecode information """
    __tablename__ = "rolecode"
    id : int | None =  Field(primary_key = True)
    name : str | None = Field(default = None)
    status : bool | None = Field(default = None)
    created_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    
class Login(SQLModel):
    email: str
    password: str
    
class Users(SQLModel, table=True):
  """schema for storing users."""
  __tablename__ = "users"
  id: int | None=Field(primary_key=True)
  username: str | None=Field(default=None)
  first_name: str | None=Field(default=None) 
  last_name: str | None=Field(default=None)
  dob: date | None=Field(default=None)
  gender: str | None=Field(default=None)
  phone: str | None=Field(default=None)
  email : str | None = Field(index = True, unique = True)
  address_id : int = Field(foreign_key = "address.id")
  address: Address = Relationship()
  emergency_contact: str | None=Field(default=None)
  blood_group: str | None=Field(default=None)
  password: str | None=Field(default=None)
  specialization: str | None=Field(default=None)
  qualification: str | None=Field(default=None)
  experience: int | None=Field(default=None)
  registration_no: str | None=Field(default=None)
  consultation_fee: Decimal | None=Field(default=None)
  status: str | None=Field(default=None)
  rolecodes_id: int = Field(foreign_key = "rolecode.id")
  rolecode: Rolecode = Relationship()
  created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
  updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Permission(SQLModel, table = True):
    __tablename__ = "permission"
    id : int | None = Field(primary_key = True)
    name: str | None = Field(default = None)
    status : bool | None =  Field(default = None)
    users_id : int = Field(foreign_key = "users.id")
    user : Users = Relationship()
    created_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))