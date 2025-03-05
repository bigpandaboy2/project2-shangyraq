from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(prefix="/shanyraks", tags=["Comments"])

@router.post("/{listing_id}/comments", status_code=200)
def add_comment(
    listing_id: int,
    comment_data: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    comment = models.Comment(
        content=comment_data.content,
        listing_id=listing.id,
        author_id=current_user.id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {"message": "Comment added successfully"}

@router.get("/{listing_id}/comments", status_code=200)
def get_comments(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    comments = db.query(models.Comment).filter(models.Comment.listing_id == listing_id).all()
    comment_list = []
    for c in comments:
        comment_list.append({
            "id": c.id,
            "content": c.content,
            "created_at": c.created_at,
            "author_id": c.author_id
        })

    return {"comments": comment_list}

@router.patch("/{listing_id}/comments/{comment_id}", status_code=200)
def update_comment(
    listing_id: int,
    comment_id: int,
    comment_data: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id,
        models.Comment.listing_id == listing_id
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")

    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return {"message": "Comment updated successfully"}

# app/routers/comments.py
@router.patch("/{listing_id}/comments/{comment_id}")
def update_comment(
    listing_id: int,
    comment_id: int,
    comment_data: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id,
        models.Comment.listing_id == listing_id
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # only author can update
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")

    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    return {"message": "Comment updated successfully"}


@router.delete("/{listing_id}/comments/{comment_id}")
def delete_comment(
    listing_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id,
        models.Comment.listing_id == listing_id
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    if (comment.author_id != current_user.id) and (listing.user_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}

