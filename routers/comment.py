from datetime import datetime
from fastapi import APIRouter, Depends, status, Form, HTTPException
from sqlalchemy.orm import Session
from schemas.article import ArticleCommentSchema
from models.Articles.ArticleComment import ArticleComment
from models.User import User
from database import get_db
from fastapi import File, UploadFile
from typing import List
from utils.get_current_user import get_current_user
from .article import get_article


comment_router = APIRouter(tags=["Comments"])


def get_comment(id:str, db:Session) -> ArticleComment:
    comment = db.query(ArticleComment).filter(ArticleComment.id == id).first()
    if not comment: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Non esiste un commento con questo id")
    return comment


@comment_router.get(
    path="/article/{article_slug}/comments", 
    status_code=status.HTTP_200_OK, 
    response_model=List[ArticleCommentSchema]
)
def comment_list(article_slug: str,
                 db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    article = get_article(article_slug, db)
    
    comments = db.query(ArticleComment).filter(ArticleComment.article_id == article.id).order_by(ArticleComment.updated_at).all()
    
    return comments

@comment_router.post(
    path="/article/{article_slug}/comments", 
    status_code=status.HTTP_201_CREATED, 
    response_model=ArticleCommentSchema
)
def comment_create(comment: ArticleCommentSchema,
                  article_slug: str,
                  db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    article = get_article(article_slug, db)
    
    comment = ArticleComment(comment.content, user.id, article.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return comment


@comment_router.patch(
    path="/article/comment/{comment_id}", 
    status_code=status.HTTP_200_OK, 
    response_model=ArticleCommentSchema
)
def comment_update(new_comment: ArticleCommentSchema,
                  comment_id: str,
                  db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    comment = get_comment(comment_id, db)
    
    if user.id != comment.author_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Soltato il creatore del commento può modificarlo")
    
    if comment.content: comment.content = new_comment.content
    
    db.commit()
    db.refresh(comment)
    
    return comment


@comment_router.delete(
    path="/article/comment/{comment_id}", 
    status_code=status.HTTP_204_NO_CONTENT, 
)
def comment_delete(comment_id: str,
                   db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    comment = get_comment(comment_id, db)
    
    if user.id != comment.author_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Soltato il creatore del commento può eliminarlo")
    
    db.delete(comment)
    db.commit()
    
    return {"msg": "Commento eliminato"}