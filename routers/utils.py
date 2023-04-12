from mongodb.mongo import MongoDb

from env import *

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import requests

# mongo db connection
db = MongoDb(
    url_conection=URL_MONGO,
    database="stock-market-service"
)

# password encryption
crypt = CryptContext(schemes=[ENCRYPT])

def email_exists_db(email:str) -> bool:
    '''Check if email exists in database'''
    if db.find_one("users",{"email":email}) != None:
        return True
    return False

def encrypt_password(password:str) -> str:
    '''Encrypt password'''
    return crypt.hash(password)

def verify_password(email:str,password:str) -> bool:
    '''Verify password'''
    user = db.find_one("users",{"email":email})
    if user:
        return crypt.verify(password,user["password"])
    return False

def verify_token(token:str) -> bool:
    '''Verify token'''
    try:
        jwt.decode(token,SEED,algorithms=[ALGORITHM])
        return True
    except:
        return False

def generate_access_token(sub:str,email:str,exp_days:int = 45 ) -> dict:
    '''Generate access token'''

    # Expiration time
    expire = datetime.utcnow() + timedelta(days=45)

    # Create access token Fields
    access_token_fields = {
        "sub": sub,
        "email": email,
        "exp":expire
    }

    # Create access token with jwt
    access_token = jwt.encode(
        access_token_fields,
        SEED,
        algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "exp": expire.strftime("%Y-%m-%d %H:%M:%S")
    }

def stock_data(symbol:str)->dict:
    '''Get stock data'''

    now = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    #Define params
    params = {
        "function":"TIME_SERIES_DAILY_ADJUSTED",
        "symbol":symbol,
        "outputsize":"compact",
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    full_data = requests.get(ALPHA_URL,params=params).json()["Time Series (Daily)"]
    now_data = full_data[now]
    yesterday_close = full_data[yesterday]["4. close"]

    # Response
    res = {
        "symbol":symbol,
        "open":now_data["1. open"],
        "high":now_data["2. high"],
        "low":now_data["3. low"],
        "variation":str(float(now_data["4. close"]) - float(yesterday_close))
    }

    return res


