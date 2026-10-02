from  sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date, time


class LeaveType(SQLModel, table = True):
    __tablename__ = "leavetype"
    id : int | None = Field(primary_key = True)
    name : str | None = Field(default = None)
    description : str | None = Field(default = None)
    max_days : int | None = Field(default = None)
    applicable_for : int | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class LeaveRequest(SQLModel, table = True):
    __tablename__ = "leaverequest"
    id : int | None = Field(primary_key = True)
    leave_type_id : int  = Field(foreign_key  = "leavetype.id")
    leave_type : LeaveType = Relationship()
    user_id : int | None = Field(default = None)
    start_date : date | None = Field(default = None)
    end_date : date | None = Field(default = None)
    reason : str | None = Field(default = None)
    status : str | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

class LeaveApprovalHistory(SQLModel, table = True):
    __tablename__ = "leave_approval_history"
    id : int | None = Field(Primary_key = True)
    leave_request_id : int  = Field(foreign_key  = "leaverequest.id")
    leave_request : LeaveRequest = Relationship()
    approver_id : int | None = Field(default = None)
    action : str | None = Field(default = None)
    remarks : str | None = Field(default = None)
    action_date : datetime | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)

