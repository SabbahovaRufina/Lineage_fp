from tabulate import tabulate
import pandas as pd
import BD.main
import asyncio


async def get_df(data, columns):
    return pd.DataFrame(data, columns=columns)


async def get_table(df):
    return tabulate(df, headers=df.columns, tablefmt='grid')


async def write_to_txt(df):
    with open('lineage servers.txt', 'w', encoding='windows-1251') as txt:
        txt.write(df)


async def main():
    columns = ["сервер", "стоимость сервера", "кол-во валюты", "стоимость валюты", "кол-во продавцов",
               "сред. цена", "мода", "25 проц.", "медиана", "75 проц.", "мин. цена", "макс. цена", ]
    data = await BD.main.main()
    df = await get_df(data, columns)
    table = await get_table(df)
    await write_to_txt(table)


if __name__ == '__main__':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)

