from confluent_kafka import Consumer
from config import KAFKA_BROKER, RAW_COMMENTS_TOPIC
from generated.comment import Comment


class CommentConsumer:
    def __init__(self):
        self.consumer_conf = {
            'bootstrap.servers': KAFKA_BROKER,
            'group.id': 'comment_processor_group',
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.consumer_conf)
        self.consumer.subscribe([RAW_COMMENTS_TOPIC])

    def process_message(self, msg):
        comment = Comment().parse(msg.value())
        print(f"Received Comment:\n  ID: {comment.comment_id}\n  Content: {comment.content}")
        return comment

    def run(self):
        while True:
            msg = self.consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error:", msg.error())
                continue
            yield self.process_message(msg)

    def close(self):
        self.consumer.close()
