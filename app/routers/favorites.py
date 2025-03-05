from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..security import get_current_user
from .. import models

router = APIRouter(prefix="/auth/users/favorites", tags=["Favorites"])

@router.post("/shanyraks/{listing_id}")
def add_favorite(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    favorites_assoc = db.execute(
        models.favorites_table.select()
        .where(models.favorites_table.c.user_id == current_user.id)
        .where(models.favorites_table.c.listing_id == listing_id)
    ).first()
    if favorites_assoc:
        return {"message": "Already in favorites"}

    db.execute(
        models.favorites_table.insert().values(
            user_id=current_user.id, listing_id=listing_id
        )
    )
    db.commit()
    return {"message": "Added to favorites"}

@router.get("/shanyraks")
def get_favorites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()

    favorites_data = []
    for listing in user.favorites:
        favorites_data.append({
            "_id": listing.id,
            "address": listing.address
        })

    return {"shanyraks": favorites_data}

@router.delete("/shanyraks/{listing_id}")
def remove_favorite(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    db.execute(
        models.favorites_table.delete()
        .where(models.favorites_table.c.user_id == current_user.id)
        .where(models.favorites_table.c.listing_id == listing_id)
    )
    db.commit()
    return {"message": "Removed from favorites"}
