from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers.auth import router
from models.User import User
from database import get_db, Base, SessionLocal

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

db = SessionLocal()
if not db.query(User).filter(User.email == "admin@admin.com").first():
    user = User("admin123456", "admin@admin.com", "admin", "admin", type_account="ADMIN")
    db.add(user)
    db.commit()
    db.refresh(user)