from producer.producer import CommentProducer


def main():
    producer = CommentProducer()
    try:
        producer.produce_messages()
    except KeyboardInterrupt:
        print("Ctrl+C pressed")


if __name__ == '__main__':
    main()
