import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "lounge")
DB_USER = os.getenv("DB_USER", "lounge")
DB_PASSWORD = os.getenv("DB_PASSWORD", "lounge_password")
