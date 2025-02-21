from sqlalchemy.orm import Session
from typing import Optional
from api_service.model.model import Comment


def get_comments(db: Session, sentiment: Optional[str] = None):
    query = db.query(Comment)
    if sentiment:
        query = query.filter(Comment.sentiment == sentiment)

    comments = query.all()
    total = len(comments)

    return comments, total
