import asyncio
from .grpc_client import analyze_sentiment
from .kafka_consumer import CommentConsumer
from .kafka_producer import CommentProducer
from .db_client import AsyncDBClient


async def main():
    consumer = CommentConsumer()
    producer = CommentProducer()
    db_client = await AsyncDBClient.create()

    await consumer.start()
    await producer.start()

    try:
        async for comment in consumer.consume_messages():
            sentiment = await analyze_sentiment(comment)
            print(f"Sentiment for comment {comment.comment_id}: {sentiment}")

            await producer.produce_processed_comment(comment, sentiment)

            await db_client.insert_comment(comment.comment_id, comment.content, sentiment)
    except KeyboardInterrupt:
        print("Consumer closed.")
    finally:
        await producer.flush_and_close()
        await db_client.close()


if __name__ == '__main__':
    asyncio.run(main())
