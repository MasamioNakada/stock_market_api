from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path

from routers import users,api,logs


app = FastAPI()
app.include_router(users.router)
app.include_router(api.router)
app.include_router(logs.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root(request : Request):
    '''This is the root path of the API.'''
    return {"Reply": "Stock Market API Service"}


