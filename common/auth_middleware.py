from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from jose import jwt, JWTError

SECRET_KEY = "priyanshu"
ALGORITHM = "HS256"

PUBLIC_ROUTES = [
    "/docs",
    "/openapi.json",
    "/redoc",
    "/login",
    "/users",      
    "/logout"      
]
# Route ke liye required permission
ROUTE_PERMISSIONS = {
    "/users": "is_admin",
    "/dashboard" : "is_dashboard",
    "/orders": "is_order",
    "/address": "is_admin",
}


class JWTMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        path = request.url.path
        #gets only url path
        # Public routes
        for route in PUBLIC_ROUTES:
            if path.startswith(route):
                return await call_next(request)

        auth = request.headers.get("Authorization")
        #Get the Authorization header
        if not auth:
           # Check if the header is missing
            return JSONResponse(
                status_code=401,
                content={"detail": "Token Missing"}
            )

        if not auth.startswith("Bearer"):
           # Check the header format
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid Authorization Header"}
            )

        try:
            token = auth.split(" ")[1]
            #It divides the string wherever there is a space.
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )

            request.state.user = payload

            # Permission check
            required_permission = ROUTE_PERMISSIONS.get(path)

            if required_permission:

                permissions = payload.get("permissions", {})

                allowed = permissions.get(required_permission)

                if allowed != "True":
                    return JSONResponse(
                        status_code=403,
                        content={
                            "detail": "Permission Denied"
                        }
                    )

        except JWTError as e:
            print("JWT ERROR:", e)

            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid Token"}
            )

        return await call_next(request)