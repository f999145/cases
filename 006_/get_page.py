from config import url, ext, headers, tmp, pagination
from os.path import  join as os_path_join
from requests import get as requests_get
from bs4 import BeautifulSoup as BS
from monitoring_progress import monitor_add, monitor_check, monitor_control, monitor_load_args
from save_and_load import filetuple, save_in_zip, save_in_zip_update
import asyncio
import aiohttp
from decor import spent_time

@spent_time
def get_page_pagination(url: str = url, headers: dict = headers) -> None:
    monitor_add(name='get_page_pagination')
    monitor = monitor_control(name='get_page_pagination')
    if monitor.name and not monitor.completed:
        page = requests_get(url=url, headers=headers)
        status = save_in_zip(filetuple('page_pagination.html', page.text),
                             os_path_join(tmp, 'page_pagination.zip'))
        if status:
            monitor_check(name='get_page_pagination')

@spent_time
def get_pages(
    url: str = url, 
    pagination: str = pagination, 
    headers: dict = headers) -> bool:
    """Скачиваем страницы с помощью одноподочного запроса
    и сохраняем их в зип файл"""
    monitor_add(name='get_pages')
    monitor = monitor_control(name='get_pages')
    arument = monitor_load_args('get_pagination')
    pagin = arument.get('pagin', 0)
    if monitor.name and not monitor.completed:
        pages = []
        for index in range(1, pagin+1):
            page = requests_get(url=f'{url}{pagination}{index}{ext}', headers=headers)
            pages.append(filetuple(f'{index:03d}.html',page.text))
        status = save_in_zip_update(tuple(pages),os_path_join(tmp, 'pages.zip'))
        if status:
            monitor_check(name='get_pages')
            return True
    return False

async def _get_pages_async(
    session: aiohttp.ClientSession,
    pagin: int,
    url: str = url, 
    pagination: str = pagination, 
    headers: dict = headers):
    pag_url = f'{url}{pagination}{pagin}{ext}'
    
    async with session.get(url=pag_url, headers=headers) as response:
        response_text = await response.text()
    return response_text


async def _get_pages_tasks(
    url: str = url, 
    pagination: str = pagination, 
    headers: dict = headers) -> bool:
    monitor_add('get_pages')
    monitor = monitor_control('get_pages')
    arument = monitor_load_args('get_pagination')
    pagin = arument.get('pagin', 0)
    if monitor.name and not monitor.completed:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for index in range(1, pagin+1):
                task = asyncio.create_task(_get_pages_async(session=session,
                                                            pagin=index, 
                                                            url=url, 
                                                            pagination=pagination,
                                                            headers=headers))
                tasks.append(task)
            pages = await asyncio.gather(*tasks)
        pages = tuple(map(lambda x:  filetuple(f'{x[0]:03d}.html', x[1]), enumerate(pages)))
        status = save_in_zip_update(tuple(pages),os_path_join(tmp, 'pages.zip'))
        if status:
            monitor_check('get_pages')
            return True
    return False

@spent_time
def run_page_async(url: str = url, 
    pagination: str = pagination, 
    headers: dict = headers):
    asyncio.run(_get_pages_tasks(url, pagination, headers))