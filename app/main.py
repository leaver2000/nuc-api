
import os

from fastapi import FastAPI,Request
import os
from pathlib import Path

cron_path = Path(os.getcwd(), "app", "cron.log")

DATAPATH = os.getenv("DIRECTORY","/media/external/data")

app = FastAPI()

@app.get("/")
def health():
    return {"Hello": "World"}
    
@app.get("/headers")
def headers(request:Request):
    return request.headers


@app.get("/cron")
def cron():
    with cron_path.open("rt") as cron:
        return {"cron_state": cron.read()}
