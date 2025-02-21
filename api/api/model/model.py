from sqlalchemy import Column, String, Text
from api.database import Base


class Comment(Base):
    __tablename__ = "comment"

    id = Column(String(255), primary_key=True, index=True)
    content = Column(Text, nullable=False)
    sentiment = Column(String(50), nullable=False)
