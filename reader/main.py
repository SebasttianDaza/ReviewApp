from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from mongoengine import connect
from fastapi.responses import JSONResponse
from .schemas.jsonapi import JSONAPIResponse
from .routers.reviews import router


INDEX_NAME = "review_idx"
CACHE_PREFIX = "review"

def create_initial_index():
    from reader.dependencies.redis_connector import get_redis_connection
    from reader.repositories.cache_repository import CacheRepository

    try:
        master_conn, _ = get_redis_connection()
        repo = CacheRepository(master_conn, master_conn)
        repo.create_search_index(INDEX_NAME, CACHE_PREFIX)
        print("Index search ready")
    except ConnectionError as e:
        print(f"Connection critic to redis: {e}")


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
    create_initial_index()
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


