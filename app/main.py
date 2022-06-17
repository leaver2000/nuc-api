
from datetime import datetime

from requests import Session
from fastapi import FastAPI,Request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.extract import fetch, ApacheDir, tomorrow


scheduler = BackgroundScheduler()

app = FastAPI()
class Cache:
    def __init__(self):
        self._state = {}
    
    def __repr__(self) -> str:
        return self.__class__.__name__+"({0})".format(" ".join(f"{k}={v}"for k, v in self.state.items()) )
        
    @property
    def state(self):
        return self._state
        
    def set_state(self, state:dict):
        self._state= state


cache = Cache()        


@app.on_event("startup")
def startup() -> None:
    scheduler.start()

@app.on_event("shutdown")
def shutdown() -> None:
    scheduler.shutdown()

        
@app.get("/")
def health():
    return {"Hello": "World"}
    
@app.get("/headers")
def headers(request:Request):
    return request.headers





@scheduler.scheduled_job(IntervalTrigger(seconds=10, start_date=tomorrow(), timezone="utc"))
def on_newday():
    target_day =datetime.utcnow().day

    with Session() as session:
        ragr = ApacheDir(session, url="https://nomads.ncep.noaa.gov/pub/data")
        cache.set_state({
            "557ww":fetch.galwem(ragr, target_day),
            "hrrr":fetch.hrrr(ragr, target_day)
            })
    

