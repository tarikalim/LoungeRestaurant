import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
RAW_COMMENTS_TOPIC = os.getenv("RAW_COMMENTS_TOPIC", "raw_comments")
PROCESSED_COMMENTS_TOPIC = os.getenv("PROCESSED_COMMENTS_TOPIC", "processed_comments")
GRPC_SERVER_ADDRESS = os.getenv("GRPC_SERVER_ADDRESS", "localhost:50051")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "lounge")
DB_USER = os.getenv("DB_USER", "lounge")
DB_PASSWORD = os.getenv("DB_PASSWORD", "lounge_password")
