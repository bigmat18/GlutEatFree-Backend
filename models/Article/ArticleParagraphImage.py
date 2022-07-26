from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ArticleParagraphImage(Base):
    __tablename__ = "article_paragraph_image"
    
    id = Column(UUID(as_uuid=True), 
                default=uuid.uuid4, 
                primary_key=True)
    
    image = Column(String)
    caption = Column(String, nullable=True)
    
    paragraph_id = Column(UUID(as_uuid=True), 
                          ForeignKey("article_paragraph.id", 
                                     ondelete="CASCADE"))
    
    paragraph = relationship("ArticleParagraph")