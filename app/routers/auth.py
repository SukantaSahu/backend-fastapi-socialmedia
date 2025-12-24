from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import schema, models,utils, Oauth2

router=APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schema.Token)
#def login(user_credentials:schema.UserLogin,db:Session=Depends(get_db)):
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
#    user=db.query(models.Users).filter(models.Users.email==user_credentials.email).first()
    user=db.query(models.Users).filter(models.Users.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    access_token=Oauth2.create_access_token(data={"user_id":user.id})
    return {"access_token":access_token,"token_type":"bearer"}