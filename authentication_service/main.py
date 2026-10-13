from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone, timedelta

import sys
import os
import traceback

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from common.auth_middleware import JWTMiddleware

from model import (
    Address,
    Rolecode,
    Users,
    Login,
    Permission,
)

from security import hash_password, verify_password
from database import get_session

from jose import jwt, JWTError

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)


# =========================================================
# SECURITY CONFIG
# =========================================================

security = HTTPBearer()

SECRET_KEY = "priyanshu"
ALGORITHM = "HS256"


# =========================================================
# APP
# =========================================================

app = FastAPI(
    title="EduSphere Authentication Service",
    description="Authentication and Authorization Management Service",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# JWT MIDDLEWARE
# =========================================================

app.add_middleware(JWTMiddleware)


# =========================================================
# COMMON FUNCTIONS
# =========================================================

def utc_now() -> datetime:
    return datetime.now(timezone.utc)


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
            detail="Invalid or expired token",
        )


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = utc_now() + timedelta(minutes=30)

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def remove_protected_fields(data: dict):
    """
    Prevent client from modifying:
    id
    created_at
    updated_at
    """

    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    return data


# =========================================================
# ADDRESS
# =========================================================

@app.post("/address")
def create_address(
    address: Address,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    try:
        now = utc_now()

        address.created_at = now
        address.updated_at = now

        session.add(address)
        session.commit()
        session.refresh(address)

        return {
            "message": "Address created successfully",
            "address": address,
        }

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Address already exists or violates database constraint",
        )


