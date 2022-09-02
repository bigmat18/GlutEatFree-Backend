from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from .ArticleTag import ArticleTag
from utils.generate_slug import generate_slug
import uuid


class ArticlesUsersLike(Base):
    __tablename__ = "articles_users_like"
    
    user_id = Column(UUID(as_uuid=True), 
                     ForeignKey("user.account_id", 
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
                     ForeignKey("article_tag.id", 
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
    image = Column(String, nullable=True)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'))
    
    author_id = Column(UUID(as_uuid=True), 
                       ForeignKey("user.account_id", 
                                  ondelete="CASCADE"),)
    
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    
    slug = Column(String, unique=True)
    
    tags = relationship("ArticlesTags")
    likes = relationship("ArticlesUsersLike")
    author = relationship("User")
    
    __table_args__ = (UniqueConstraint('slug', name='slug_unique_constraint'),)
    
    def __init__(self, title, intro, author_id, image=None):
        self.title = title
        self.intro = intro
        self.author_id = author_id
        self.set_slug(self.title)
        
    def set_slug(self, title):
        if not self.slug: 
            self.slug = generate_slug(title)
        else:
            slug_split = self.slug.split("-")
            self.slug = f"{title}-{slug_split[1]}"