
import os


from fastapi import FastAPI
from fastapi import Request
DATAPATH = os.getenv("DIRECTORY","/media/external/data")

app = FastAPI()

@app.get("/")
def health():
    return {"Hello": "World"}
@app.get("/headers")
def headers(request:Request):
    return request.headers