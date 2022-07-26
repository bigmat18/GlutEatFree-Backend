from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.Account import Account
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db, Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)