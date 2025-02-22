import asyncio
from aiokafka import AIOKafkaProducer
from .config import KAFKA_BROKER, PROCESSED_COMMENTS_TOPIC
from .generated.processed import Processed


class CommentProducer:
    def __init__(self, batch_size=10):
        self.producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
        self.batch_size = batch_size
        self.message_count = 0

    async def start(self):
        await self.producer.start()
        print("Kafka producer started.")

    async def produce_processed_comment(self, comment, sentiment):
        processed = Processed(
            comment_id=comment.comment_id,
            content=comment.content,
            sentiment=sentiment
        )
        serialized_message = processed.SerializeToString()
        try:
            await self.producer.send_and_wait(PROCESSED_COMMENTS_TOPIC, serialized_message)
        except Exception as e:
            print("Error sending message t Kafka:", e)

        self.message_count += 1

        if self.message_count % self.batch_size == 0:
            await self.producer.flush()

    async def flush_and_close(self):
        await self.producer.flush()
        await self.producer.stop()
