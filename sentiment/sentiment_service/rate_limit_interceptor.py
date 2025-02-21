import time
import collections
import grpc

RATE_LIMIT = 100
WINDOW_SIZE_SECONDS = 1


# sentiment_service serverinterceptor sınıfı, gelen tüm sentiment_service callarını kesebiliyor, rate limit eklemek için ideal
# daha büyük bir projede api gateway vs kullanılabilir ama bu şu an için yeterli.
class RateLimitInterceptor(grpc.ServerInterceptor):
    def __init__(self):
        self.request_timestamps = collections.deque()

    def intercept_service(self, continuation, handler_call_details):
        current_time = time.time()
        while self.request_timestamps and self.request_timestamps[0] < current_time - WINDOW_SIZE_SECONDS:
            self.request_timestamps.popleft()

        if len(self.request_timestamps) >= RATE_LIMIT:
            def deny_request(context):
                # sentiment_service servislerinde rate limit aşıldığında clienta yollanan hata
                context.abort(grpc.StatusCode.RESOURCE_EXHAUSTED, "Rate limit exceeded.")
            return grpc.unary_unary_rpc_method_handler(deny_request)

        self.request_timestamps.append(current_time)

        return continuation(handler_call_details)
