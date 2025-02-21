from confluent_kafka import Producer
from .config import KAFKA_BROKER, PROCESSED_COMMENTS_TOPIC
from .generated.processed import Processed

class CommentProducer:
    def __init__(self, batch_size=10):
        self.producer_conf = {'bootstrap.servers': KAFKA_BROKER}
        self.producer = Producer(self.producer_conf)
        self.batch_size = batch_size
        self.message_count = 0

    def produce_processed_comment(self, comment, sentiment):
        processed = Processed(
            comment_id=comment.comment_id,
            content=comment.content,
            sentiment=sentiment
        )
        serialized_message = processed.SerializeToString()

        try:
            self.producer.produce(
                topic=PROCESSED_COMMENTS_TOPIC,
                value=serialized_message
            )
        except Exception as e:
            print("Error while sending message to kafka: ", e)

        self.message_count += 1

        if self.message_count % self.batch_size == 0:
            self.producer.flush()

    def flush(self):
        self.producer.flush()
