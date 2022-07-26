from email.policy import default
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ArticlesUsersLike(Base):
    __tablename__ = "articles_users_like"
    
    user_id = Column(UUID(as_uuid=True), 
                     ForeignKey("user.id", 
                                ondelete="CASCADE"), 
                     primary_key=True)
    
    article_id = Column(UUID(as_uuid=True), 
                        ForeignKey("article.id", 
                                   ondelete="CASCADE"),
                        primary_key=True)
    
    date_like = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'))
    
    
class ArticlesTags(Base):
    __tablename__ = "articles_tags"
    
    tag_id = Column(UUID(as_uuid=True), 
                     ForeignKey("tag.id", 
                                ondelete="CASCADE"), 
                     primary_key=True)
    
    article_id = Column(UUID(as_uuid=True), 
                        ForeignKey("article.id", 
                                   ondelete="CASCADE"),
                        primary_key=True)


class Article(Base):
    __tablename__ = "article"
    
    id = Column(UUID(as_uuid=True), 
                default=uuid.uuid4, 
                primary_key=True)
    
    title = Column(String(64))
    intro = Column(String)
    image = Column(String)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    
    author_id = Column(UUID(as_uuid=True), 
                       default=uuid.uuid4, 
                       primary_key=True)
    
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    
    tags = relationship("ArticlesTags")
    likes = relationship("ArticlesUsersLike")