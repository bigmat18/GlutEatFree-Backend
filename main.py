from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, SessionLocal, engine
from routers.auth import router
from models.User import User

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel


Base.metadata.create_all(bind=engine)
app = FastAPI()

# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

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