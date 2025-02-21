from .grpc_server import serve


def main():
    try:
        serve()
    except KeyboardInterrupt:
        print("Server stopped")


if __name__ == "__main__":
    main()
