
import os

import os
from pathlib import Path
from fastapi import FastAPI,Request
from fastapi_utils.tasks import repeat_every
from app import cronjob

cron_path = Path(os.getcwd(), "app", "cron.log")



app = FastAPI()

@app.on_event("startup")
@repeat_every(seconds=60)  # 1 hour
def remove_expired_tokens_task() -> None:
    cronjob.do_cron()
    # with sessionmaker.context_session() as db:

        
        
    #     remove_expired_tokens(db=db)
@app.get("/")
def health():
    return {"Hello": "World"}
    
@app.get("/headers")
def headers(request:Request):
    return request.headers


@app.get("/cron")
def cron():
    with cron_path.open("rt") as cron:
        return {"cron_state": cron.read().split("\n")}
import pandas as pd

pd.concat()