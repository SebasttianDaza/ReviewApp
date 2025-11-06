import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from .models import ReaderReview
from mongoengine import connect

@asynccontextmanager
async def lifespan(app: FastAPI):
    from .config import get_settings
    connect(
        host=get_settings().mongo_uri,
    )
    yield
    # Optional: Disconnect from MongoDB on shutdown
    # disconnect()
    print("MongoDB disconnected.")


app = FastAPI(lifespan=lifespan)

@app.get("/api/")
def read_root(request: Request):
    import socket
    ReaderReview(
        title="Hello there",
        subtitle="This is the subtitle",
        date_created=datetime.datetime.now,
        date_updated=datetime.datetime.now
    ).save()
    return {"Hello": f"Worlds {socket.gethostname()}"}

