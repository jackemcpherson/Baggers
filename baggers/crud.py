from sqlalchemy.orm import Session

from . import models, schemas


def get_bagger(db: Session, bagger_id: int):
    """Get a single bagger by ID.

    Args:
        db: Database session.
        bagger_id: The ID of the bagger to retrieve.

    Returns:
        Bagger model instance or None if not found.
    """
    return db.query(models.Bagger).filter(models.Bagger.id == bagger_id).first()


def get_baggers(db: Session, skip: int = 0, limit: int = 100):
    """Get all baggers with optional pagination.

    Args:
        db: Database session.
        skip: Number of records to skip.
        limit: Maximum number of records to return.

    Returns:
        List of Bagger model instances.
    """
    return db.query(models.Bagger).offset(skip).limit(limit).all()


def get_bagger_by_membership(db: Session, membership_no: str):
    """Get a bagger by membership number.

    Args:
        db: Database session.
        membership_no: The AFL membership number to search for.

    Returns:
        Bagger model instance or None if not found.
    """
    return (
        db.query(models.Bagger)
        .filter(models.Bagger.membershipNo == membership_no)
        .first()
    )


def create_bagger(db: Session, bagger: schemas.BaggerCreate):
    """Create a new bagger.

    Args:
        db: Database session.
        bagger: Bagger data to create.

    Returns:
        Created Bagger model instance.
    """
    db_bagger = models.Bagger(
        name=bagger.name,
        membershipNo=bagger.membershipNo,
        emailAddress=bagger.emailAddress,
        phoneNumber=bagger.phoneNumber,
    )
    db.add(db_bagger)
    db.commit()
    db.refresh(db_bagger)
    return db_bagger


def update_bagger(db: Session, bagger_id: int, bagger: schemas.BaggerCreate):
    """Update an existing bagger.

    Args:
        db: Database session.
        bagger_id: The ID of the bagger to update.
        bagger: Updated bagger data.

    Returns:
        Updated Bagger model instance or None if not found.
    """
    db_bagger = db.query(models.Bagger).filter(models.Bagger.id == bagger_id).first()
    if db_bagger:
        update_data = bagger.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_bagger, key, value)
        db.commit()
        db.refresh(db_bagger)
    return db_bagger


def delete_bagger(db: Session, bagger_id: int):
    """Delete a bagger by ID.

    Args:
        db: Database session.
        bagger_id: The ID of the bagger to delete.

    Returns:
        Deleted Bagger model instance or None if not found.
    """
    db_bagger = db.query(models.Bagger).filter(models.Bagger.id == bagger_id).first()
    if db_bagger:
        db.delete(db_bagger)
        db.commit()
    return db_bagger
