from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class BookBase(BaseModel):
    title: str = Field(..., max_length=200)
    author: str = Field(..., max_length=150)
    isbn: str = Field(..., max_length=50)
    price: float = Field(..., ge=0)


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class BookPatch(BaseModel):
    title: Optional[str] = None #atomic habits
    author: Optional[str] = None
    isbn: Optional[str] = None
    price: Optional[float] = None