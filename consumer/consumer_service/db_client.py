import aiomysql
import asyncio
from .config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class AsyncDBClient:
    def __init__(self, pool):
        self.pool = pool
        self.queue = asyncio.Queue()
        self.writer_task = asyncio.create_task(self._db_writer())

    @classmethod
    async def create(cls):
        pool = await aiomysql.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            db=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        print("Database connection pool established.")
        return cls(pool)

    async def _db_writer(self):
        while True:
            comment_data = await self.queue.get()
            try:
                await self._insert_comment(*comment_data)
            except Exception as e:
                print(f"DB insert error: {e}")
            finally:
                self.queue.task_done()

    async def _insert_comment(self, comment_id, content, sentiment):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = "INSERT INTO comment (id, content, sentiment) VALUES (%s, %s, %s)"
                try:
                    await cursor.execute(query, (comment_id, content, sentiment))
                    await conn.commit()
                    print(f"Inserted comment with id: {comment_id}")
                except Exception as err:
                    print("Error inserting comment:", err)
                    await conn.rollback()

    async def insert_comment(self, comment_id, content, sentiment):

        await self.queue.put((comment_id, content, sentiment))

    async def close(self):
        await self.queue.join()
        self.writer_task.cancel()
        self.pool.close()
        await self.pool.wait_closed()
        print("Database connection closed.")
