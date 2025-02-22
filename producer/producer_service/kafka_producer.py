import uuid
import time
import random
from faker import Faker
from confluent_kafka import Producer
from .config import KAFKA_BROKER, RAW_COMMENTS_TOPIC
from producer_service.generated.comment import Comment
from .check_kafka import check_kafka


class CommentProducer:
    def __init__(self, batch_size=10, sleep_range=(0.1, 10)):
        self.producer = Producer({'bootstrap.servers': KAFKA_BROKER})
        self.fake = Faker()
        self.batch_size = batch_size
        self.sleep_range = sleep_range
        self.message_count = 0

    def generate_comment(self):
        return Comment(
            comment_id=str(uuid.uuid4()),
            content=self.fake.sentence()
        )

    def log_callback(self, err, msg):
        if err is not None:
            print(f"Error: {err}")
        else:
            print(f"Message topic in Kafka: {msg.topic()}")

    @check_kafka
    def produce_messages(self):
        while True:
            comment = self.generate_comment()
            serialized_message = comment.SerializeToString()

            try:
                self.producer.produce(
                    topic=RAW_COMMENTS_TOPIC,
                    key=comment.comment_id.encode(),
                    value=serialized_message,
                    callback=self.log_callback
                )
            except Exception as e:
                print(f"Exception occurred: {e}")
                raise

            print(f"Sent Message: {comment}")
            self.message_count += 1

            if self.message_count % self.batch_size == 0:
                # Buffer'da bekleyen mesajların Kafka'ya gönderilmesini sağlıyor.
                # her 10 mesajda bir bufferdakileri kafka brokerına iletiyor.
                # veri kaybını önlemek için önemli, 10 yerine daha yüksek bir miktar olabilir.
                self.producer.flush()
                print(f"Flushed {self.batch_size} messages to Kafka.")

            time.sleep(random.uniform(*self.sleep_range))
