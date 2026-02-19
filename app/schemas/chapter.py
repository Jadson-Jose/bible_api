from pydantic import BaseModel


class ChapterCreate(BaseModel):
    number: int
    book_id: int


class ChapterResponse(BaseModel):
    id: int
    number: int
    book_id: int

    class Config:
        from_attributes = True
