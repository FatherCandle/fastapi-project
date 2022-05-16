from fastapi import Depends, Response, status, HTTPException, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from app import database

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    post = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post: {vote.post_id} doesnt exists",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.is_voted:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user: {current_user.id} already voted for post: {vote.post_id}",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return_obj = {"message": "Post was successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"vote for user: {current_user.id} of post: {vote.post_id} doesnt exists",
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return_obj = {"message": "Voted deleted"}
    return return_obj
