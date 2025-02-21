from pydantic import BaseModel

class CommentResponse(BaseModel):
    id: str
    content: str
    sentiment: str

    class Config:
        from_attributes = True
