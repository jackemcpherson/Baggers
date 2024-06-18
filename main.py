from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Set up the database connection
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    barcode = Column(String, unique=True, index=True)
    phone_number = Column(String)
    email = Column(String)


# Create the database tables
Base.metadata.create_all(bind=engine)


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint to get all barcodes
@app.get("/barcode")
def get_all_barcodes(db: SessionLocal = Depends(get_db)):
    barcodes = db.query(User.name, User.barcode).all()
    return barcodes


# Endpoint to get the barcode of a user by name
@app.get("/barcode/{name}")
def get_barcode_by_name(name: str, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.name == name).first()
    if user:
        return {"name": user.name, "barcode": user.barcode}
    else:
        raise HTTPException(status_code=404, detail="User not found")


# Endpoint to get all phone numbers
@app.get("/phone")
def get_all_phone_numbers(db: SessionLocal = Depends(get_db)):
    phone_numbers = db.query(User.name, User.phone_number).all()
    return phone_numbers


# Endpoint to get the phone number of a user by name
@app.get("/phone/{name}")
def get_phone_by_name(name: str, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.name == name).first()
    if user:
        return {"name": user.name, "phone_number": user.phone_number}
    else:
        raise HTTPException(status_code=404, detail="User not found")


# Endpoint to get all emails
@app.get("/email")
def get_all_emails(db: SessionLocal = Depends(get_db)):
    emails = db.query(User.name, User.email).all()
    return emails


# Endpoint to get the email of a user by name
@app.get("/email/{name}")
def get_email_by_name(name: str, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.name == name).first()
    if user:
        return {"name": user.name, "email": user.email}
    else:
        raise HTTPException(status_code=404, detail="User not found")
