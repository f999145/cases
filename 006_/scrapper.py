from config import tmp, host, result
from os.path import  join as os_path_join
from bs4 import BeautifulSoup as BS
from monitoring_progress import monitor_add, monitor_check, monitor_control
from save_and_load import load_from_zip, load_from_zip_all
from operations_with_paths import MakeDir
import pandas as pd
from decor import spent_time


@spent_time
def get_pagination() -> int:
    monitor_add(name='get_pagination', pagin=0)
    monitor = monitor_control(name='get_pagination')
    if monitor.name and not monitor.completed:
        page = load_from_zip(os_path_join(tmp, 'page_pagination.zip'))
        soup = BS(page.content, 'html.parser')
        pagin = soup.find('div', class_="pagination-number")
        pagin = pagin.find('div', class_="pagination-number__right")
        pagin = pagin.find('a', class_="pagination-number__text")
        pagin = int(pagin.text)
        monitor_check(name='get_pagination', pagin=pagin)
        return pagin
    return 0

@spent_time
def get_info_book():
    monitor_add('info_book')
    monitor = monitor_control('info_book')
    if monitor.name and not monitor.completed:
        pages = load_from_zip_all(os_path_join(tmp, 'pages.zip'))
        books_df = pd.DataFrame()
        for page in pages:
            src = BS(page.content, 'html.parser')
            body = src.find('tbody')
            books = body.find_all('tr')
            for book in books:
                temp = _get_data_of_book(book)
                books_df = pd.concat([books_df, temp], ignore_index=True, sort=False)
        save_bool = _save_df(books_df, result)        
        if save_bool:
            monitor_check('info_book')


def _get_data_of_book(book: BS) -> pd.DataFrame:
    try:
        title = book.find('a', class_='book-qtip').get('title').strip()
    except:
        title = 'НЕТ НАЗВАНИЯ'
    
    try:
        link = host+book.find('a', class_='book-qtip').get('href')
    except:
        link = 'НЕТ ССЫЛКИ'
    
    try:
        autor = book.find('td', class_="col-sm-2").find('a').text.strip()
    except:
        autor = 'НЕТ АВТОРА'
    
    try:
        autor_link = host + book.find('td', class_="col-sm-2").find('a').get('href')
    except:
        autor_link = 'НЕТ ССЫЛКИ НА АВТОРА'
    
    try:
        pubhouse = book.find('td', class_='products-table__pubhouse').find('a').text.strip()
    except:
        pubhouse = 'НЕТ ИЗДАТЕЛЯ'
    
    try:
        price = book.find('td', class_='products-table__price').find('span', class_='price-val').find('span')
        price = int(str(price.text).strip().replace(' ',''))
    except:
        price = 0
    
    try:
        price_old = book.find('td', class_='products-table__price').find('span', class_='price-old').find('span')
        price_old = int(str(price_old.text).strip().replace(' ',''))
    except:
        price_old = 0
    
    temp = pd.DataFrame({
        'Название':[title],
        'Ссылка':[link],
        'Автор':[autor],
        'Ссылка на автора':[autor_link],
        'Издательство':[pubhouse],
        'Текущая цена':[price],
        'Старая цена':[price_old]
    })
    
    return temp



def _save_df(df: pd.DataFrame, result: str) -> bool:
    compression_opts = dict(method='zip', archive_name='books.csv')
    MakeDir(result)
    df.to_csv(
        os_path_join(result, 'books.zip'), 
        index=False,
        compression=compression_opts
        )
    return True