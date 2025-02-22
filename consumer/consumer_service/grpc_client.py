import grpc
from .config import GRPC_SERVER_ADDRESS
from .generated.sentiment_pb2 import SentimentRequest
from .generated.sentiment_pb2_grpc import SentimentAnalysisStub

async def analyze_sentiment(comment):
    async with grpc.aio.insecure_channel(GRPC_SERVER_ADDRESS) as channel:
        stub = SentimentAnalysisStub(channel)
        request = SentimentRequest(
            comment_id=comment.comment_id,
            content=comment.content
        )
        response = await stub.Analyze(request)
        return response.sentiment
