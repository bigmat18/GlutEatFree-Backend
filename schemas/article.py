from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4
from typing import List


class ArticleParagraphImageSchema(BaseModel):
    id: UUID4
    image: str
    caption: str | None = None
    
    class Config:
        orm_mode = True


class ArticleParagraphSchema(BaseModel):
    id: UUID4
    title: str
    content: str
    images: List[ArticleParagraphImageSchema] = []
    
    class Config:
        orm_mode = True


class AuthorSchema(BaseModel):
    id: UUID4
    email: EmailStr
    image: str | None = None
    
    class Config:
        orm_mode = True


class ArticleCommentSchema(BaseModel):
    id: UUID4 | None = None
    author: AuthorSchema | None = None
    content: str
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class ArticleSchema(BaseModel):
    title: str
    intro: str
    image: str | None = None
    updated_at: datetime
    author: AuthorSchema
    slug: str
    paragraphs: List[ArticleParagraphSchema] = []
    likes: int
    
    class Config:
        orm_mode = True
    