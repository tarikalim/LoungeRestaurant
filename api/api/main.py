from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.router import comment

app = FastAPI(title="Comment API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(comment.router, prefix="/comments", tags=["comments"])

if __name__ == "__main__":
    import uvicorn

    # for development environment
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
