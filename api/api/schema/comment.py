from pydantic import BaseModel
from typing import List


class CommentResponse(BaseModel):
    id: str
    content: str
    sentiment: str

    class Config:
        from_attributes = True


class CommentsResponse(BaseModel):
    comments: List[CommentResponse]
    total: int
