from BD.DataBase import DataBase


class Table(DataBase):
    def __init__(self, name):
        super().__init__()
        self.name = name

    async def drop_table_sql(self):
        return f'''DROP TABLE IF EXISTS {self.schema}.{self.name} CASCADE'''

    async def create_table_sql(self):
        return f''' '''

    async def insert_sql(self, values):
        return f''' '''

    async def truncate_sql(self):
        return f'''TRUNCATE {self.schema}.{self.name} CASCADE;'''

    async def select_all_sql(self):
        return f'''SELECT * from {self.schema}.{self.name};'''

    async def drop_table(self):
        await self.execute(await self.drop_table_sql())

    async def create_table(self):
        await self.execute(await self.create_table_sql())

    async def insert_table(self, values):
        await self.execute(await self.insert_sql(values))

    async def truncate_table(self):
        await self.execute(await self.truncate_sql())

    async def select_all_from_table(self):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(await self.select_all_sql())
                return cur.fetchall()

