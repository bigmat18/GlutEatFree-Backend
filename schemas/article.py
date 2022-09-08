from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4
from typing import List, Union


class ArticleParagraphImageSchema(BaseModel):
    id: UUID4
    image: str
    caption: Union[str, None] = None
    
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
    image: Union[str, None] = None
    
    class Config:
        orm_mode = True


class ArticleCommentSchema(BaseModel):
    id: Union[UUID4, None] = None
    author: Union[AuthorSchema, None] = None
    content: str
    updated_at: Union[datetime, None] = None

    class Config:
        orm_mode = True


class ArticleSchema(BaseModel):
    title: str
    intro: str
    image: Union[str, None] = None
    updated_at: datetime
    author: AuthorSchema
    slug: str
    paragraphs: List[ArticleParagraphSchema] = []
    likes: int
    
    class Config:
        orm_mode = True
    