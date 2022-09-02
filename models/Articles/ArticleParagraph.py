from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ArticleParagraph(Base):
    __tablename__ = "article_paragraph"
    
    id = Column(UUID(as_uuid=True), 
                default=uuid.uuid4, 
                primary_key=True)
    
    title = Column(String)
    content = Column(String)
    
    article_id = Column(UUID(as_uuid=True), 
                        ForeignKey("article.id", 
                                   ondelete="CASCADE"))
    
    article = relationship("Article")