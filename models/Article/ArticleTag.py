from database import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ArticleTag(Base):
    __tablename__ = "article_tag"
    
    id = Column(UUID(as_uuid=True), 
                dafault=uuid.uuid4,
                primary_key=True)
    
    name = Column(String(64))