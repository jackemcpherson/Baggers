from pydantic import BaseModel


class BaggerBase(BaseModel):
    name: str
    membershipNo: str
    emailAddress: str | None = None
    phoneNumber: str | None = None


class BaggerCreate(BaggerBase):
    pass


class Bagger(BaggerBase):
    id: int

    class Config:
        from_attributes = True
