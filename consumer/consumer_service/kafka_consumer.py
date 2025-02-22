import asyncio
from aiokafka import AIOKafkaConsumer
from .config import KAFKA_BROKER, RAW_COMMENTS_TOPIC
from .generated.comment import Comment

class CommentConsumer:
    def __init__(self):
        self.consumer = AIOKafkaConsumer(
            RAW_COMMENTS_TOPIC,
            bootstrap_servers=KAFKA_BROKER,
            group_id="comment_processor_group",
            auto_offset_reset="earliest"
        )

    async def start(self):
        await self.consumer.start()
        print("Kafka Consumer started.")

    async def consume_messages(self):
        try:
            async for msg in self.consumer:
                comment = self.process_message(msg)
                yield comment
        finally:
            await self.consumer.stop()

    def process_message(self, msg):
        comment = Comment().parse(msg.value)
        print(f"Received Comment:\n  ID: {comment.comment_id}\n  Content: {comment.content}")
        return comment

    async def close(self):
        await self.consumer.stop()
