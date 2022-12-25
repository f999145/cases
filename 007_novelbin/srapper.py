import requests
from bs4 import BeautifulSoup as BS
import asyncio, aiohttp
from config import url, headers, pagin_url
from operations_with_paths import ChangeDir
import time
from parser import get_urls
from typing import NamedTuple

class PageTuple(NamedTuple):
    i: int
    page: str

def _get_urls() -> tuple:
    count = 0
    while True:
        urls_page = requests.get(url=pagin_url,headers=headers)
        if int(urls_page.status_code) == 200:
            break
        print('Что-то пошло не так!')
        print('\t\tНе загрузилась страница с адресами')
        print(f'Попытка {count+1}')
        if count < 5:
            count += 1
        else:
            exit()
        time.sleep(3)
    return tuple(get_urls(urls_page.text))

async def _get_page(option: tuple, session: aiohttp.ClientSession) -> PageTuple:
    index, url = option
    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
    return PageTuple(index, response_text)
    

async def get_pages_tasks(urls_list: tuple):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for op in list(enumerate(urls_list))[:1]:
            tasks = asyncio.create_task()



def main():
    urls_list = _get_urls()
    
    
if __name__ == '__main__':
    main()