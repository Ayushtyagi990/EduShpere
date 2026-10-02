from fastapi import FastAPI, Header, Depends, HTTPException, Request
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
from datetime import datetime
from model import Address, Rolecode, Users, Login, Permission
from security import hash_password, verify_password
from database import get_session
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2PasswordBearer


security = HTTPBearer()

SECRET_KEY = "priyanshu"
ALGORITHM = "HS256"

app = FastAPI(
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc"
)

app.add_middleware(JWTMiddleware)

@app.post("/address")
def create_address(
    address: Address,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    token = credentials.credentials

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    session.add(address)
    session.commit()
    session.refresh(address)

    return {
        "created_by": payload["id"],
        "address": address
    }

@app.get("/address")
def get_address(credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    address = session.exec(select(Address)).all()

    return {
        "user": payload,
        "addresses": address
    }

@app.get("/address/{address_id}")
def get_address_by_id(address_id : int,  session : Session = Depends(get_session) ):
    address = session.get(Address,address_id)
    return address

@app.delete("/address/", status_code=204)
def delete_address(session : Session = Depends(get_session)):
    address = session.exec(select(Address)).all()
    for add in  address:
     session.delete(add)
     session.refresh()
    return {"details" : "all address deleted"}

@app.delete("/address/{address_id}", status_code = 204)
def delete_address(address_id : int, session : Session = Depends(get_session)):
   address = session.get(Address, address_id)
   if not address:
        raise HTTPException(status_code=404, detail="address not found")
   session.delete(address)
   session.commit()
   return {"details " :  f" address { address_id} deleted "}

@app.put("/address/")
def update_all_addresses(data: Address, session: Session = Depends(get_session)):
    addresses = session.exec(select(Address)).all()
    if not addresses:
        raise HTTPException(status_code=404, detail="Addresses not found")

    update_data = data.dict(exclude_unset=True)
    for a in addresses:
        for key, value in update_data.items():
            setattr(a, key, value)

    session.commit()
    for a in addresses:
        session.refresh(a)
    return addresses

@app.put("/address/{address_id}")
def update_address_by_id(address_id: int, data: Address, session: Session = Depends(get_session)):
    address = session.get(Address, address_id)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(address, key, value)

    session.commit()
    session.refresh(address)
    return address

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

@app.post("/login")
def login(data: Login, session: Session = Depends(get_session)):
    email = data.email.strip().lower()
    user = session.exec(
        select(Users).where(Users.email == email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_matches = verify_password(data.password, user.password or "")
    # Keep legacy development accounts usable if they contain plain text.
    if not password_matches and data.password != user.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    permission = session.exec(
        select(Permission)
        .where(Permission.users_id == user.id)
    ).first()

    token = create_access_token({
        "id": user.id,
        "role": user.rolecode_id,
        "permissions": permission.name if permission else {}
    })

    return {
        "access_token": token,
        "token_type": "Bearer"
    }
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



@app.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    return {
        "message": "Logout successful",
        "user_id": payload["id"]
    }

@app.post("/users")
def create_user(user: Users, session: Session = Depends(get_session)):
    existing_user = session.exec(select(Users).where(Users.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email is already registered")

    # The signup form uses these IDs by default. Create development defaults
    # when the referenced lookup rows have not been seeded yet.
    if user.address_id and session.get(Address, user.address_id) is None:
        session.add(Address(id=user.address_id, name="Default address"))
    if user.rolecode_id and session.get(Rolecode, user.rolecode_id) is None:
        session.add(Rolecode(id=user.rolecode_id, name="customer", status=True))

    user.password = hash_password(user.password or "")
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Unable to create user with these details")

    # Never return the stored password hash to the browser.
    user.password = None
    return user

@app.get("/users")
def get_users(credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    users = session.exec(select(Users)).all()

    return {
        "user": payload,
        "users": users
    }



@app.delete("/users/{users_id}", status_code=204)
def delete_user_by_id(users_id: int, session: Session = Depends(get_session)):
    user = session.get(Users, users_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"details " :  f" users { users_id} deleted "}


@app.put("/users/")
def update_all_users(data: Users, session: Session = Depends(get_session)):
    User = session.exec(select(Users)).all()
    if not User:
        raise HTTPException(status_code=404, detail="users not found")

    update_data = data.dict(exclude_unset=True)
    for use in User:
        for key, value in update_data.items():
            setattr(use, key, value)

    session.commit()
    for use in User:
        session.refresh(use)
    return User


@app.put("/users/{users_id}")
def update_user_by_id(users_id: int, data: Users, session: Session = Depends(get_session)):
    user = session.get(Users, users_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(user, key, value)

    session.commit()
    session.refresh(user)
    return user























@app.post("/permission")
def create_permission(permission: Permission,session: Session = Depends(get_session)):
    permission.created_at = datetime.now()
    permission.updated_at = datetime.now()

    session.add(permission)
    session.commit()
    session.refresh(permission)

    return {
        "message": "Permission created successfully",
        "data": permission
    }

@app.get("/permission")
def get_permission(permission : Permission, session : Session = Depends(get_session)):
    permission = session.exec(select(Permission)).all()
    return permission

@app.get("/permission")
def get_permission_by_id(permission_id : int, session : Session = Depends(get_session)):
    permission = session.get(permission, permission_id)
    return permission









@app.post("/rolecode")
def create_rolecode(Rolecode: Rolecode, session: Session = Depends(get_session)):
    session.add(Rolecode)
    session.commit()
    session.refresh(Rolecode)
    return Rolecode
@app.get("/rolecode/{rolecode_id}")
def get_rolecode_by_id(rolecode_id: int, session: Session = Depends(get_session)):
    rolecode = session.get(Rolecode, rolecode_id)
    if not rolecode:
        raise HTTPException(status_code=404, detail="RoleCode not found")
    return rolecode


@app.get("/rolecode")
def get_rolecode(credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    rolecode = session.exec(select(Rolecode)).all()

    return {
        "user": payload,
        "rolecode": rolecode
    }

@app.delete("/rolecode/", status_code=204)
def delete_all_rolecodes(session: Session = Depends(get_session)):
    all_rolecodes = session.exec(select(Rolecode)).all()
    for item in all_rolecodes:
     session.delete(item)
    session.commit()
    return {"details" : "all rolecode deleted"}


@app.delete("/rolecode/{rolecode_id}", status_code=204)
def delete_rolecode_by_id(rolecode_id: int, session: Session = Depends(get_session)):
    rolecode = session.get(Rolecode, rolecode_id)
    if not rolecode:
        raise HTTPException(status_code=404, detail="RoleCode not found")
    session.delete(rolecode)
    session.commit()
    return {"details " :  f" rolecode { rolecode_id} deleted "}

@app.put("/rolecode/")
def update_all_rolecodes(data: Rolecode, session: Session = Depends(get_session)):
    rolecodes = session.exec(select(Rolecode)).all()
    if not rolecodes:
        raise HTTPException(status_code=404, detail="RoleCodes not found")

    update_data = data.dict(exclude_unset=True)
    for role in rolecodes:
        for key, value in update_data.items():
            setattr(role, key, value)

    session.commit()
    for role in rolecodes:
        session.refresh(role)
    return rolecodes
@app.put("/rolecode/{rolecode_id}")
def update_rolecode_by_id(rolecode_id: int, data: Rolecode, session: Session = Depends(get_session)):
    rolecodes = session.get(Rolecode, rolecode_id)
    if not rolecodes:
        raise HTTPException(status_code=404, detail="RoleCode not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(rolecodes, key, value)

    session.commit()
    session.refresh(rolecodes)
    return rolecodes