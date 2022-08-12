from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas.auth import LoginSchema, RegistrationSchema
from models.User import User
from database import get_db
from fastapi_jwt_auth import AuthJWT
from utils.get_current_user import get_current_user
import datetime

