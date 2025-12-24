from fastapi import APIRouter, Depends, status, HTTPException
import schema,database,models,Oauth2
from sqlalchemy.orm import Session
router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote,db:Session=Depends(database.get_db),current_user:models.Users=Depends(Oauth2.get_current_user)):
    # check_vote=db.query(models.Vote).filter(vote.post_id == models.Post.id ).first()
    # if not check_vote:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    check_post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not check_post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already vated on this post")
        new_vote=models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message":"Successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message":"Successfully deleted vote"}