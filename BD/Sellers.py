from BD.Table import Table


class Sellers(Table):
    def __init__(self, name):
        super().__init__(name)

    async def create_table_sql(self):
        return f'''CREATE TABLE IF NOT EXISTS {self.schema}.{self.name} (
            seller_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            seller_name TEXT NOT NULL,
            seller_online BOOLEAN NOT NULL,
            CONSTRAINT "seller_unique" UNIQUE (seller_name)
            );'''

    async def insert_sql(self, values):
        return f'''INSERT INTO {self.schema}.{self.name} (seller_name, seller_online)
        SELECT {values[3]}, {values[2]}
        WHERE NOT EXISTS (
            SELECT 1
            FROM {self.schema}.{self.name}
            WHERE
                seller_name = {values[3]}
            LIMIT 1
        );'''

    async def insert_sql2(self, values):
        return f'''INSERT INTO {self.schema}.{self.name} (seller_name, seller_online)
        VALUES ({values[3]}, {values[2]})
        ON CONFLICT (seller_name) DO NOTHING;'''

    async def insert_sql1(self, values):
        return f'''IF EXISTS (SELECT * FROM {self.schema}.{self.name} WHERE seller_name = {values[3]})
        UPDATE {self.schema}.{self.name} SET seller_online = {values[2]} WHERE seller_name = {values[3]}
        ELSE
        INSERT INTO {self.schema}.{self.name} (seller_name, seller_online) VALUES ({values[3]}, {values[2]})
        END IF;'''

