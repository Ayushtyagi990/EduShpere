from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, Column, UniqueConstraint
from datetime import datetime


class BiometricDevice(SQLModel, table=True):
    __tablename__ = "biometric_device"
    id: int | None = Field(primary_key=True)
    name: str | None = Field(default=None)
    serial_number: str | None = Field(index=True, unique=True)
    vendor: str | None = Field(default=None)
    device_model: str | None = Field(default=None)
    device_type: str | None = Field(default=None)
    location: str | None = Field(default=None)
    ip_address: str | None = Field(default=None)
    port: int | None = Field(default=None)
    attendance_session_id: int | None = Field(default=None)
    api_key_hash: str | None = Field(default=None)
    is_active: bool = Field(default=True)
    last_seen_at: datetime | None = Field(default=None)
    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)
    

class BiometricEnrollment(SQLModel, table=True):
    __tablename__ = "biometric_enrollment"

    id: int | None = Field(primary_key=True)

    # STUDENT / STAFF
    person_type: str | None = Field(default=None)

    # Student admission number / Employee ID
    person_ref: str | None = Field(default=None, index=True)

    person_name: str | None = Field(default=None)

    # ID stored inside biometric machine
    device_user_id: str | None = Field(
        default=None,
        index=True,
        unique=True
    )

    # Academic service references
    class_id: int 
    section_id: int 


    is_active: bool = Field(default=True)

    enrolled_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)

   

class PunchLog(SQLModel, table=True):
    __tablename__ = "punch_log"

    __table_args__ = (
        UniqueConstraint(
            "device_id",
            "device_user_id",
            "punch_time",
            name="uq_punch_dedupe"
        ),
    )

    id: int | None = Field(primary_key=True)

    device_id: int = Field(
        foreign_key="biometric_device.id",
        index=True
    )

    device: BiometricDevice | None = Relationship(
        back_populates="punches"
    )

    enrollment_id: int | None = Field(
        foreign_key="biometric_enrollment.id",
        index=True
    )

    enrollment: BiometricEnrollment | None = Relationship(
        back_populates="punches"
    )

    device_user_id: str | None = Field(
        default=None,
        index=True
    )

    punch_time: datetime | None = Field(
        default=None,
        index=True
    )

    # IN / OUT / UNKNOWN
    punch_type: str | None = Field(default=None)

    # FINGER / FACE / CARD / PASSWORD / UNKNOWN
    verify_mode: str | None = Field(default=None)

    raw_payload: dict | None = Field(
        default=None,
        sa_column=Column(JSON)
    )

    # PENDING / SYNCED / FAILED / BLOCKED / IGNORED
    sync_status: str | None = Field(
        default="PENDING",
        index=True
    )

    sync_attempts: int = Field(default=0)

    sync_error: str | None = Field(default=None)

    synced_at: datetime | None = Field(default=None)

    created_at: datetime | None = Field(default=None)


class SyncRun(SQLModel, table=True):
    __tablename__ = "sync_run"

    id: int | None = Field(primary_key=True)

    started_at: datetime | None = Field(default=None)
    finished_at: datetime | None = Field(default=None)

    processed: int = Field(default=0)
    synced: int = Field(default=0)
    failed: int = Field(default=0)
    blocked: int = Field(default=0)
    ignored: int = Field(default=0)

    # RUNNING / OK / ERROR
    status: str | None = Field(default="RUNNING")

    error: str | None = Field(default=None)


class DeviceConfiguration(SQLModel, table=True):
    __tablename__ = "device_configuration"

    id: int | None = Field(primary_key=True)

    device_id: int = Field(
        foreign_key="biometric_device.id",
        index=True
    )

    connection_type: str | None = Field(default=None)

    ip_address: str | None = Field(default=None)
    port: int | None = Field(default=None)

    username: str | None = Field(default=None)
    password: str | None = Field(default=None)

    timeout: int | None = Field(default=10)

    status: str | None = Field(default=None)

    created_at: datetime | None = Field(default=None)
    updated_at: datetime | None = Field(default=None)


class DeviceCommand(SQLModel, table=True):
    __tablename__ = "device_command"

    id: int | None = Field(primary_key=True)

    device_id: int = Field(
        foreign_key="biometric_device.id",
        index=True
    )

    command: str | None = Field(default=None)

    payload: dict | None = Field(
        default=None,
        sa_column=Column(JSON)
    )

    status: str | None = Field(default="PENDING")

    response: str | None = Field(default=None)

    error: str | None = Field(default=None)

    created_at: datetime | None = Field(default=None)
    executed_at: datetime | None = Field(default=None)


class DeviceHealth(SQLModel, table=True):
    __tablename__ = "device_health"

    id: int | None = Field(primary_key=True)

    device_id: int = Field(
        foreign_key="biometric_device.id",
        index=True
    )

    status: str | None = Field(default=None)

    response_time: float | None = Field(default=None)

    last_checked_at: datetime | None = Field(default=None)

    error_message: str | None = Field(default=None)

    created_at: datetime | None = Field(default=None)


class AuditLog(SQLModel, table=True):
    __tablename__ = "audit_log"

    id: int | None = Field(primary_key=True)

    user_id: int | None = Field(default=None)

    action: str | None = Field(default=None)

    entity_type: str | None = Field(default=None)

    entity_id: int | None = Field(default=None)

    description: str | None = Field(default=None)

    ip_address: str | None = Field(default=None)

    created_at: datetime | None = Field(default=None)

