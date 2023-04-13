from fastapi import APIRouter,Depends ,HTTPException, status, Request
from fastapi.responses import JSONResponse

from fastapi.security import OAuth2PasswordBearer

from slowapi import Limiter
from slowapi.util import get_remote_address

from .utils import stock_data, verify_token, decode_token, db

# Create the router
router = APIRouter(
    prefix="/api",
    tags=["api"],
)

# Security for the endpoints 
oauth2 = OAuth2PasswordBearer(tokenUrl="token")

# Create limiter
limiter = Limiter(key_func=get_remote_address)

@router.get("/stock/{symbol}")
@limiter.limit("1/second")
async def stocks(symbol:str,request:Request,token:str = Depends(oauth2)):
    '''Get stock data'''
    # Check token
    if not verify_token(token):
        raise HTTPException(status_code=401,detail="Invalid token")
    
    # Get user data
    user_data = decode_token(token)

    # Check if user is active
    if not db.find_one("users",{"email":user_data["email"]})["active"]:
        raise HTTPException(status_code=401,detail="User not active, please verify your email")

    # Insert record
    db.insert_one("record",{
        "email":user_data["email"],
        "symbol":symbol
    })

    return JSONResponse(stock_data(symbol),status_code=status.HTTP_200_OK)
