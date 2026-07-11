from fastapi import FastAPI, Request
from app.exceptions import AppException
from fastapi.responses import JSONResponse
from app.api import auth_router


app = FastAPI()

@app.exception_handler(AppException)
async def handle_app_exc(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message}
    )

app.include_router(auth_router)

