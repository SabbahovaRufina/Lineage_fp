from BD.Table import Table


class Servers(Table):
    def __init__(self, name):
        super().__init__(name)

    async def create_table_sql(self):
        return f'''CREATE TABLE IF NOT EXISTS {self.schema}.{self.name} (
            server_id   BIGINT PRIMARY KEY,
            server_name TEXT NOT NULL
        );'''

    async def insert_sql(self, values):
        return f'''INSERT INTO {self.schema}.{self.name} (server_id, server_name)
        VALUES ({values[0]}, {values[1]})
        ON CONFLICT (server_id) DO NOTHING;'''

