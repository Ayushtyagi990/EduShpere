from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from common.auth_middleware import JWTMiddleware
from model import ReportType, Report, ReportSchedule, ReportDownload
from database import get_session, create_db_and_tables
from jose import jwt, JWTError


security = HTTPBearer()

# Same signing key/algorithm as the users service, since tokens are issued
# there and only verified here.
SECRET_KEY = os.getenv("SECRET_KEY", "priyanshu")
ALGORITHM = "HS256"


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(JWTMiddleware)

PROTECTED_FIELDS = {"id", "created_at"}


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return payload


def get_or_404(session: Session, model, obj_id: int, name: str):
    obj = session.get(model, obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"{name} not found")
    return obj


# --------------------------------------------------------------------------
# ReportType
# --------------------------------------------------------------------------
@app.post("/reportType")
def create_reportType(
    reportType: ReportType,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    exists = session.exec(
        select(ReportType).where(ReportType.code == reportType.code)
    ).first()
    if exists:
        raise HTTPException(status_code=409, detail="reportType code already exists")
    reportType.created_at = datetime.now()
    reportType.updated_at = datetime.now()
    session.add(reportType)
    session.commit()
    session.refresh(reportType)
    return reportType


@app.get("/reportType")
def get_reportType(session: Session = Depends(get_session)):
    return session.exec(select(ReportType)).all()


@app.get("/reportType/{reportType_id}")
def get_reportType_by_id(reportType_id: int, session: Session = Depends(get_session)):
    return get_or_404(session, ReportType, reportType_id, "reportType")


@app.put("/reportType/{reportType_id}")
def update_reportType_by_id(
    reportType_id: int,
    data: ReportType,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    reportType = get_or_404(session, ReportType, reportType_id, "reportType")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(reportType, key, value)
    reportType.updated_at = datetime.now()

    session.add(reportType)
    session.commit()
    session.refresh(reportType)
    return reportType


@app.delete("/reportType/{reportType_id}", status_code=204)
def delete_reportType_by_id(
    reportType_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    reportType = get_or_404(session, ReportType, reportType_id, "reportType")
    used = session.exec(
        select(Report).where(Report.report_type_id == reportType_id)
    ).first()
    if used:
        raise HTTPException(
            status_code=409,
            detail="reportType is used by reports, set is_active to false instead",
        )
    session.delete(reportType)
    session.commit()


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
@app.post("/report")
def create_report(
    report: Report,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    reportType = get_or_404(session, ReportType, report.report_type_id, "reportType")
    if not reportType.is_active:
        raise HTTPException(status_code=400, detail="reportType is not active")
    if report.date_from and report.date_to and report.date_from > report.date_to:
        raise HTTPException(status_code=400, detail="date_from must be before date_to")
    report.status = "pending"
    report.created_at = datetime.now()
    report.updated_at = datetime.now()
    session.add(report)
    session.commit()
    session.refresh(report)
    return report


@app.get("/report")
def get_report(
    status: str | None = None,
    report_type_id: int | None = None,
    session: Session = Depends(get_session),
):
    query = select(Report)
    if status:
        query = query.where(Report.status == status)
    if report_type_id:
        query = query.where(Report.report_type_id == report_type_id)
    return session.exec(query).all()


@app.get("/report/{report_id}")
def get_report_by_id(report_id: int, session: Session = Depends(get_session)):
    return get_or_404(session, Report, report_id, "report")


@app.put("/report/{report_id}")
def update_report_by_id(
    report_id: int,
    data: Report,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    report = get_or_404(session, Report, report_id, "report")

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(report, key, value)
    if report.status == "completed":
        if not report.file_path:
            raise HTTPException(
                status_code=400, detail="file_path is required when status is completed"
            )
        report.completed_at = datetime.now()
    report.updated_at = datetime.now()

    session.add(report)
    session.commit()
    session.refresh(report)
    return report


@app.delete("/report/{report_id}", status_code=204)
def delete_report_by_id(
    report_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    report = get_or_404(session, Report, report_id, "report")
    downloads = session.exec(
        select(ReportDownload).where(ReportDownload.report_id == report_id)
    ).all()
    for download in downloads:
        session.delete(download)
    session.delete(report)
    session.commit()


@app.get("/report/{report_id}/download")
def download_report(
    report_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    report = get_or_404(session, Report, report_id, "report")
    if report.status != "completed" or not report.file_path:
        raise HTTPException(status_code=400, detail="report is not ready yet")
    path = Path(report.file_path)
    if not path.is_file():
        raise HTTPException(status_code=404, detail="report file not found on server")

    download = ReportDownload(
        report_id=report_id,
        downloaded_at=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    session.add(download)
    session.commit()
    return FileResponse(path, filename=path.name)


# --------------------------------------------------------------------------
# ReportSchedule
# --------------------------------------------------------------------------
@app.post("/reportSchedule")
def create_reportSchedule(
    reportSchedule: ReportSchedule,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    reportType = get_or_404(
        session, ReportType, reportSchedule.report_type_id, "reportType"
    )
    if not reportType.is_active:
        raise HTTPException(status_code=400, detail="reportType is not active")
    reportSchedule.created_at = datetime.now()
    reportSchedule.updated_at = datetime.now()
    session.add(reportSchedule)
    session.commit()
    session.refresh(reportSchedule)
    return reportSchedule


@app.get("/reportSchedule")
def get_reportSchedule(session: Session = Depends(get_session)):
    return session.exec(select(ReportSchedule)).all()


@app.get("/reportSchedule/{reportSchedule_id}")
def get_reportSchedule_by_id(
    reportSchedule_id: int, session: Session = Depends(get_session)
):
    return get_or_404(session, ReportSchedule, reportSchedule_id, "reportSchedule")


@app.put("/reportSchedule/{reportSchedule_id}")
def update_reportSchedule_by_id(
    reportSchedule_id: int,
    data: ReportSchedule,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    reportSchedule = get_or_404(
        session, ReportSchedule, reportSchedule_id, "reportSchedule"
    )

    for key, value in data.model_dump(exclude_unset=True, exclude=PROTECTED_FIELDS).items():
        setattr(reportSchedule, key, value)
    reportSchedule.updated_at = datetime.now()

    session.add(reportSchedule)
    session.commit()
    session.refresh(reportSchedule)
    return reportSchedule


@app.delete("/reportSchedule/{reportSchedule_id}", status_code=204)
def delete_reportSchedule_by_id(
    reportSchedule_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    reportSchedule = get_or_404(
        session, ReportSchedule, reportSchedule_id, "reportSchedule"
    )
    session.delete(reportSchedule)
    session.commit()


# --------------------------------------------------------------------------
# ReportDownload (log)
# --------------------------------------------------------------------------
@app.post("/reportDownload")
def create_reportDownload(
    reportDownload: ReportDownload,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    get_or_404(session, Report, reportDownload.report_id, "report")
    reportDownload.downloaded_at = reportDownload.downloaded_at or datetime.now()
    reportDownload.created_at = datetime.now()
    reportDownload.updated_at = datetime.now()
    session.add(reportDownload)
    session.commit()
    session.refresh(reportDownload)
    return reportDownload


@app.get("/reportDownload")
def get_reportDownload(
    report_id: int | None = None, session: Session = Depends(get_session)
):
    query = select(ReportDownload)
    if report_id:
        query = query.where(ReportDownload.report_id == report_id)
    return session.exec(query).all()


@app.get("/reportDownload/{reportDownload_id}")
def get_reportDownload_by_id(
    reportDownload_id: int, session: Session = Depends(get_session)
):
    return get_or_404(session, ReportDownload, reportDownload_id, "reportDownload")


@app.delete("/reportDownload/{reportDownload_id}", status_code=204)
def delete_reportDownload_by_id(
    reportDownload_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    reportDownload = get_or_404(
        session, ReportDownload, reportDownload_id, "reportDownload"
    )
    session.delete(reportDownload)
    session.commit()