from typing import List, Optional
from fastapi import HTTPException, status, Response, Depends, APIRouter
from .. import models, schemas, oauth2
from .. database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/post", tags=['Post'])

@router.get("/", response_model=List[schemas.Post])
def get_posts(db:Session = Depends(get_db),current_user: int = 
                 Depends(oauth2.get_current_user), limit: int = 30, search: Optional[str]=""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
       
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    print(current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int,db:Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post {id} not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not Authorized")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(post: schemas.PostCreate, id:int,db:Session = Depends(get_db), current_user: int = 
                 Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated_post = post_query.first()
    
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post {id} not found")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized")

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
