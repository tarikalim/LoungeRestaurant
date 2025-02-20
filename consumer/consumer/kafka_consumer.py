from confluent_kafka import Consumer
from config import KAFKA_BROKER, RAW_COMMENTS_TOPIC
from generated.comment import Comment

consumer_conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'comment_processor_group',
    'auto.offset.reset': 'earliest'
}


def create_consumer():
    consumer = Consumer(consumer_conf)
    consumer.subscribe([RAW_COMMENTS_TOPIC])
    return consumer


def process_message(msg):
    comment = Comment().parse(msg.value())
    print(f"Received Comment:\n  ID: {comment.comment_id}\n  Content: {comment.content}")
    return comment

def run_consumer():
    consumer = create_consumer()
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error:", msg.error())
            continue
        process_message(msg)

    consumer.close()