@app.get("/address")
def get_addresses(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    addresses = session.exec(
        select(Address)
    ).all()

    return {
        "user": payload,
        "addresses": addresses,
    }


@app.get("/address/{address_id}")
def get_address_by_id(
    address_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    address = session.get(Address, address_id)

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found",
        )

    return address


@app.delete("/address/")
def delete_all_addresses(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    addresses = session.exec(
        select(Address)
    ).all()

    for address in addresses:
        session.delete(address)

    session.commit()

    return {
        "message": "All addresses deleted successfully"
    }


@app.delete("/address/{address_id}")
def delete_address(
    address_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    address = session.get(Address, address_id)

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found",
        )

    session.delete(address)
    session.commit()

    return {
        "message": f"Address {address_id} deleted successfully"
    }


@app.put("/address/")
def update_all_addresses(
    data: Address,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    addresses = session.exec(
        select(Address)
    ).all()

    if not addresses:
        raise HTTPException(
            status_code=404,
            detail="Addresses not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    remove_protected_fields(update_data)

    for address in addresses:

        for key, value in update_data.items():
            setattr(address, key, value)

        address.updated_at = utc_now()

    session.commit()

    for address in addresses:
        session.refresh(address)

    return addresses


@app.put("/address/{address_id}")
def update_address_by_id(
    address_id: int,
    data: Address,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    address = session.get(Address, address_id)

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Address not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    remove_protected_fields(update_data)

    for key, value in update_data.items():
        setattr(address, key, value)

    address.updated_at = utc_now()

    session.commit()
    session.refresh(address)

    return address


# =========================================================
# ROLECODE
# =========================================================

@app.post("/rolecode")
def create_rolecode(
    rolecode: Rolecode,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    try:
        now = utc_now()

        rolecode.created_at = now
        rolecode.updated_at = now

        session.add(rolecode)
        session.commit()
        session.refresh(rolecode)

        return rolecode

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="RoleCode already exists or violates database constraint",
        )


@app.get("/rolecode")
def get_rolecodes(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    rolecodes = session.exec(
        select(Rolecode)
    ).all()

    return {
        "user": payload,
        "rolecodes": rolecodes,
    }


@app.get("/rolecode/{rolecode_id}")
def get_rolecode_by_id(
    rolecode_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    rolecode = session.get(Rolecode, rolecode_id)

    if not rolecode:
        raise HTTPException(
            status_code=404,
            detail="RoleCode not found",
        )

    return rolecode


@app.delete("/rolecode/")
def delete_all_rolecodes(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    rolecodes = session.exec(
        select(Rolecode)
    ).all()

    for rolecode in rolecodes:
        session.delete(rolecode)

    session.commit()

    return {
        "message": "All rolecodes deleted successfully"
    }


@app.delete("/rolecode/{rolecode_id}")
def delete_rolecode_by_id(
    rolecode_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    rolecode = session.get(Rolecode, rolecode_id)

    if not rolecode:
        raise HTTPException(
            status_code=404,
            detail="RoleCode not found",
        )

    session.delete(rolecode)
    session.commit()

    return {
        "message": f"RoleCode {rolecode_id} deleted successfully"
    }


@app.put("/rolecode/")
def update_all_rolecodes(
    data: Rolecode,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    rolecodes = session.exec(
        select(Rolecode)
    ).all()

    if not rolecodes:
        raise HTTPException(
            status_code=404,
            detail="RoleCodes not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    remove_protected_fields(update_data)

    for rolecode in rolecodes:

        for key, value in update_data.items():
            setattr(rolecode, key, value)

        rolecode.updated_at = utc_now()

    session.commit()

    for rolecode in rolecodes:
        session.refresh(rolecode)

    return rolecodes


@app.put("/rolecode/{rolecode_id}")
def update_rolecode_by_id(
    rolecode_id: int,
    data: Rolecode,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    rolecode = session.get(Rolecode, rolecode_id)

    if not rolecode:
        raise HTTPException(
            status_code=404,
            detail="RoleCode not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    remove_protected_fields(update_data)

    for key, value in update_data.items():
        setattr(rolecode, key, value)

    rolecode.updated_at = utc_now()

    session.commit()
    session.refresh(rolecode)

    return rolecode


# =========================================================
# USERS
# =========================================================

@app.post("/users")
def create_user(
    user: Users,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    try:

        # ---------------------------------------------
        # Duplicate email
        # ---------------------------------------------

        existing_user = session.exec(
            select(Users).where(
                Users.email == user.email
            )
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email is already registered",
            )

        # ---------------------------------------------
        # Address validation
        # ---------------------------------------------

        if user.address_id:

            address = session.get(
                Address,
                user.address_id
            )

            if address is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Address {user.address_id} not found",
                )

        # ---------------------------------------------
        # Role validation
        # ---------------------------------------------

        if user.rolecodes_id:

            role = session.get(
                Rolecode,
                user.rolecodes_id
            )

            if role is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"RoleCode {user.rolecodes_id} not found",
                )

        # ---------------------------------------------
        # Password hash
        # ---------------------------------------------

        if not user.password:
            raise HTTPException(
                status_code=400,
                detail="Password is required",
            )

        user.password = hash_password(
            user.password
        )

        # ---------------------------------------------
        # Timestamps
        # ---------------------------------------------

        now = utc_now()

        user.created_at = now
        user.updated_at = now

        # ---------------------------------------------
        # Save
        # ---------------------------------------------

        session.add(user)
        session.commit()
        session.refresh(user)

        # Never return password
        user.password = None

        return {
            "message": "User created successfully",
            "user": user,
        }

    except HTTPException:
        raise

    except IntegrityError as e:
        session.rollback()

        print("\n========== INTEGRITY ERROR ==========")
        print(str(e))
        print("=====================================\n")

        raise HTTPException(
            status_code=409,
            detail="User could not be created because of a database constraint",
        )

    except Exception as e:
        session.rollback()

        print("\n========== UNEXPECTED ERROR ==========")
        print(repr(e))
        traceback.print_exc()
        print("======================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@app.get("/users")
def get_users(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    users = session.exec(
        select(Users)
    ).all()

    # Remove password from response
    for user in users:
        user.password = None

    return {
        "user": payload,
        "users": users,
    }


@app.get("/users/{users_id}")
def get_user_by_id(
    users_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    user = session.get(Users, users_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    user.password = None

    return user


@app.delete("/users/")
def delete_all_users(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    users = session.exec(
        select(Users)
    ).all()

    for user in users:
        session.delete(user)

    session.commit()

    return {
        "message": "All users deleted successfully"
    }


@app.delete("/users/{users_id}")
def delete_user_by_id(
    users_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    user = session.get(Users, users_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    session.delete(user)
    session.commit()

    return {
        "message": f"User {users_id} deleted successfully"
    }


@app.put("/users/")
def update_all_users(
    data: Users,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    users = session.exec(
        select(Users)
    ).all()

    if not users:
        raise HTTPException(
            status_code=404,
            detail="Users not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    # Never update these through bulk update
    update_data.pop("id", None)
    update_data.pop("password", None)
    update_data.pop("created_at", None)
    update_data.pop("updated_at", None)

    for user in users:

        for key, value in update_data.items():
            setattr(user, key, value)

        user.updated_at = utc_now()

    session.commit()

    for user in users:
        session.refresh(user)
        user.password = None

    return users


@app.put("/users/{users_id}")
def update_user_by_id(
    users_id: int,
    data: Users,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    user = session.get(Users, users_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    update_data.pop("id", None)
    update_data.pop("password", None)
    update_data.pop("created_at", None)
    update_data.pop("updated_at", None)

    for key, value in update_data.items():
        setattr(user, key, value)

    user.updated_at = utc_now()

    session.commit()
    session.refresh(user)

    user.password = None

    return user


# =========================================================
# PERMISSION
# =========================================================

@app.post("/permission")
def create_permission(
    permission: Permission,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    try:

        # Check user
        user = session.get(
            Users,
            permission.users_id
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"User {permission.users_id} not found",
            )

        now = utc_now()

        permission.created_at = now
        permission.updated_at = now

        session.add(permission)
        session.commit()
        session.refresh(permission)

        return {
            "message": "Permission created successfully",
            "data": permission,
        }

    except HTTPException:
        raise

    except IntegrityError:
        session.rollback()

        raise HTTPException(
            status_code=409,
            detail="Permission could not be created",
        )


@app.get("/permission")
def get_permissions(
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    return session.exec(
        select(Permission)
    ).all()


@app.get("/permission/{permission_id}")
def get_permission_by_id(
    permission_id: int,
    payload: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    permission = session.get(
        Permission,
        permission_id
    )

    if not permission:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    return permission


# =========================================================
# LOGIN
# PUBLIC ENDPOINT
# =========================================================

@app.post("/login")
def login(
    data: Login,
    session: Session = Depends(get_session),
):
    email = data.email.strip().lower()

    user = session.exec(
        select(Users).where(
            Users.email == email
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    password_matches = verify_password(
        data.password,
        user.password or "",
    )

    # Legacy plain-text password support
    if not password_matches:

        if data.password != user.password:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password",
            )

    permission = session.exec(
        select(Permission).where(
            Permission.users_id == user.id
        )
    ).first()

    role_id = getattr(
        user,
        "rolecodes_id",
        None
    )

    token = create_access_token({
        "id": user.id,
        "role": role_id,
        "permissions": permission.name if permission else {},
    })

    return {
        "access_token": token,
        "token_type": "Bearer",
    }


# =========================================================
# LOGOUT
# PROTECTED ENDPOINT
# =========================================================

@app.post("/logout")
def logout(
    payload: dict = Depends(verify_token),
):
    return {
        "message": "Logout successful",
        "user_id": payload.get("id"),
    }