from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

class User(Base):
    __tablename__ = "user"
    
    account_id = Column(UUID(as_uuid=True), 
                        ForeignKey("account.id", 
                                   ondelete="CASCADE"), 
                        primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    image = Column(String)
    
    account = relationship("Account")
    
    
    