from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from mongoengine import connect
from fastapi.responses import JSONResponse

from .models import JSONAPIResponse
from .routers.reviews import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from .config import get_settings
    from pymongo import monitoring
    from .logger import CommandLogger

    monitoring.register(CommandLogger())
    connect(
        db="reader",
        host=get_settings().mongo_uri,
    )
    yield
    # Optional: Disconnect from MongoDB on shutdown
    # disconnect()
    print("MongoDB disconnected.")


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api/v1")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == status.HTTP_404_NOT_FOUND:
        return JSONResponse(
            status_code=404,
            content=JSONAPIResponse(
                links={
                    "self": str(request.url)
                },
                data=None
            )
        )
    return JSONResponse(
        status_code=exc.status_code,
        content=JSONAPIResponse(
            links={
                "self": str(request.url)
            },
            data=None
        )
    )

@app.get("/")
def read_root(request: Request):
    import socket
    return {"Hello": f"Worlds {socket.gethostname()}"}


