from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
    

class AuthenticationSchema(BaseModel):
    access_token: str
    refresh_token: str