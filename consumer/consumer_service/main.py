import asyncio
from .kafka_consumer import CommentConsumer
from .kafka_producer import CommentProducer
from .grpc_client import analyze_sentiment
from .db_client import AsyncDBClient


async def main():
    consumer = CommentConsumer()
    producer = CommentProducer()
    db_client = await AsyncDBClient.create()

    try:
        while True:
            msg = consumer.consumer.poll(1.0)
            if msg is None:
                await asyncio.sleep(0.1)
                continue
            if msg.error():
                print("Consumer error:", msg.error())
                continue

            comment = consumer.process_message(msg)
            if comment is None:
                continue

            sentiment = analyze_sentiment(comment)
            print(f"Sentiment for comment {comment.comment_id}: {sentiment}")

            producer.produce_processed_comment(comment, sentiment)

            await db_client.insert_comment(comment.comment_id, comment.content, sentiment)
    except KeyboardInterrupt:
        print("Consumer closed.")
    finally:
        consumer.consumer.close()
        producer.flush()
        await db_client.close()


if __name__ == '__main__':
    asyncio.run(main())
