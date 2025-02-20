import threading
import time
import random
from cachetools import TTLCache
from sentiment.generated.sentiment_pb2 import SentimentResponse
from sentiment.generated.sentiment_pb2_grpc import SentimentAnalysisServicer

cache_lock = threading.Lock()
# cache üzerinde ufak kontroller sağlamak için ttlcache kullandım
# aynı content geldiği durumda cache'de zaten sentiment varsa direkt cacheden aynı sentiment atanacak.
sentiment_cache = TTLCache(maxsize=1000, ttl=3600)


class SentimentAnalysisService(SentimentAnalysisServicer):
    def Analyze(self, request, context):
        content = request.content

        with cache_lock:
            if content in sentiment_cache:
                return SentimentResponse(
                    comment_id=request.comment_id,
                    sentiment=sentiment_cache[content]
                )

        sentiment = random.choice(["positive", "negative", "neutral"])
        time.sleep(len(content) * 0.001)

        with cache_lock:
            sentiment_cache[content] = sentiment

        return SentimentResponse(comment_id=request.comment_id, sentiment=sentiment)
