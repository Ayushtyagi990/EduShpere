from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
from common.auth_middleware import JWTMiddleware
from model import Notification_Template, Notification, NotificationLog, NotificationPreference
from database import get_session
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


security = HTTPBearer()

# Same signing key/algorithm as the users service, since tokens are issued
# there and only verified here.
SECRET_KEY = "priyanshu"
ALGORITHM = "HS256"

app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc"
)

app.add_middleware(JWTMiddleware)

DEFAULT_LOAN_DAYS = 14
FINE_PER_DAY = 5.0


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return payload


# --------------------------------------------------------------------------
#-----------------------------------------------------------
@app.post("/notification_template")
def create_notification_template(
    notification_template: Notification_Template,payload: dict = Depends(verify_token),  session: Session = Depends(get_session),
):
    notification_template.created_at = datetime.now()
    notification_template.updated_at = datetime.now()
    session.add(notification_template)
    session.commit()
    session.refresh(notification_template)
    return notification_template


@app.get("/notification_template")
def get_notification_template(session: Session = Depends(get_session)):
    return session.exec(select(Notification_Template)).all()




@app.put("/notification_Template/{notificationTemplate_id}")
def update_NotificationTemplate_by_id(notification_Template_id: int, data: Notification_Template, session: Session = Depends(get_session)):
    notification_Template = session.get(Notification_Template, notification_Template_id)
    if not notification_Template:
        raise HTTPException(status_code=404, detail="notification_Template not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(notification_Template, key, value)
    notification_Template.updated_at = datetime.now()

    session.commit()
    session.refresh(notification_Template)
    return notification_Template


@app.delete("/notification_Template/{notificationTemplate_id}", status_code=204)
def delete_notificationTemplate_by_id(notificationTemplate_id: int, session: Session = Depends(get_session)):
    notification_Template = session.get(Notification_Template, notificationTemplate_id)
    if not notification_Template:
        raise HTTPException(status_code=404, detail="notification_Template_id not found")
    session.delete(notification_Template)
    session.commit()
    return {"details": f" {notificationTemplate_id} deleted"}



@app.post("/notification")
def create_notification(
    notification: Notification,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    notification.created_at = datetime.now()
    notification.updated_at = datetime.now()
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


@app.get("/notification")
def get_notification(session: Session = Depends(get_session)):
    return session.exec(select(Notification)).all()


@app.get("/notification/{notification_id}")
def get_notification_by_id(notification_id: int, session: Session = Depends(get_session)):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Author not found")
    return notification


@app.put("/notification/{notification_id}")
def update_notification_by_id(notification_id: int, data: Notification, session: Session = Depends(get_session)):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(notification, key, value)
    notification.updated_at = datetime.now()

    session.commit()
    session.refresh(notification)
    return notification


@app.delete("/notification/{notification_id}", status_code=204)
def delete_notification_by_id(notification_id: int, session: Session = Depends(get_session)):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="notification not found")
    session.delete(notification)
    session.commit()
    return {"details": f"notification {notification_id} deleted"}



@app.post("/notificationLog")
def create_NotificationLog(
    notificationLog: NotificationLog,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    notificationLog.created_at = datetime.now()
    notificationLog.updated_at = datetime.now()
    session.add(notificationLog)
    session.commit()
    session.refresh(notificationLog)
    return notificationLog


@app.get("/notificationLog")
def get_notificationLog(session: Session = Depends(get_session)):
    return session.exec(select(NotificationLog)).all()


@app.get("/notificationLog/{notificationLog_id}")
def get_notificationLog_by_id(notificationLog_id: int, session: Session = Depends(get_session)):
    notificationLog = session.get(NotificationLog, notificationLog_id)
    if not notificationLog:
        raise HTTPException(status_code=404, detail="notificationLog not found")
    return notificationLog


@app.put("/notificationLog/{notificationLog_id}")
def update_notificationLog_by_id(notificationLog_id: int, data: NotificationLog, session: Session = Depends(get_session)):
    notificationLog = session.get(NotificationLog, notificationLog_id)
    if not notificationLog:
        raise HTTPException(status_code=404, detail="notificationLog not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(notificationLog, key, value)
    notificationLog.updated_at = datetime.now()

    session.commit()
    session.refresh(notificationLog)
    return notificationLog


@app.delete("/notificationLog/{notificationLog_id}", status_code=204)
def delete_notificationLog_by_id(notificationLog_id: int, session: Session = Depends(get_session)):
    notificationLog = session.get(NotificationLog, notificationLog_id)
    if not notificationLog:
        raise HTTPException(status_code=404, detail="notificationLog not found")
    session.delete(notificationLog)
    session.commit()
    return {"details": f"notificationLog {notificationLog_id} deleted"}



@app.post("/notification")
def create_notification(
    notification: Notification,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    notification.created_at = datetime.now()
    notification.updated_at = datetime.now()
    session.add(notification)
    session.commit()
    session.refresh(notification)
    return notification


@app.get("/notification")
def get_notification(session: Session = Depends(get_session)):
    return session.exec(select(Notification)).all()


@app.get("/notification/{notification_id}")
def get_notification_by_id(notification_id: int, session: Session = Depends(get_session)):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Author not found")
    return notification


@app.put("/notification/{notification_id}")
def update_notification_by_id(notification_id: int, data: Notification, session: Session = Depends(get_session)):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(notification, key, value)
    notification.updated_at = datetime.now()

    session.commit()
    session.refresh(notification)
    return notification


@app.delete("/notification/{notification_id}", status_code=204)
def delete_notification_by_id(notification_id: int, session: Session = Depends(get_session)):
    notification = session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="notification not found")
    session.delete(notification)
    session.commit()
    return {"details": f"notification {notification_id} deleted"}



@app.post("/notificationPreference")
def create_notificationPreference(
    notificationPreference: NotificationPreference,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    notificationPreference.created_at = datetime.now()
    notificationPreference.updated_at = datetime.now()
    session.add(notificationPreference)
    session.commit()
    session.refresh(notificationPreference)
    return notificationPreference


@app.get("/notificationPreference")
def get_notificationPreference(session: Session = Depends(get_session)):
    return session.exec(select(NotificationPreference)).all()


@app.get("/notificationPreference/{notificationPreference_id}")
def get_notificationPreference_by_id(notificationPreference_id: int, session: Session = Depends(get_session)):
    notificationPreference = session.get(NotificationPreference, notificationPreference_id)
    if not notificationPreference:
        raise HTTPException(status_code=404, detail="notificationPreference not found")
    return notificationPreference


@app.put("/notificationPreference/{notificationPreference_id}")
def update_notificationPreference_by_id(notificationPreference_id: int, data: NotificationPreference, session: Session = Depends(get_session)):
    notificationPreference = session.get(NotificationLog, notificationPreference_id)
    if not notificationPreference:
        raise HTTPException(status_code=404, detail="notificationPreference not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(notificationPreference, key, value)
    notificationPreference.updated_at = datetime.now()

    session.commit()
    session.refresh(notificationPreference)
    return notificationPreference


@app.delete("/notificationPreference/{notificationPreference_id}", status_code=204)
def delete_notificationPreference_by_id(notificationPreference_id: int, session: Session = Depends(get_session)):
    notificationPreference = session.get(NotificationPreference, notificationPreference_id)
    if not notificationPreference:
        raise HTTPException(status_code=404, detail="notificationPreference not found")
    session.delete(notificationPreference)
    session.commit()
    return {"details": f"notificationLog {notificationPreference_id} deleted"}



