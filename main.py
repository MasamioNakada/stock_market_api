from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import users,api

app = FastAPI()

app.include_router(users.router)
app.include_router(api.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    '''This is the root path of the API.'''
    return {"Reply": "Stock Market API Service"}


