from fastapi import APIRouter,Depends ,HTTPException, status
from fastapi.responses import JSONResponse

from fastapi.security import OAuth2PasswordBearer

from .utils import stock_data, verify_token

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

oauth2 = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/stock/{symbol}")
async def stocks(symbol:str,token:str = Depends(oauth2)):
    '''Get stock data'''
    
    # Check token
    if not verify_token(token):
        raise HTTPException(status_code=401,detail="Invalid token")

    return stock_data(symbol)


