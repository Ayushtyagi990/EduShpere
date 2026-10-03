
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from common.auth_middleware import JWTMiddleware
from model import (
    BiometricDevice,
    BiometricEnrollment,
    PunchLog,
    SyncRun,
    DeviceConfiguration,
    DeviceCommand,
    DeviceHealth,
    AuditLog,
)
from database import get_session

from jose import jwt, JWTError


# ============================================================
# SECURITY
# ============================================================

security = HTTPBearer()

SECRET_KEY = "priyanshu"
ALGORITHM = "HS256"


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
)

app.add_middleware(JWTMiddleware)


# ============================================================
# JWT VERIFICATION
# ============================================================

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token",
        )


# ============================================================
# BIOMETRIC DEVICE
# ============================================================

@app.post("/biometric-device")
def create_biometric_device(
    biometric_device: BiometricDevice,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing_device = session.exec(
        select(BiometricDevice).where(
            BiometricDevice.serial_number
            == biometric_device.serial_number
        )
    ).first()

    if existing_device:
        raise HTTPException(
            status_code=409,
            detail="Device with this serial number already exists",
        )

    biometric_device.created_at = datetime.now()
    biometric_device.updated_at = datetime.now()

    session.add(biometric_device)

    try:
        session.commit()
        session.refresh(biometric_device)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create biometric device",
        )

    return biometric_device


