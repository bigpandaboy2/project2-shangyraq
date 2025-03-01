from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(prefix="/shanyraks", tags=["Listings"])

@router.post("/", status_code=200)
def create_listing(
    listing_data: schemas.ListingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    listing = models.Listing(
        type=listing_data.type,
        price=listing_data.price,
        address=listing_data.address,
        area=listing_data.area,
        rooms_count=listing_data.rooms_count,
        description=listing_data.description,
        user_id=current_user.id
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return {"id": listing.id}

@router.get("/{listing_id}", response_model=schemas.ListingOut, status_code=200)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    total_comments = db.query(models.Comment).filter(models.Comment.listing_id == listing_id).count()

    return schemas.ListingOut(
        id=listing.id,
        type=listing.type,
        price=listing.price,
        address=listing.address,
        area=listing.area,
        rooms_count=listing.rooms_count,
        description=listing.description,
        user_id=listing.user_id,
        total_comments=total_comments
    )

@router.patch("/{listing_id}", status_code=200)
def update_listing(
    listing_id: int,
    update_data: schemas.ListingUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this listing")

    if update_data.type is not None:
        listing.type = update_data.type
    if update_data.price is not None:
        listing.price = update_data.price
    if update_data.address is not None:
        listing.address = update_data.address
    if update_data.area is not None:
        listing.area = update_data.area
    if update_data.rooms_count is not None:
        listing.rooms_count = update_data.rooms_count
    if update_data.description is not None:
        listing.description = update_data.description

    db.commit()
    db.refresh(listing)
    return {"message": "Listing updated successfully"}

@router.delete("/{listing_id}", status_code=200)
def delete_listing(
    listing_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    listing = db.query(models.Listing).filter(models.Listing.id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this listing")

    db.delete(listing)
    db.commit()
    return {"message": "Listing deleted successfully"}
