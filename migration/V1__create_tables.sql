CREATE TABLE IF NOT EXISTS comment (
    id VARCHAR(255) PRIMARY KEY,
    content TEXT NOT NULL,
    sentiment VARCHAR(50) NOT NULL
);
