from BD.Table import Table


class Exchanges(Table):
    def __init__(self, name, servers, sellers):
        super().__init__(name)
        self.servers = servers
        self.sellers = sellers

    async def create_table_sql(self):
        return f'''CREATE TABLE IF NOT EXISTS {self.schema}.{self.name} (
        offer_id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
        server_id BIGINT,
        seller_id BIGINT,
        amount BIGINT NOT NULL,
        price NUMERIC NOT NULL,
        CONSTRAINT "FK_exchanges_server" 
            FOREIGN KEY (server_id) REFERENCES {self.schema}.{self.servers} (server_id) ON DELETE CASCADE,
        CONSTRAINT "FK_exchanges_seller"
            FOREIGN KEY (seller_id) REFERENCES {self.schema}.{self.sellers} ON DELETE CASCADE
            );'''

    async def insert_sql(self, values):
        return f'''INSERT INTO {self.schema}.{self.name} (server_id, seller_id, amount, price)
        VALUES ({values[0]}, (SELECT seller_id FROM {self.schema}.{self.sellers} WHERE seller_name = {values[3]}), {values[4]}, {values[5]});'''

    async def get_sql_query_sellers(self):
        return f'''
        SELECT server_name, amount, price::float
        FROM {self.schema}.{self.name} AS offer 
        INNER JOIN {self.schema}.{self.sellers} AS sel ON offer.seller_id = sel.seller_id
        INNER JOIN {self.schema}.{self.servers} AS serv ON offer.server_id = serv.server_id
        WHERE seller_name = 'Cybertrade';'''

    async def get_sql_query_servers(self):
        return f'''
        SELECT server_name, 
        SUM(amount*price)::BIGINT, 
        SUM(amount)::BIGINT,
        ROUND(SUM(amount*price)/SUM(amount), 2)::FLOAT,
        COUNT(seller_name),  
        ROUND(AVG(price), 2)::FLOAT, 
        mode() WITHIN GROUP (ORDER BY price)::FLOAT, 
        ROUND(percentile_cont(0.25) WITHIN GROUP (ORDER BY price)::NUMERIC, 2)::FLOAT,
        ROUND(percentile_cont(0.5) WITHIN GROUP (ORDER BY price)::NUMERIC, 2)::FLOAT,
        ROUND(percentile_cont(0.75) WITHIN GROUP (ORDER BY price)::NUMERIC, 2)::FLOAT,
        MIN(price)::FLOAT, 
        MAX(price)::FLOAT
        FROM {self.schema}.{self.name} AS offer 
        INNER JOIN {self.schema}.{self.sellers} AS sel ON offer.seller_id = sel.seller_id
        INNER JOIN {self.schema}.{self.servers} AS serv ON offer.server_id = serv.server_id
        WHERE amount BETWEEN 1500 AND 30000 AND price BETWEEN 0.9 AND 4
        GROUP BY server_name
        ORDER BY 2 DESC;'''

    async def do_sql_servers(self):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(await self.get_sql_query_servers())
                return cur.fetchall()

    async def do_sql_sellers(self):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(await self.get_sql_query_sellers())
                return cur.fetchall()

