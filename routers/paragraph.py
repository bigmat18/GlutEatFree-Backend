from tkinter.messagebox import RETRY
from fastapi import APIRouter, Depends, status, Form, HTTPException
from sqlalchemy.orm import Session
from schemas.article import ArticleParagraphSchema, ArticleParagraphImageSchema
from models.User import User
from models.Articles.ArticleParagraph import ArticleParagraph
from models.Articles.ArticleParagraphImage import ArticleParagraphImage
from database import get_db
from fastapi import File, UploadFile
from utils.get_current_user import get_current_user
from typing import List, Optional
from utils.file_manager import delete_file, upload_file, AWS_BUCKET_URL
from .article import get_article


paragraph_router = APIRouter(tags=["Paragraph"])

def get_paragraph(id: str, db: Session):
    paragraph = db.query(ArticleParagraph).filter(ArticleParagraph.id == id).first()
    if not paragraph:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Non esiste un paragrafo con questo id")
    return paragraph


def get_paragraph_image(id: str, db: Session):
    image = db.query(ArticleParagraphImage).filter(ArticleParagraphImage.id == id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Non esiste un immagie con questo id")
    return image


@paragraph_router.post(path="/article/{article_slug}/paragraphs", status_code=status.HTTP_201_CREATED, response_model=ArticleParagraphSchema)
def paragraph_create(article_slug: str, title: str = Form(), content: str = Form(), 
                     images: List[UploadFile] = File(default=None), 
                     captions: List[str] = Form(default=[]),
                     db: Session = Depends(get_db),
                     user: User = Depends(get_current_user)):
    
    article = get_article(article_slug, db)

    # create paragraph and save it
    paragraph = ArticleParagraph(title=title, content=content, article_id=article.id)
    db.add(paragraph)
    db.commit()
    db.refresh(paragraph)
    
    # check if images was sended
    if images:
        for index, image in enumerate(images):
            # check if position is empty
            if image.content_type:
                
                # create paragraph image
                paragraph_image = ArticleParagraphImage(image="", paragraph_id=paragraph.id)
                db.add(paragraph_image)
                db.commit()
                db.refresh(paragraph_image)
                
                # upload file in AWS S3 bucket
                url = upload_file(image.file, f"{paragraph_image.id}", f"paragrah-images/paragraph-{paragraph.id}/")
                
                # save url image and caption in paragraph image object
                paragraph_image.image = url
                if len(captions) > index: paragraph_image.caption = captions[index]
                db.commit()
                db.refresh(paragraph_image)
                
    return paragraph


@paragraph_router.get(path="/article/{article_slug}/paragraphs", status_code=status.HTTP_201_CREATED, response_model=List[ArticleParagraphSchema])
def paragraph_list(article_slug: str,
                   db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    
    article = get_article(article_slug, db)
    
    # return all paragraph
    return db.query(ArticleParagraph)\
             .filter(ArticleParagraph.article_id == article.id)\
             .all()
             

@paragraph_router.patch(path="/article/paragraph/{paragraph_id}", status_code=status.HTTP_200_OK, response_model=ArticleParagraphSchema)
def paragraph_update(paragraph_id: str, title: str = Form(default=None), content: str = Form(str),
                     db: Session = Depends(get_db),
                     user: User = Depends(get_current_user)):
    
    # get paragraph
    paragraph = get_paragraph(paragraph_id, db)
    
    # update field send
    if title: paragraph.title = title
    if content: paragraph.content = content
    
    # save update
    db.commit()
    db.refresh(paragraph)
    
    return paragraph
    

@paragraph_router.get(path="/article/paragraph/{paragraph_id}", status_code=status.HTTP_200_OK, response_model=ArticleParagraphSchema)
def paragraph_retrieve(paragraph_id: str,
                       db: Session = Depends(get_db),
                       user: User = Depends(get_current_user)):
    # return paragraph
    return get_paragraph(paragraph_id, db)


@paragraph_router.delete(path="/article/paragraph/{paragraph_id}", status_code=status.HTTP_204_NO_CONTENT)
def paragraph_delete(paragraph_id: str,
                     db: Session = Depends(get_db),
                     user: User = Depends(get_current_user)):
    paragraph = get_paragraph(paragraph_id, db)
    
    # for all image of paragraph remove it in AWS bucket
    for el in db.query(ArticleParagraphImage).filter(ArticleParagraphImage.paragraph_id == paragraph.id).all():
        delete_file(el.image.replace(AWS_BUCKET_URL + "/", ''))
        
    # delete paragraph
    db.delete(paragraph)
    db.commit()
    
    return {"msg": "Paragrafo elimitato"}
        

@paragraph_router.delete(path="/article/paragraph/image/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def paragraph_image_delete(image_id: str,
                           db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    image = get_paragraph_image(image_id, db)
    
    # remove file from AWS S3 bucket
    delete_file(image.image.replace(AWS_BUCKET_URL + "/", ''))
    
    # remove object from database
    db.delete(image)
    db.commit()
    return {"msg": "Immagine eliminata"}


@paragraph_router.post(path="/article/paragraph/{paragraph_id}/image", status_code=status.HTTP_201_CREATED, response_model=List[ArticleParagraphImageSchema])
def paragraph_image_create(paragraph_id: str,
                           images: List[UploadFile] = File(), 
                           captions: List[str] = [],
                           db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    paragraph = get_paragraph(paragraph_id, db)
    response = []
    
    # for all images send get it
    for index, image in enumerate(images):
        
        # create object and save it
        paragraph_image = ArticleParagraphImage(image="", paragraph_id=paragraph.id)
        db.add(paragraph_image)
        db.commit()
        db.refresh(paragraph_image)
        
        # upload file on AWS S3 bucket
        url = upload_file(image.file, f"{paragraph_image.id}", f"paragrah-images/paragraph-{paragraph.id}/")

        # save caption and url in object
        paragraph_image.image = url
        if len(captions) > index: paragraph_image.caption = captions[index]
        db.commit()
        db.refresh(paragraph_image)
        response.append(paragraph_image)
        
    return response


@paragraph_router.patch(path="/article/paragraph/image/{image_id}", status_code=status.HTTP_200_OK, response_model=ArticleParagraphImageSchema)
def paragraph_image_update(image_id: str, caption: str = Form(),
                           db: Session = Depends(get_db),
                           user: User = Depends(get_current_user)):
    image = get_paragraph_image(image_id, db)
    # update caption
    image.caption = caption
    
    # save image
    db.commit()
    db.refresh(image)
    
    return image
    