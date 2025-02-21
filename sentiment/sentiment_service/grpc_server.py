from concurrent import futures
import grpc
from .generated.sentiment_pb2_grpc import add_SentimentAnalysisServicer_to_server
from .analyze import SentimentAnalysisService
from .rate_limit_interceptor import RateLimitInterceptor


def serve():
    interceptors = [RateLimitInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=interceptors
    )
    add_SentimentAnalysisServicer_to_server(SentimentAnalysisService(), server)
    server.add_insecure_port("[::]:50051")
    print("Server started")
    server.start()
    server.wait_for_termination()
