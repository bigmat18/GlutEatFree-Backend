from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas.article import ArticleTagSchema
from models.User import User
from models.Articles.ArticleTag import ArticleTag
from database import get_db
from utils.get_current_user import get_current_user
from typing import List
from models.Account import TypeAccount


def check_user_has_permissions(user: User) -> bool:
    if user.type_account != TypeAccount.ADMIN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Solo un utente admin può eseguire questa operazione")
    return True


tag_rounter = APIRouter(tags=["ArticleTag"])

@tag_rounter.get(path="/tags",
                 status_code=status.HTTP_200_OK,
                 response_model=List[ArticleTagSchema])
def tag_list(db: Session = Depends(get_db),
             user: User = Depends(get_current_user)):
    tags = db.query(ArticleTag).all()
    return tags



@tag_rounter.post(path="/tags",
                  status_code=status.HTTP_201_CREATED,
                  response_model=ArticleTagSchema)
def tag_create(tag: ArticleTagSchema,
               db: Session = Depends(get_db),
               user: User = Depends(get_current_user)):
    check_user_has_permissions(user)
    
    tag = ArticleTag(tag.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    
    return tag
    


@tag_rounter.delete(path="/tag/{tag_id}",status_code=status.HTTP_204_NO_CONTENT)
def tag_delete(tag_id: str,
               db: Session = Depends(get_db),
               user: User = Depends(get_current_user)):
    check_user_has_permissions(user)

    tag = db.query(ArticleTag).filter(ArticleTag.id == tag_id).first()
    
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Non esiste un tag con questo id")
        
    db.delete(tag)
    db.commit()
    
    return {"msg": "tag eliminato"}



@tag_rounter.patch(path="/tag/{tag_id}",
                   status_code=status.HTTP_200_OK, 
                   response_model=ArticleTagSchema)
def tag_update(tag_id: str,
               new_tag: ArticleTagSchema,
               db: Session = Depends(get_db),
               user: User = Depends(get_current_user)):
    check_user_has_permissions(user)
    
    tag = db.query(ArticleTag).filter(ArticleTag.id == tag_id).first()
    
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Non esiste un tag con questo id")
        
    tag.name = new_tag.name
    
    db.commit()
    db.refresh(tag)
    
    return tag