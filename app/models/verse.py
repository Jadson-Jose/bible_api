from sqlalchemy import Column, ForeignKey, Integer, Text

from app.database import Base


class Verse(Base):
    __tablename__ = "verses"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)  # Text para textos longos
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
