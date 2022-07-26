from datetime import datetime
from fastapi import APIRouter, Depends, status, Form, HTTPException
from sqlalchemy.orm import Session
from schemas.article import ArticleSchema
from models.User import User
from models.Articles.Article import Article, ArticlesUsersLike
from database import get_db
from fastapi import File, UploadFile
from utils.get_current_user import get_current_user
from typing import List, Optional
from pydantic import constr
from utils.file_manager import upload_file, delete_file, AWS_BUCKET_URL
from sqlalchemy import and_


article_router = APIRouter(tags=["Article"])

def get_article(slug: str, db: Session) -> Article:
    article = db.query(Article).filter(Article.slug == slug).first()
    if not article: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Lo slug non esiste")
    return article


def check_user_has_permissions(user: User, article: Article):
    if article.author_id != user.id and user.type_account != "ADMIN":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Soltato l'autore o un admin può elimiare l'articolo")


@article_router.post(
    path="/articles", 
    status_code=status.HTTP_201_CREATED, 
    response_model=ArticleSchema,
    response_model_exclude={"paragraphs"}
)
def article_create(title: Optional[constr(max_length=64)] = Form(), intro: str = Form(), 
                   image: UploadFile = File(default=None), db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    
    # Creation of article
    article = Article(title=title, intro=intro, author_id=user.id)
    db.add(article)
    db.commit()
    db.refresh(article)

    # If you send image save it
    if image:
        url = upload_file(image.file, f"/article-{article.id}", "article-images")
        article.image = url
        db.commit()
        db.refresh(article)
        
    # Return article
    return article


@article_router.get(
    path="/articles", 
    status_code=status.HTTP_200_OK, 
    response_model=List[ArticleSchema],
    response_model_exclude={"paragraphs"}
)
def article_list(db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)):
    articles = db.query(Article).all()
    return articles



@article_router.get(path="/article/{article_slug}", status_code=status.HTTP_200_OK, response_model=ArticleSchema)
def article_retrieve(article_slug: str,
                     db: Session = Depends(get_db)):
    return get_article(article_slug, db)



@article_router.patch(path="/article/{article_slug}", status_code=status.HTTP_200_OK, response_model=ArticleSchema)
def article_update(article_slug: str, title: Optional[constr(max_length=64)] = Form(default=None), 
                   intro: str = Form(default=None), image: UploadFile = File(default=None),
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    article = get_article(article_slug, db)
    
    # Check if user is author or admin user
    check_user_has_permissions(user, article)
    
    # aply changes to article
    if title: 
        article.title = title
        article.set_slug(title)
        article.update_at = datetime.now()
        
    if intro: 
        article.intro = intro
        article.update_at = datetime.now()
        
    if image:
        article.image = upload_file(image.file, f"/article-{article.id}", "article-images")
        article.update_at = datetime.now()
        db.commit()
        db.refresh(article)
        
    # update object in db
    db.commit()
    db.refresh(article)
    return article
    

@article_router.delete(path="/article/{article_slug}", status_code=status.HTTP_204_NO_CONTENT)
def article_delete(article_slug: str, db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    article = get_article(article_slug, db)
    
    # Check if user is author or admin user
    check_user_has_permissions(user, article)
        
    # Delete image in bucket
    if article.image:
        path = article.image.replace(AWS_BUCKET_URL + "/", '')
        delete_file(path)
        
    # delete object in db
    db.delete(article)
    db.commit()
    return {"msg": "Articolo eliminato"}


@article_router.post(path="/article/{article_slug}/likes", status_code=status.HTTP_201_CREATED)
def article_like_create(article_slug: str, db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    article = get_article(article_slug, db)
    
    if db.query(ArticlesUsersLike)\
         .filter(and_(ArticlesUsersLike.article_id == article.id, ArticlesUsersLike.user_id == user.id))\
         .first():
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="Like già inserito da questo utente")
    
    like = ArticlesUsersLike(user_id=user.id, article_id=article.id)
    db.add(like)
    db.commit()
    db.refresh(like)
    
    return {"msg": "Like aggiunto"}


@article_router.delete(path="/article/{article_slug}/likes", status_code=status.HTTP_204_NO_CONTENT)
def article_like_delete(article_slug: str, db: Session = Depends(get_db),
                        user: User = Depends(get_current_user)):
    article = get_article(article_slug, db)
    
    like = db.query(ArticlesUsersLike)\
         .filter(and_(ArticlesUsersLike.article_id == article.id, ArticlesUsersLike.user_id == user.id))\
         .first()

    if not like: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                     detail="Like non esistente") 
    
    db.delete(like)
    db.commit()
    
    return {"msg": "Like rimosso"}