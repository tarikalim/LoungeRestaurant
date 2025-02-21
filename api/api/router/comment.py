from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from api.schema.comment import CommentsResponse
from api.database import get_db
from api.service.comment import get_comments

router = APIRouter()


@router.get("/", response_model=CommentsResponse)
def read_comments(
        sentiment: Optional[str] = Query(None),
        db: Session = Depends(get_db)
):
    comments, total = get_comments(db, sentiment)
    if not comments:
        raise HTTPException(status_code=404, detail="No Comment Found")
    return {"comments": comments, "total": total}
