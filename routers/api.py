from fastapi import APIRouter,Depends ,HTTPException, status, Request
from fastapi.responses import JSONResponse

from fastapi.security import OAuth2PasswordBearer

from slowapi import Limiter
from slowapi.util import get_remote_address

from .utils import stock_data, verify_token, decode_token, db

limiter = Limiter(key_func=get_remote_address)



router = APIRouter(
    prefix="/api",
    tags=["api"],
)

oauth2 = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/stock/{symbol}")
@limiter.limit("1/second")
async def stocks(symbol:str,request:Request,token:str = Depends(oauth2)):
    '''Get stock data'''
    # Check token
    if not verify_token(token):
        raise HTTPException(status_code=401,detail="Invalid token")
    
    user_data = decode_token(token)

    if not db.find_one("users",{"email":user_data["email"]})["active"]:
        raise HTTPException(status_code=401,detail="User not active, please verify your email")

    # Insert record
    db.insert_one("record",{
        "email":user_data["email"],
        "symbol":symbol
    })

    return JSONResponse(stock_data(symbol),status_code=status.HTTP_200_OK)
