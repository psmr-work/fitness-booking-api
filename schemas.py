from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class FitnessClassOut(BaseModel):
    id: int
    name: str
    datetime: datetime
    instructor: str
    available_slots: int

    class Config:
        from_attributes = True


class BookingRequest(BaseModel):
    class_id : int
    client_name : str = Field(..., strip_whitespace=True, min_length=1 )
    client_email : EmailStr

class BookingOut(BaseModel):
    id:int
    class_id:int
    client_name:str
    client_email:EmailStr

    class Config:
        from_attributes = True

