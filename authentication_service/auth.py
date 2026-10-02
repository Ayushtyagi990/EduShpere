from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET_KEY = "priyanshu"
ALGORITHM = "HS256"

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    print("AUTH HEADER RECEIVED:", credentials)

    token = credentials.credentials

    print("TOKEN:", token)

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("JWT PAYLOAD:", payload)

        return payload

    except JWTError as e:
        print("JWT ERROR:", e)
        raise HTTPException(
            
            status_code=401,
            detail="Invalid Token"
        )