from sqlalchemy import Column, Integer, String

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    abbreviation = Column(String, nullable=False)
