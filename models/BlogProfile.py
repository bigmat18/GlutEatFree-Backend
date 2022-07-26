from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

class BlogProfile(Base):
    __tablename__ = "blog_profile"
    
    user_id = Column(UUID(as_uuid=True), 
                  ForeignKey("user.account_id", 
                             ondelete="CASCADE"), 
                  primary_key=True)
    
    instagram_link = Column(String)
    facebook_link = Column(String)
    linkedin_link = Column(String)
    link_site = Column(String)
    
    phone_number = Column(String(10))
    presetation = Column(String)
    
    user = relationship('User')