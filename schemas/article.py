from pydantic import BaseModel, EmailStr
from typing import Optional

class ArticleParagraphImage(BaseModel):
    pass


class ArticleParagraph(BaseModel):
    pass


class ArticleSchema(BaseModel):
    title: str
    intro: str
    image: bytes | None
    