@app.get("/biometric-device")
def get_biometric_devices(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    devices = session.exec(
        select(BiometricDevice)
    ).all()

    return {
        "user": payload,
        "biometric_devices": devices,
    }


@app.get("/biometric-device/{device_id}")
def get_biometric_device_by_id(
    device_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    device = session.get(
        BiometricDevice,
        device_id,
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Biometric device not found",
        )

    return device


@app.put("/biometric-device/{device_id}")
def update_biometric_device_by_id(
    device_id: int,
    data: BiometricDevice,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    device = session.get(
        BiometricDevice,
        device_id,
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Biometric device not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(device, key, value)

    device.updated_at = datetime.now()

    session.add(device)
    session.commit()
    session.refresh(device)

    return device


@app.delete("/biometric-device/{device_id}")
def delete_biometric_device_by_id(
    device_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    device = session.get(
        BiometricDevice,
        device_id,
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Biometric device not found",
        )

    session.delete(device)
    session.commit()

    return {
        "details": f"biometric device {device_id} deleted"
    }


# ============================================================
# BIOMETRIC ENROLLMENT
# ============================================================

@app.post("/biometric-enrollment")
def create_biometric_enrollment(
    enrollment: BiometricEnrollment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    existing_enrollment = session.exec(
        select(BiometricEnrollment).where(
            BiometricEnrollment.device_user_id
            == enrollment.device_user_id
        )
    ).first()

    if existing_enrollment:
        raise HTTPException(
            status_code=409,
            detail="Device user already enrolled",
        )

    enrollment.enrolled_at = datetime.now()
    enrollment.updated_at = datetime.now()

    session.add(enrollment)

    try:
        session.commit()
        session.refresh(enrollment)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create enrollment",
        )

    return enrollment


@app.get("/biometric-enrollment")
def get_biometric_enrollments(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    enrollments = session.exec(
        select(BiometricEnrollment)
    ).all()

    return {
        "user": payload,
        "biometric_enrollments": enrollments,
    }


@app.get("/biometric-enrollment/{enrollment_id}")
def get_biometric_enrollment_by_id(
    enrollment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    enrollment = session.get(
        BiometricEnrollment,
        enrollment_id,
    )

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Biometric enrollment not found",
        )

    return enrollment


@app.put("/biometric-enrollment/{enrollment_id}")
def update_biometric_enrollment_by_id(
    enrollment_id: int,
    data: BiometricEnrollment,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    enrollment = session.get(
        BiometricEnrollment,
        enrollment_id,
    )

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Biometric enrollment not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(enrollment, key, value)

    enrollment.updated_at = datetime.now()

    session.add(enrollment)
    session.commit()
    session.refresh(enrollment)

    return enrollment


@app.delete("/biometric-enrollment/{enrollment_id}")
def delete_biometric_enrollment_by_id(
    enrollment_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    enrollment = session.get(
        BiometricEnrollment,
        enrollment_id,
    )

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="Biometric enrollment not found",
        )

    session.delete(enrollment)
    session.commit()

    return {
        "details": f"biometric enrollment {enrollment_id} deleted"
    }


# ============================================================
# PUNCH LOG
# ============================================================

@app.post("/punch")
def create_punch(
    punch: PunchLog,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    device = session.get(
        BiometricDevice,
        punch.device_id,
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Biometric device not found",
        )

    if punch.enrollment_id:

        enrollment = session.get(
            BiometricEnrollment,
            punch.enrollment_id,
        )

        if not enrollment:
            raise HTTPException(
                status_code=404,
                detail="Biometric enrollment not found",
            )

    punch.created_at = datetime.now()

    session.add(punch)

    try:
        session.commit()
        session.refresh(punch)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Duplicate punch record",
        )

    return punch


@app.get("/punch")
def get_punches(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    punches = session.exec(
        select(PunchLog)
    ).all()

    return {
        "user": payload,
        "punches": punches,
    }


@app.get("/punch/{punch_id}")
def get_punch_by_id(
    punch_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    punch = session.get(
        PunchLog,
        punch_id,
    )

    if not punch:
        raise HTTPException(
            status_code=404,
            detail="Punch record not found",
        )

    return punch


@app.put("/punch/{punch_id}")
def update_punch(
    punch_id: int,
    data: PunchLog,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    punch = session.get(
        PunchLog,
        punch_id,
    )

    if not punch:
        raise HTTPException(
            status_code=404,
            detail="Punch record not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(punch, key, value)

    session.add(punch)
    session.commit()
    session.refresh(punch)

    return punch


@app.delete("/punch/{punch_id}")
def delete_punch(
    punch_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    punch = session.get(
        PunchLog,
        punch_id,
    )

    if not punch:
        raise HTTPException(
            status_code=404,
            detail="Punch record not found",
        )

    session.delete(punch)
    session.commit()

    return {
        "details": f"punch {punch_id} deleted"
    }


# ============================================================
# SYNC RUN
# ============================================================

@app.post("/sync-run")
def create_sync_run(
    sync_run: SyncRun,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    sync_run.started_at = datetime.now()
    sync_run.status = "RUNNING"

    session.add(sync_run)
    session.commit()
    session.refresh(sync_run)

    return sync_run


@app.get("/sync-run")
def get_sync_runs(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    sync_runs = session.exec(
        select(SyncRun)
    ).all()

    return {
        "user": payload,
        "sync_runs": sync_runs,
    }


@app.get("/sync-run/{sync_run_id}")
def get_sync_run_by_id(
    sync_run_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    sync_run = session.get(
        SyncRun,
        sync_run_id,
    )

    if not sync_run:
        raise HTTPException(
            status_code=404,
            detail="Sync run not found",
        )

    return sync_run


@app.put("/sync-run/{sync_run_id}")
def update_sync_run(
    sync_run_id: int,
    data: SyncRun,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    sync_run = session.get(
        SyncRun,
        sync_run_id,
    )

    if not sync_run:
        raise HTTPException(
            status_code=404,
            detail="Sync run not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(sync_run, key, value)

    sync_run.finished_at = datetime.now()

    session.add(sync_run)
    session.commit()
    session.refresh(sync_run)

    return sync_run


@app.delete("/sync-run/{sync_run_id}")
def delete_sync_run(
    sync_run_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    sync_run = session.get(
        SyncRun,
        sync_run_id,
    )

    if not sync_run:
        raise HTTPException(
            status_code=404,
            detail="Sync run not found",
        )

    session.delete(sync_run)
    session.commit()

    return {
        "details": f"sync run {sync_run_id} deleted"
    }


# ============================================================
# DEVICE CONFIGURATION
# ============================================================

@app.post("/device-configuration")
def create_device_configuration(
    configuration: DeviceConfiguration,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    device = session.get(
        BiometricDevice,
        configuration.device_id,
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Biometric device not found",
        )

    configuration.created_at = datetime.now()
    configuration.updated_at = datetime.now()

    session.add(configuration)

    try:
        session.commit()
        session.refresh(configuration)

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to create device configuration",
        )

    return configuration


@app.get("/device-configuration")
def get_device_configurations(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    configurations = session.exec(
        select(DeviceConfiguration)
    ).all()

    return {
        "user": payload,
        "device_configurations": configurations,
    }


@app.get("/device-configuration/{configuration_id}")
def get_device_configuration_by_id(
    configuration_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    configuration = session.get(
        DeviceConfiguration,
        configuration_id,
    )

    if not configuration:
        raise HTTPException(
            status_code=404,
            detail="Device configuration not found",
        )

    return configuration


@app.put("/device-configuration/{configuration_id}")
def update_device_configuration(
    configuration_id: int,
    data: DeviceConfiguration,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    configuration = session.get(
        DeviceConfiguration,
        configuration_id,
    )

    if not configuration:
        raise HTTPException(
            status_code=404,
            detail="Device configuration not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(configuration, key, value)

    configuration.updated_at = datetime.now()

    session.add(configuration)
    session.commit()
    session.refresh(configuration)

    return configuration


@app.delete("/device-configuration/{configuration_id}")
def delete_device_configuration(
    configuration_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    configuration = session.get(
        DeviceConfiguration,
        configuration_id,
    )

    if not configuration:
        raise HTTPException(
            status_code=404,
            detail="Device configuration not found",
        )

    session.delete(configuration)
    session.commit()

    return {
        "details": f"device configuration {configuration_id} deleted"
    }


# ============================================================
# DEVICE COMMAND
# ============================================================

@app.post("/device-command")
def create_device_command(
    command: DeviceCommand,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    device = session.get(
        BiometricDevice,
        command.device_id,
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Biometric device not found",
        )

    command.created_at = datetime.now()
    command.status = "PENDING"

    session.add(command)
    session.commit()
    session.refresh(command)

    return command


@app.get("/device-command")
def get_device_commands(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    commands = session.exec(
        select(DeviceCommand)
    ).all()

    return {
        "user": payload,
        "device_commands": commands,
    }


@app.get("/device-command/{command_id}")
def get_device_command_by_id(
    command_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    command = session.get(
        DeviceCommand,
        command_id,
    )

    if not command:
        raise HTTPException(
            status_code=404,
            detail="Device command not found",
        )

    return command


@app.put("/device-command/{command_id}")
def update_device_command(
    command_id: int,
    data: DeviceCommand,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    command = session.get(
        DeviceCommand,
        command_id,
    )

    if not command:
        raise HTTPException(
            status_code=404,
            detail="Device command not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(command, key, value)

    session.add(command)
    session.commit()
    session.refresh(command)

    return command


@app.delete("/device-command/{command_id}")
def delete_device_command(
    command_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    command = session.get(
        DeviceCommand,
        command_id,
    )

    if not command:
        raise HTTPException(
            status_code=404,
            detail="Device command not found",
        )

    session.delete(command)
    session.commit()

    return {
        "details": f"device command {command_id} deleted"
    }


# ============================================================
# DEVICE HEALTH
# ============================================================

@app.post("/device-health")
def create_device_health(
    health: DeviceHealth,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    device = session.get(
        BiometricDevice,
        health.device_id,
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Biometric device not found",
        )

    health.created_at = datetime.now()
    health.last_checked_at = datetime.now()

    session.add(health)
    session.commit()
    session.refresh(health)

    return health


@app.get("/device-health")
def get_device_health(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    health_records = session.exec(
        select(DeviceHealth)
    ).all()

    return {
        "user": payload,
        "device_health": health_records,
    }


@app.get("/device-health/{health_id}")
def get_device_health_by_id(
    health_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    health = session.get(
        DeviceHealth,
        health_id,
    )

    if not health:
        raise HTTPException(
            status_code=404,
            detail="Device health record not found",
        )

    return health


@app.put("/device-health/{health_id}")
def update_device_health(
    health_id: int,
    data: DeviceHealth,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    health = session.get(
        DeviceHealth,
        health_id,
    )

    if not health:
        raise HTTPException(
            status_code=404,
            detail="Device health record not found",
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():

        if key != "id":
            setattr(health, key, value)

    health.last_checked_at = datetime.now()

    session.add(health)
    session.commit()
    session.refresh(health)

    return health


@app.delete("/device-health/{health_id}")
def delete_device_health(
    health_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    health = session.get(
        DeviceHealth,
        health_id,
    )

    if not health:
        raise HTTPException(
            status_code=404,
            detail="Device health record not found",
        )

    session.delete(health)
    session.commit()

    return {
        "details": f"device health {health_id} deleted"
    }


# ============================================================
# AUDIT LOG
# ============================================================

@app.post("/audit-log")
def create_audit_log(
    audit_log: AuditLog,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    audit_log.created_at = datetime.now()

    session.add(audit_log)
    session.commit()
    session.refresh(audit_log)

    return audit_log


@app.get("/audit-log")
def get_audit_logs(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    audit_logs = session.exec(
        select(AuditLog)
    ).all()

    return {
        "user": payload,
        "audit_logs": audit_logs,
    }


@app.get("/audit-log/{audit_id}")
def get_audit_log_by_id(
    audit_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    audit_log = session.get(
        AuditLog,
        audit_id,
    )

    if not audit_log:
        raise HTTPException(
            status_code=404,
            detail="Audit log not found",
        )

    return audit_log


@app.delete("/audit-log/{audit_id}")
def delete_audit_log(
    audit_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    audit_log = session.get(
        AuditLog,
        audit_id,
    )

    if not audit_log:
        raise HTTPException(
            status_code=404,
            detail="Audit log not found",
        )

    session.delete(audit_log)
    session.commit()

    return {
        "details": f"audit log {audit_id} deleted"
    }

