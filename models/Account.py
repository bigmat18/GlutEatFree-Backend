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
    password = Column(String)
    email = Column(String)
    type_account = Column(Enum(TypeAccount))
    