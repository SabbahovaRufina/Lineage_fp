import asyncio
from sys import exit
from BD.DataBase import DataBase
from BD.Servers import Servers
from BD.Sellers import Sellers
from BD.Exchanges import Exchanges
import ParserFP.Funpay as Fp


async def get_info():
    site = Fp.Funpay()
    return await site.get_info_list()


async def main():
    bd = DataBase()
    servers = Servers('servers')
    sellers = Sellers('sellers')
    exchanges = Exchanges('exchanges', servers.name, sellers.name)

    try:
        await bd.drop_schema()
        await bd.create_schema()

        await servers.drop_table()
        await sellers.drop_table()
        await exchanges.drop_table()

        await servers.create_table()
        await sellers.create_table()
        await exchanges.create_table()

        for row in await get_info():
            await servers.insert_table(row)
            await sellers.insert_table(row)
            await exchanges.insert_table(row)

        return await exchanges.do_sql_servers()

    finally:
        bd.conn.close()


if __name__ == '__main__':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)

