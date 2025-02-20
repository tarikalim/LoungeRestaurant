from consumer.kafka_consumer import CommentConsumer
from consumer.kafka_producer import CommentProducer
from grpc_client import analyze_sentiment


def main():
    consumer = CommentConsumer()
    producer = CommentProducer()

    try:
        while True:
            msg = consumer.consumer.poll(1.0)
            if msg is None:
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
    except KeyboardInterrupt:
        print(" Consumer closed.")
    finally:
        consumer.consumer.close()
        producer.flush()


if __name__ == '__main__':
    main()
