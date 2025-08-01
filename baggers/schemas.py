from pydantic import BaseModel
from typing import Optional


class BaggerBase(BaseModel):
    name: str
    membershipNo: str
    emailAddress: Optional[str] = None
    phoneNumber: Optional[str] = None


class BaggerCreate(BaggerBase):
    pass


class Bagger(BaggerBase):
    id: int

    class Config:
        from_attributes = True