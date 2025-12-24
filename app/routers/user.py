
from fastapi import  status, HTTPException, Depends, APIRouter
import models, schema, utils
from sqlalchemy.orm import Session
from database import get_db

router=APIRouter(
    prefix="/users", tags=['users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_users(user:schema.Usercreate,db:Session =Depends(get_db)):
    hased_password=utils.hash(user.password)
    user.password=hased_password
    new_user=models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schema.UserOut)
def gate_post(id:int,db:Session=Depends(get_db)): #response:Response):
    try:
        # cursor.execute("select * from posts where id=%s", id)
        # post1=cursor.fetchone()
        user1=db.query(models.Users).filter(models.Users.id==id).first()
    except Exception as e:
        print(e)
    if not user1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Selected id {id} not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {f"post with id {id} not found"}
    return user1

@router.get("/",response_model=list[schema.UserOut])
def gate_post(db:Session=Depends(get_db)): #response:Response):
    try:
        # cursor.execute("select * from posts where id=%s", id)
        # post1=cursor.fetchone()
        user1=db.query(models.Users).all()
    except Exception as e:
        print(e)
    if not user1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error in getting details")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {f"post with id {id} not found"}
    return user1