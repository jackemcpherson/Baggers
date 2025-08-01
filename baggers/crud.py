from sqlalchemy.orm import Session
from . import models, schemas


def get_bagger(db: Session, bagger_id: int):
    """Get a single bagger by ID"""
    return db.query(models.Bagger).filter(models.Bagger.id == bagger_id).first()


def get_baggers(db: Session, skip: int = 0, limit: int = 100):
    """Get all baggers with optional pagination"""
    return db.query(models.Bagger).offset(skip).limit(limit).all()


def get_bagger_by_membership(db: Session, membership_no: str):
    """Get a bagger by membership number"""
    return db.query(models.Bagger).filter(models.Bagger.membershipNo == membership_no).first()


def create_bagger(db: Session, bagger: schemas.BaggerCreate):
    """Create a new bagger"""
    db_bagger = models.Bagger(
        name=bagger.name,
        membershipNo=bagger.membershipNo,
        emailAddress=bagger.emailAddress,
        phoneNumber=bagger.phoneNumber
    )
    db.add(db_bagger)
    db.commit()
    db.refresh(db_bagger)
    return db_bagger


def update_bagger(db: Session, bagger_id: int, bagger: schemas.BaggerCreate):
    """Update an existing bagger"""
    db_bagger = db.query(models.Bagger).filter(models.Bagger.id == bagger_id).first()
    if db_bagger:
        # Get data from the Pydantic model as a dictionary
        update_data = bagger.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_bagger, key, value)
        db.commit()
        db.refresh(db_bagger)
    return db_bagger


def delete_bagger(db: Session, bagger_id: int):
    """Delete a bagger by ID"""
    db_bagger = db.query(models.Bagger).filter(models.Bagger.id == bagger_id).first()
    if db_bagger:
        db.delete(db_bagger)
        db.commit()
    return db_bagger