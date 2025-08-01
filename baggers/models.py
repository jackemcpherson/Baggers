from sqlalchemy import Column, Integer, String

from .database import Base


class Bagger(Base):
    __tablename__ = "baggers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    membershipNo = Column(String, nullable=False, unique=True, index=True)
    emailAddress = Column(String, nullable=True)
    phoneNumber = Column(String, nullable=True)
