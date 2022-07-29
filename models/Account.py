from email.policy import default
from sqlalchemy.sql.expression import text
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid, enum

class TypeAccount(enum.Enum):
    STANDARD = 1
    BLOGGER = 2
    ADMIN = 3

class Account(Base):
    __tablename__ = "account"
    
    id = Column(UUID(as_uuid=True), 
                primary_key=True, 
                default=uuid.uuid4)
    
    date_joined = Column(TIMESTAMP(timezone=True),
                         server_default=text('now()'))
    last_login = Column(TIMESTAMP(timezone=True),
                        nullable=True)
    
    password = Column(String(64))
    email = Column(String(64),unique=True)
    type_account = Column(Enum(TypeAccount), default=TypeAccount.STANDARD)
    
    __mapper_args__ = {
        "polymorphic_identity": "account"
    }
    
    def __init__(self, password, email, type_account=None):
        self.password = password
        self.email = email
        if type_account: self.type_account = type_account