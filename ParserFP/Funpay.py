from bs4 import BeautifulSoup
from aiohttp.client_exceptions import ClientConnectorError
import aiohttp
import asyncio
import sys
import re


class Funpay:
    def __init__(self):
        self.main_page = 'https://funpay.com/chips/124/'

    async def get_soup(self):
        try:
            async with aiohttp.ClientSession(trust_env=True) as session:
                async with session.get(url=self.main_page) as response:
                    if response.reason == 'OK':
                        response.encoding = 'UTF-8'
                        soup = BeautifulSoup(await response.text(), 'lxml')
                        return soup
                    else:
                        print(f"Код ошибки: {response.reason}")
                        return None
        except ClientConnectorError:
            print("Ошибка")

    @staticmethod
    async def get_data_server(seller):
        return int(seller["data-server"])

    @staticmethod
    async def get_name_server(seller):
        name_server = str(seller.find("div", class_="tc-server hidden-xxs").text)
        substring = re.match(r'\((NA|RU) / EU (West|East)\) ', name_server).group(0)
        return "'"+name_server.replace(substring, '')+"'"

    @staticmethod
    async def get_data_online(seller):
        try:
            return bool(seller["data-online"])
        except KeyError:
            return bool(0)

    @staticmethod
    async def get_username(seller):
        return "'"+str(seller.find("div", class_="media-user-name").text.replace(' ', '').replace('\n', ''))+"'"

    @staticmethod
    async def get_amount(seller):
        return int(seller.find("div", class_="tc-amount").text.replace(' ', ''))

    @staticmethod
    async def get_price(seller):
        return float(seller.find("div", class_="tc-price").text[:-2])

    async def parser_info(self):
        soup = await self.get_soup()
        for seller in soup.find("div", class_="content-with-cd-wide showcase").find_all("a", class_="tc-item"):
            data_server = await self.get_data_server(seller)
            name_server = await self.get_name_server(seller)
            data_online = await self.get_data_online(seller)
            username = await self.get_username(seller)
            amount = await self.get_amount(seller)
            price = await self.get_price(seller)
            yield [data_server, name_server, data_online, username, amount, price]

    async def parser_info_test(self):
        soup = await self.get_soup()
        for seller in soup.find("div", class_="content-with-cd-wide showcase").find_all("a", class_="tc-item"):
            data_server = await self.get_data_server(seller)
            name_server = await self.get_name_server(seller)
            data_online = await self.get_data_online(seller)
            username = await self.get_username(seller)
            amount = await self.get_amount(seller)
            price = await self.get_price(seller)
            print(data_server, name_server, data_online, username, amount, price)

    async def get_info_list(self):
        return [x async for x in self.parser_info()]


async def main():
    site = Funpay()
    print(await site.parser_info_test())


if __name__ == '__main__':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)

