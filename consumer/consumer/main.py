from kafka_consumer import create_consumer, process_message
from grpc_client import analyze_sentiment
from kafka_producer import produce_processed_comment


def main():
    consumer = create_consumer()
    while True:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue

        comment = process_message(msg)
        if comment is None:
            continue

        sentiment = analyze_sentiment(comment)
        print(f"Sentiment for comment {comment.comment_id}: {sentiment}")
        produce_processed_comment(comment, sentiment)


if __name__ == '__main__':
    main()
