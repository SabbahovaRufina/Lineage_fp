import psycopg2


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="parser_fp",
            user="postgres",
            password="5s5nd4q0",
            host="127.0.0.1",
            port="5432"
        )
        self.schema = "lineage"

    async def execute(self, sql):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(sql)

    async def drop_schema(self):
        await self.execute(f'''DROP SCHEMA IF EXISTS {self.schema} CASCADE;''')

    async def create_schema(self):
        await self.execute(f'''CREATE SCHEMA IF NOT EXISTS {self.schema};''')

