from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional, List


class ArticleParagraphImage(BaseModel):
    image: str
    caption: str | None = None
    
    class Config:
        orm_mode = True


class ArticleParagraph(BaseModel):
    title: str
    content: str
    images: List[ArticleParagraphImage] = []
    
    class Config:
        orm_mode = True


class AuthorSchema(BaseModel):
    id: UUID4
    email: EmailStr
    image: str | None = None
    
    class Config:
        orm_mode = True


class ArticleSchema(BaseModel):
    title: str
    intro: str
    image: str | None = None
    updated_at: datetime
    author: AuthorSchema
    slug: str
    paragraphs: List[ArticleParagraphImage] = []
    
    class Config:
        orm_mode = True
    