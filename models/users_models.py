from pydantic import BaseModel , Field

class User(BaseModel):
    full_name : str = Field(...,min_length=3,max_length=50)
    email : str = Field(...,min_length=3,max_length=50)
    password : str = Field(...,min_length=8,max_length=50)

