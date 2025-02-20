import uuid
import time
import random
from faker import Faker
from confluent_kafka import Producer
from config import KAFKA_BROKER, RAW_COMMENTS_TOPIC
from generated.comment import Comment

producer = Producer({'bootstrap.servers': KAFKA_BROKER})
fake = Faker()


def generate_comment():
    return Comment(
        comment_id=str(uuid.uuid4()),
        content=fake.sentence()
    )


def log(err, msg):
    if err is not None:
        print(f"Error: {err}")
    else:
        print(f" Message topic in kafka : {msg.topic()}")


batch_size = 10  # Her 10 mesajda bir flush yapmak için, her mesaj yerine
message_count = 0

while True:
    comment = generate_comment()
    serialized_message = comment.SerializeToString()

    producer.produce(
        topic=RAW_COMMENTS_TOPIC,
        key=comment.comment_id.encode(),
        value=serialized_message,
        callback=log
    )

    print(f"Sent Message: {comment}")

    message_count += 1

    if message_count % batch_size == 0:
        # kafka mesajları bufferda tutuyor normalde,
        # flush, bufferdakilerin brokera gönderilmesi için zorlar
        # bu sayede veri kaybının önüne geçilir.
        # bir nevi blocklama görevi görür, mesajlar iletilene kadar durdurur.
        producer.flush()
        print(f"Flushed {batch_size} messages to Kafka.")

    time.sleep(random.uniform(0.1, 10))
