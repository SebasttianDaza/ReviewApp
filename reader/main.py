from typing import Union

from fastapi import FastAPI, Request
import socket

app = FastAPI()

@app.get("/api/")
def read_root(request: Request):
    return {"Hello": f"Worlds {socket.gethostname()}"}

