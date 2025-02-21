from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from api.schema.comment import CommentResponse
from api.database import get_db
from api.service.comment import get_comments

router = APIRouter()


@router.get("/", response_model=List[CommentResponse])
def read_comments(sentiment: Optional[str] = Query(None),
                  db: Session = Depends(get_db)):
    comments = get_comments(db, sentiment)
    if not comments:
        raise HTTPException(status_code=404, detail="No Comment Found")
    return comments
