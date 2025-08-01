from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/baggers/", response_model=schemas.Bagger)
def create_bagger(bagger: schemas.BaggerCreate, db: Session = Depends(get_db)):
    """Create a new bagger"""
    try:
        return crud.create_bagger(db=db, bagger=bagger)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=422, detail="Membership number already registered"
        )


@router.get("/baggers/", response_model=List[schemas.Bagger])
def read_baggers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all baggers"""
    baggers = crud.get_baggers(db, skip=skip, limit=limit)
    return baggers


@router.get("/baggers/{bagger_id}", response_model=schemas.Bagger)
def read_bagger(bagger_id: int, db: Session = Depends(get_db)):
    """Get a single bagger by ID"""
    db_bagger = crud.get_bagger(db, bagger_id=bagger_id)
    if db_bagger is None:
        raise HTTPException(status_code=404, detail="Bagger not found")
    return db_bagger


@router.put("/baggers/{bagger_id}", response_model=schemas.Bagger)
def update_bagger(
    bagger_id: int, bagger: schemas.BaggerCreate, db: Session = Depends(get_db)
):
    """Update an existing bagger"""
    # Check if bagger exists
    db_bagger = crud.get_bagger(db, bagger_id=bagger_id)
    if db_bagger is None:
        raise HTTPException(status_code=404, detail="Bagger not found")

    try:
        return crud.update_bagger(db=db, bagger_id=bagger_id, bagger=bagger)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=422, detail="Membership number already registered"
        )


@router.delete("/baggers/{bagger_id}", response_model=schemas.Bagger)
def delete_bagger(bagger_id: int, db: Session = Depends(get_db)):
    """Delete a bagger by ID"""
    db_bagger = crud.get_bagger(db, bagger_id=bagger_id)
    if db_bagger is None:
        raise HTTPException(status_code=404, detail="Bagger not found")

    return crud.delete_bagger(db=db, bagger_id=bagger_id)
