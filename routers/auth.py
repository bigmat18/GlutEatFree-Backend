from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy.orm import Session
from schemas.auth import LoginSchema, RegistrationSchema
from models.User import User
from database import get_db
from oauth2 import create_access_token
import datetime

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(credentials: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"La mail {credentials.email} è errata")
        
    if user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"La password è errata")
    user.last_login = datetime.datetime.now()
    db.commit()
    token = create_access_token(data={"id": str(user.id)})
    return {"access_token": token}


@router.post('/registration', response_model=RegistrationSchema)
def registration(credentials: RegistrationSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == credentials.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"La mail {credentials.email} è usata da un altro utente")
    
    user = User(**credentials.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
    


@router.post('/logout')
def logout():
    pass