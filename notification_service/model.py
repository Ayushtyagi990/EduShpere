from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, JSON
from datetime import datetime


class Notification_Template(SQLModel, table=True):
    __tablename__ = "notification_templates"
    id : int | None = Field(default = None, primary_key = True)
    name : str | None = Field(default = None, index = True)
    channel : str | None = Field(default = None)
    subject : str | None = Field(default = None)
    body : str | None = Field(default = None)
    variables : dict | None = Field(default = None, sa_column = Column(JSON))
    is_active : bool | None = Field(default = True)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class Notification(SQLModel, table=True):
    __tablename__ = "notification"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int
    template_id: int | None = Field(default=None)

    channel: str | None = Field(default=None)
    title: str | None = Field(default=None)
    message: str | None = Field(default=None)
    data: dict | None = Field(default=None, sa_column=Column(JSON))
    priority: str | None = Field(default=None)
    status: str | None = Field(default=None, index=True)
    is_read: bool | None = Field(default=False)
    notificationTemplate_id: int | None = Field(foreign_key="notification_templates.id")
    notificationTemplate: Notification_Template | None = Relationship()
    scheduled_at: datetime | None = Field(default=None)
    sent_at: datetime | None = Field(default=None)
    read_at: datetime | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    

class NotificationLog(SQLModel, table = True):
    __tablename__ = "notificationlog"
    id : int | None = Field(default = None, primary_key = True)
    notification_id : int | None = Field(default = None, foreign_key = "notification.id")
    channel : str | None = Field(default = None)
    recipient : str | None = Field(default = None)
    status : str | None = Field(default = None)
    provider_response : str | None = Field(default = None)
    error_message : str | None = Field(default = None)
    attempt : int | None = Field(default = None)
    attempted_at : datetime | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)


class NotificationPreference(SQLModel, table = True):
    __tablename__ = "notificationpreference"
    id : int | None = Field(default = None, primary_key = True)
    user_id : int | None = Field(default = None, index = True)
    channel : str | None = Field(default = None)
    category : str | None = Field(default = None)
    is_enabled : bool | None = Field(default = True)
    quiet_hours_start : datetime | None = Field(default = None)
    quiet_hours_end : datetime | None = Field(default = None)
    created_at : datetime | None = Field(default = None)
    updated_at : datetime | None = Field(default = None)