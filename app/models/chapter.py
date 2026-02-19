from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    # Relacionamento
    # book = relationship("Book", back_populates="chapters")
