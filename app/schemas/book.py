from pydantic import BaseModel


class BookCreate(BaseModel):
    name: str
    abbreviation: str


class BookResponse(BaseModel):
    id: int
    name: str
    abbreviation: str
