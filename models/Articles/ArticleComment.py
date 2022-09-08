from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ArticleComment(Base):
    __tablename__ = "article_comment"
    
    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    content = Column(String)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.account_id", ondelete="CASCADE"))
    article_id = Column(UUID(as_uuid=True), ForeignKey("article.id", ondelete="CASCADE"))
    
    author = relationship("User")
    article = relationship("Article")
    
    def __init__(self, content, author_id, article_id):
        self.content = content
        self.author_id = author_id
        self.article_id = article_id