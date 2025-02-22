from functools import wraps
import time


def check_kafka(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        while True:
            try:
                metadata = self.consumer.list_topics(timeout=5)
                if metadata.brokers:
                    print("Connected to Kafka.")
                    break
                else:
                    print("Kafka connection failed: No brokers found. Retrying.")
            except Exception as e:
                if "Connection refused" in str(e):
                    print(f"Kafka connection refused: {e}. Retrying.")
                else:
                    print(f"Kafka connection error: {e}. Retrying.")
            time.sleep(1)
        return func(self, *args, **kwargs)

    return wrapper
