from sqlalchemy.orm import Session
from typing import Optional, Type

from api.model.model import Comment


def get_comments(db: Session, sentiment: Optional[str] = None) -> list[Type[Comment]]:
    query = db.query(Comment)
    if sentiment:
        query = query.filter(Comment.sentiment == sentiment)
    return query.all()
