import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
RAW_COMMENTS_TOPIC = os.getenv("RAW_COMMENTS_TOPIC", "raw_comments")
PROCESSED_COMMENTS_TOPIC=os.getenv("PROCESSED_COMMENTS_TOPIC", "processed_comments")
GRPC_SERVER_ADDRESS=os.getenv("GRPC_SERVER_ADDRESS", "localhost:50051")

