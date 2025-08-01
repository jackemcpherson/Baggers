import pytest
from sqlalchemy.exc import IntegrityError

from baggers import crud, schemas


def test_create_bagger(db):
    """Test creating a new bagger"""
    bagger_data = schemas.BaggerCreate(
        name="John Doe",
        membershipNo="AFL12345",
        emailAddress="john@example.com",
        phoneNumber="0412345678",
    )
    db_bagger = crud.create_bagger(db=db, bagger=bagger_data)

    assert db_bagger.name == "John Doe"
    assert db_bagger.membershipNo == "AFL12345"
    assert db_bagger.emailAddress == "john@example.com"
    assert db_bagger.phoneNumber == "0412345678"
    assert db_bagger.id is not None


def test_create_bagger_minimal(db):
    """Test creating a bagger with only required fields"""
    bagger_data = schemas.BaggerCreate(name="Jane Smith", membershipNo="AFL67890")
    db_bagger = crud.create_bagger(db=db, bagger=bagger_data)

    assert db_bagger.name == "Jane Smith"
    assert db_bagger.membershipNo == "AFL67890"
    assert db_bagger.emailAddress is None
    assert db_bagger.phoneNumber is None


def test_get_bagger(db):
    """Test retrieving a bagger by ID"""
    bagger_data = schemas.BaggerCreate(name="Test User", membershipNo="AFL11111")
    created_bagger = crud.create_bagger(db=db, bagger=bagger_data)

    retrieved_bagger = crud.get_bagger(db=db, bagger_id=created_bagger.id)

    assert retrieved_bagger is not None
    assert retrieved_bagger.id == created_bagger.id
    assert retrieved_bagger.name == "Test User"
    assert retrieved_bagger.membershipNo == "AFL11111"


def test_get_bagger_not_found(db):
    """Test retrieving a non-existent bagger"""
    result = crud.get_bagger(db=db, bagger_id=999)
    assert result is None


def test_get_baggers(db):
    """Test retrieving all baggers"""
    bagger1 = schemas.BaggerCreate(name="User 1", membershipNo="AFL001")
    bagger2 = schemas.BaggerCreate(name="User 2", membershipNo="AFL002")

    crud.create_bagger(db=db, bagger=bagger1)
    crud.create_bagger(db=db, bagger=bagger2)

    baggers = crud.get_baggers(db=db)

    assert len(baggers) == 2
    assert baggers[0].name == "User 1"
    assert baggers[1].name == "User 2"


def test_get_bagger_by_membership(db):
    """Test retrieving a bagger by membership number"""
    bagger_data = schemas.BaggerCreate(name="Member Test", membershipNo="AFL99999")
    created_bagger = crud.create_bagger(db=db, bagger=bagger_data)

    retrieved_bagger = crud.get_bagger_by_membership(db=db, membership_no="AFL99999")

    assert retrieved_bagger is not None
    assert retrieved_bagger.id == created_bagger.id
    assert retrieved_bagger.membershipNo == "AFL99999"


def test_update_bagger(db):
    """Test updating an existing bagger"""
    original_data = schemas.BaggerCreate(name="Original Name", membershipNo="AFL555")
    created_bagger = crud.create_bagger(db=db, bagger=original_data)

    update_data = schemas.BaggerCreate(
        name="Updated Name",
        membershipNo="AFL555",
        emailAddress="updated@example.com",
        phoneNumber="0400000000",
    )
    updated_bagger = crud.update_bagger(
        db=db, bagger_id=created_bagger.id, bagger=update_data
    )

    assert updated_bagger.id == created_bagger.id
    assert updated_bagger.name == "Updated Name"
    assert updated_bagger.emailAddress == "updated@example.com"
    assert updated_bagger.phoneNumber == "0400000000"


def test_update_bagger_not_found(db):
    """Test updating a non-existent bagger"""
    update_data = schemas.BaggerCreate(name="Non-existent", membershipNo="AFL000")
    result = crud.update_bagger(db=db, bagger_id=999, bagger=update_data)
    assert result is None


def test_delete_bagger(db):
    """Test deleting a bagger"""
    bagger_data = schemas.BaggerCreate(name="Delete Me", membershipNo="AFL777")
    created_bagger = crud.create_bagger(db=db, bagger=bagger_data)

    deleted_bagger = crud.delete_bagger(db=db, bagger_id=created_bagger.id)

    assert deleted_bagger.id == created_bagger.id
    assert deleted_bagger.name == "Delete Me"

    result = crud.get_bagger(db=db, bagger_id=created_bagger.id)
    assert result is None


def test_delete_bagger_not_found(db):
    """Test deleting a non-existent bagger"""
    result = crud.delete_bagger(db=db, bagger_id=999)
    assert result is None


def test_unique_membership_constraint(db):
    """Test that membership numbers must be unique"""
    bagger1 = schemas.BaggerCreate(name="First User", membershipNo="AFL123")
    bagger2 = schemas.BaggerCreate(name="Second User", membershipNo="AFL123")

    crud.create_bagger(db=db, bagger=bagger1)

    with pytest.raises(IntegrityError):
        crud.create_bagger(db=db, bagger=bagger2)
