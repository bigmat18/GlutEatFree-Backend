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
    
    def __init__(self, image, paragraph_id, caption=None):
        self.image = image
        self.caption = caption
        self.paragraph_id = paragraph_id