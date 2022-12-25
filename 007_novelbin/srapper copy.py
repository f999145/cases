import requests
# from bs4 import BeautifulSoup as BS
import asyncio, aiohttp
from config import url, headers, pagin_url
from operations_with_paths import ChangeDir
import time
from parser import _pars_urls
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
    return tuple(_pars_urls(urls_page.text))

async def _worker(queue: asyncio.Queue):#, session: aiohttp.ClientSession):
    index, url = await queue.get()
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        response_text = await response.text()
        print(index)
        queue.task_done()
    return PageTuple(index, response_text)

# Создаем очередь, которую будем использовать
# для хранения рабочей нагрузки.    
def _queue(urls_list: tuple) -> asyncio.Queue[tuple[int, str]]:
    queue: asyncio.Queue[tuple[int, str]]  = asyncio.Queue()
    for op in list(enumerate(urls_list))[:7]:
        queue.put_nowait(op)
    return queue
    

async def get_pages_tasks(urls_list: tuple) -> tuple[PageTuple]:
    tasks = []
    queue = _queue(urls_list)
    # Создаем семь рабочие задачи для одновременной обработки очереди.
    for _ in range(7):
        # async with aiohttp.ClientSession() as session:
        task = asyncio.create_task(_worker(queue))
        tasks.append(task)
    
    # Запускаем обработку очереди и ожидаем, 
    # пока элементы не закончатся
    await queue.join()
     # После того как очередь израсходована
    # останавливаем задачи
    for task in tasks:
        task.cancel()
    # Ждем, остановку задач.
    pages = await asyncio.gather(*tasks, return_exceptions=True)
    return pages


def main():
    urls_list = _get_urls()
    asyncio.run(get_pages_tasks(urls_list))
    
    
if __name__ == '__main__':
    main()