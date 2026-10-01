from  sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from datetime import datetime, date

class Address(SQLModel, table = True):
    """ storing address information """
    __tablename__ = "address"
    id : int | None =  Field(primary_key = True)
    name : str | None = Field(default = None)
    city : str | None = Field(default = None)
    pincode : int | None = Field(default = None)
    latitude : float | None = Field(default = None)
    longitude : float | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class Rolecode(SQLModel, table = True):
    """ storing rolecode information """
    __tablename__ = "rolecode"
    id : int | None =  Field(primary_key = True)
    name : str | None = Field(default = None)
    status : bool | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


    
class Login(SQLModel):
    email: str
    password: str
    
class Users(SQLModel, table = True):
    """ stroing users information"""
    __tablename__ = "users"
    id : int | None = Field(primary_key = True)
    username : str | None = Field(default = None)
    firstname : str | None = Field(default = None)
    lastname  : str | None = Field(default = None)
    email : str  = Field(index = True, unique = True)
    phone : int | None = Field(default = None)
    dob : date | None = Field(default = None)
    gender : str | None = Field(default = None)
    password : str | None = Field(default = None)
    address_id : int  = Field(foreign_key  = "address.id")
    address : Address = Relationship()
    rolecode_id: int = Field(foreign_key="rolecode.id")
    rolecode: Rolecode = Relationship()
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class Permission(SQLModel, table = True):
    __tablename__ = "permission"
    id : int | None = Field(primary_key = True)
    name: str | None = Field(default = None)
    status : bool | None =  Field(default = None)
    users_id : int = Field(foreign_key = "users.id")
    users : Users = Relationship()
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)