from pydantic import BaseModel, EmailStr,constr
from typing import Optional
from fastapi import File, UploadFile


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    
class RegistrationSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[constr(max_length=64)]
    last_name: Optional[constr(max_length=64)]