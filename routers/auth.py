from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy.orm import Session
from schemas.auth import LoginSchema, RegistrationSchema
from models.User import User
from database import get_db
from fastapi_jwt_auth import AuthJWT
from utils.get_current_user import get_current_user
import datetime


auth_router = APIRouter(tags=['Authentication'])


@auth_router.post('/login', status_code=status.HTTP_200_OK)
def login(credentials: LoginSchema, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    
    # check if user exists
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"La mail {credentials.email} è errata")
        
    # check if password is correct
    if user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"La password è errata")
        
    # update last login and save
    user.last_login = datetime.datetime.now()
    user.access_revoked = False
    db.commit()
    
    # generate new tokens
    access = Authorize.create_access_token(subject=str(user.id))
    refresh = Authorize.create_refresh_token(subject=str(user.id))
    return {"access_token": access, "refresh_token": refresh}



@auth_router.post('/registration', status_code=status.HTTP_201_CREATED)
def registration(credentials: RegistrationSchema,
                 db: Session = Depends(get_db), 
                 Authorize: AuthJWT = Depends()):
    
    # check if user altredy exists
    if db.query(User).filter(User.email == credentials.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"La mail {credentials.email} è usata da un altro utente")
    
    # create and save user
    user = User(**credentials.dict())
    user.last_login = datetime.datetime.now()
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # generate tokens
    access = Authorize.create_access_token(subject=str(user.id))
    refresh = Authorize.create_refresh_token(subject=str(user.id))
    return {"access_token": access, "refresh_token": refresh}
    


@auth_router.get('/logout', status_code=status.HTTP_200_OK)
def logout(db: Session = Depends(get_db),
           user: User = Depends(get_current_user)):
    # set user logged out and save
    user.access_revoked = True
    db.commit()
    return {"msg": "Logout sucessfull"}


@auth_router.get('/token/refresh', status_code=status.HTTP_200_OK)
def refresh_token(Authorize: AuthJWT = Depends()):
    # verify refresh token
    Authorize.jwt_refresh_token_required()
    
    # get user_id and create new access token
    user_id = Authorize.get_jwt_subject()
    access = Authorize.create_access_token(subject=str(user_id))
    return {"access_token": access}