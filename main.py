from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path

from routers import users,api,logs

# Create the FastAPI app
app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(api.router)
app.include_router(logs.router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root(request : Request):
    '''This is the root path of the API.'''
    return {"Reply": "Stock Market API Service"}


