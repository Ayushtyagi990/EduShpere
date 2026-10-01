from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date


class Category(SQLModel, table = True):
    __tablename__ = "category"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None, index = True)
    description : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Supplier(SQLModel, table = True):
    __tablename__ = "supplier"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    contact_person : str | None = Field(default = None)
    email : str | None = Field(default = None)
    phone : str | None = Field(default = None)
    address : str | None = Field(default = None)
    is_active : bool | None = Field(default = True)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Warehouse(SQLModel, table = True):
    __tablename__ = "warehouse"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    location : str | None = Field(default = None)
    capacity : int | None = Field(default = None)
    is_active : bool | None = Field(default = True)
    stocks : int | None = Field(default = None) 
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)
    stocks : list["Stock"] = Relationship(back_populates = "warehouse")


class Item(SQLModel, table = True):
    __tablename__ = "item"
    id : int | None = Field(primary_key = True)
    sku : str | None = Field(index = True, unique = True)
    name : str | None = Field(default = None, index = True)
    description : str | None = Field(default = None)
    category_id : int | None = Field(foreign_key = "category.id")
    category : Category = Relationship()
    supplier_id : int | None = Field(foreign_key = "supplier.id")
    supplier : Supplier = Relationship()
    stocks : int | None = Field(default = None) 
    unit : str | None = Field(default = None)
    unit_price : float | None = Field(default = None)
    reorder_level : int | None = Field(default = None)
    is_active : bool | None = Field(default = True)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Stock(SQLModel, table = True):
    __tablename__ = "stock"
    id : int | None = Field(primary_key = True)
    item_id : int | None = Field(foreign_key = "item.id")
    item : Item = Relationship()
    warehouse_id : int | None = Field(foreign_key = "warehouse.id")
    warehouse : Warehouse = Relationship()
    quantity : int | None = Field(default = None)
    reserved_quantity : int | None = Field(default = None)
    batch_number : str | None = Field(default = None)
    expiry_date : date | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class StockMovement(SQLModel, table = True):
    __tablename__ = "stockmovement"
    id : int | None = Field(primary_key = True)
    item_id : int | None = Field(foreign_key = "item.id")
    item : Item = Relationship()
    warehouse_id : int | None = Field(foreign_key = "warehouse.id")
    warehouse : Warehouse = Relationship()
    movement_type : str | None = Field(default = None)
    quantity : int | None = Field(default = None)
    reference : str | None = Field(default = None)
    remarks : str | None = Field(default = None)
    performed_by : int | None = Field(default = None)
    movement_date : datetime | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)
