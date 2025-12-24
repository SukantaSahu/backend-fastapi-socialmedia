from fastapi import  status, HTTPException, Depends, APIRouter
import models, schema, Oauth2
from sqlalchemy.orm import Session
from database import get_db

router=APIRouter(
    prefix="/post",tags=['posts']
)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post:schema.Postcreate,db:Session=Depends(get_db), get_current_user:int =Depends(Oauth2.get_current_user)):
    # cursor.execute("insert into posts (title,content) values(%s,%s)",(post.title,post.content))
    # connection.commit()
    # new_id=cursor.lastrowid
    # cursor.execute("select * from posts where id=%s",(new_id))
    # new_post=cursor.fetchone()
    #new_post =models.Post(title=post.title,content=post.content,published=post.published)
    new_post=models.Post(owner_id=get_current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

@router.get("/",response_model=list[schema.Post])
def gate_post(db:Session=Depends(get_db),get_current_user:int =Depends(Oauth2.get_current_user)):
    try:
        # cursor.execute("select * from posts")
        # table=cursor.fetchall()
        posts=db.query(models.Post).all()
    except Exception as e:
        print(e)
    #return {"data":table}
    return posts

@router.get("/{id}",response_model=schema.Post)
def gate_post(id:int,db:Session=Depends(get_db),get_current_user:int =Depends(Oauth2.get_current_user)): #response:Response):
    try:
        # cursor.execute("select * from posts where id=%s", id)
        # post1=cursor.fetchone()
        post1=db.query(models.Post).filter(models.Post.id==id).first()
    except Exception as e:
        print(e)
    if not post1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Selected id {id} not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {f"post with id {id} not found"}
    return post1

@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id:int,db:Session=Depends(get_db),get_current_user:int =Depends(Oauth2.get_current_user)):
    #index = find_index_post(id)
    try:
        # cursor.execute("delete from posts where id=%s",id)
        # index=cursor.fetchone
        # connection.commit()
        index=db.query(models.Post).filter(models.Post.id==id)
    except Exception as e:
        print(e)
    if index.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
    if index.first().owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete others post")
    #my_posts.pop(index)

    index.delete(synchronize_session=False)
    db.commit()
    

@router.put("/{id}", response_model=schema.Post)
def update_post(id:int,post:schema.Postcreate,db:Session=Depends(get_db),current_user:int =Depends(Oauth2.get_current_user)):
    #index = find_index_post(id)
    # cursor.execute("select * from posts where %s in (id)",id)
    # index1=cursor.fetchone()
    index1=db.query(models.Post).filter(models.Post.id==id)
    query=index1.first()
    if query==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
    #cursor.execute("update posts set title=%s, content=%s where id=%s",(post.title,post.content,id))
    #index=cursor.fetchone()
    #connection.commit()
    if query.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update others post")
    updated_post=post.model_dump()
    updated_post['owner_id']=current_user.id
    index1.update(updated_post,synchronize_session=False)
    db.commit()
    # if index==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} not found")
    #post_dict=post.model_dump()
    #post_dict['id']=id
    #my_posts[index]=post_dict
    #return post_dict
    #cursor.execute("select * from posts where %s in (id)",id)
    #index2=cursor.fetchone()
    return index1.first()