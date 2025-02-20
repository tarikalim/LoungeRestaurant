from confluent_kafka import Producer
from config import KAFKA_BROKER, PROCESSED_COMMENTS_TOPIC
from generated.processed import Processed

producer_conf = {
    'bootstrap.servers': KAFKA_BROKER
}
producer = Producer(producer_conf)

batch_size = 10
message_count = 0


def produce_processed_comment(comment, sentiment):
    global message_count
    processed = Processed(
        comment_id=comment.comment_id,
        content=comment.content,
        sentiment=sentiment
    )
    serialized_message = processed.SerializeToString()

    producer.produce(
        topic=PROCESSED_COMMENTS_TOPIC,
        value=serialized_message
    )

    message_count += 1
    if message_count % batch_size == 0:
        producer.flush()
