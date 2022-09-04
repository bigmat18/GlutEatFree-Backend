from sqlalchemy.orm import relationship
from fastapi import Depends
from database import Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from database import SessionLocal
from .ArticleParagraphImage import ArticleParagraphImage
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
    
    def __init__(self, title, content, article_id) -> None:
        self.title = title,
        self.content = content
        self.article_id = article_id
    
    @hybrid_property
    def images(self):
        db = SessionLocal()
        return db.query(ArticleParagraphImage).filter(ArticleParagraphImage.paragraph_id == self.id).all()