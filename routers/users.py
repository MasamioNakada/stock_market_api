from fastapi import APIRouter,Depends ,HTTPException, status

from fastapi.security import HTTPBasic, HTTPBasicCredentials,OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from models.users_models import User

from .utils import email_exists_db, db, encrypt_password, verify_password, generate_access_token, decode_token

# Create the router
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# Security for the endpoints Basic and OAuth2
security = HTTPBasic()
oauth2 = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/create_user")
async def create_user(user: User):
    '''Create a new user'''

    # Check if email already exists
    if email_exists_db(user.email):
        raise HTTPException(status_code=400,detail="Email already exists")
    
    # Create user
    r = db.insert_one(
        collection="users",
        data={
            "full_name":user.full_name,
            "email":user.email,
            "password":encrypt_password(user.password),
            "active":True ## For testing purposes (If you want to test the email verification, change this to False) Email Verification endpoint: /users/check_email/{token}
        }
    )

    # Generate access token
    token_data = generate_access_token(
        sub=str(r.inserted_id),
        email=user.email
    )

    # Response
    res = {
        "access_token": token_data.get("access_token"),
        "token_type": "bearer",
        "expires_in": token_data.get("exp")
    }

    return JSONResponse(
        content=res,
        status_code=status.HTTP_201_CREATED
    )


@router.get("/get_access_token")
async def get_access_token(credentials: HTTPBasicCredentials = Depends(security)):
    '''Get access token'''

    # Check correct Credentials
    if not verify_password(credentials.username,credentials.password):
        raise HTTPException(status_code=401,detail="Incorrect email or password")
    
    # Get user
    user = db.find_one("users",{"email":credentials.username})

    # Generate access token
    token = generate_access_token(
        sub=str(user["_id"]),
        email=user["email"]
    )

    # Response
    res = {
        "access_token": token.get("access_token"),
        "token_type": "bearer",
        "expires_in": token.get("exp")
    }

    return JSONResponse(
        content=res,
        status_code=status.HTTP_200_OK
    )    

@router.get("/check_email/{token}")
async def check_email(token:str):
    '''Check email and activate user to prevent spam'''

    # Decode token and get user data
    user_data = decode_token(token)
    
    # Update user to active
    db.update_one("users",{"email":user_data["email"]},{"active":True})
    
    return JSONResponse(
        content={"message":"User Activate"},
        status_code=status.HTTP_200_OK
    )