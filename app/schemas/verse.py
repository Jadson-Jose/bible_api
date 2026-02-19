from pydantic import BaseModel


class VerseCreate(BaseModel):
    number: int
    text: str
    chapter_id: int


class Verseresponse(BaseModel):
    id: int
    number: int
    text: str
    chapter_id: int

    class Config:
        from_attributes = True
