import requests
from bs4 import BeautifulSoup
import os
from time import sleep
from random import randrange
from my_library import *
from pprint import pprint

def always_load():
    
        # изменение рабочего каталога
    file_name = os.path.basename(__file__)
    cwd = os.path.abspath(__file__).replace(file_name, '')
    os.chdir(cwd)

    global url, host, headers
    url = 'https://roscarservis.ru/catalog/legkovye/?arCatalogFilter_458_1500340406=Y&set_filter=Y&sort%5Brecommendations%5D=asc&PAGEN_1='
    
    host = '/'.join(url.split(sep='/', maxsplit=3)[:3])
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    folder = os.path.join('data')
    if not os.path.exists(folder):
        os.mkdir(folder)
    
    

@spent_time
def load_page_first():
    req = requests.get(url=f'{url}{1}', headers=headers)
    print(req)
    
    save_in_zip(req.json(), 'index.json', os.path.join('data', 'index.zip'))

@spent_time
def load_all_pages():
    src = load_from_zip(os.path.join('data', 'index.zip'))

    pageCount = src['pagesCount']
    pages_dict = {}
    
    for count in range(1, pageCount + 1):
        page = requests.get(url=f'{url}{count}', headers=headers)
        pages_dict[f'{count:03d}.json'] = page.json()
        print(f'loaded {count} page')
        sleep(1)
        if count%9 == 0:
            sleep(13)
    
    save_in_zip_update(
        pages_dict,
        os.path.join('data', 'all_pages_in_json.zip')
    )
        
def colected_data():
    pages_dict = load_from_zip_all(os.path.join('data', 'all_pages_in_json.zip'))
    
    busbar_dict = {}
    for item in list(pages_dict.values()):
        for busbar in (item['items']):
            commonStores = {}
            busbar_id = int(busbar['id'])
            for store in busbar['commonStores']:
                commonStores[store['STORE_NAME']] = int(store['AMOUNT'])
            if not commonStores:
                for bb in busbar['raznItems']:
                    if int(bb['id']) == busbar_id:
                        total_amount = int(bb['amount'])
                        break
                else:
                    total_amount = None
            else:
                total_amount = sum(commonStores.values())

            busbar_url = busbar.get('url', None)

            busbar_dict[int(busbar['id'])] = {
                    'name': busbar.get('name', None),
                    'price': busbar.get('price', None),
                    'total amount': total_amount,
                    'commonStores': commonStores,
                    'url': f'{host}{busbar_url}',
                }
    
    save_in_zip(
        busbar_dict,
        'busbars.json',
        os.path.join('data', 'busbars.zip')
    )
        
    # print(busbar_dict)
        
def test():
    pages_dict = load_from_zip_all(os.path.join('data', 'all_pages_in_json.zip'))
    
    for index, item in list(pages_dict.items())[:]:
        for busbar in (item['items'])[:]:
            busbar_id = int(busbar['id'])
            if 160022 == busbar_id:
                for bb in busbar['raznItems']:
                    if int(bb['id']) == busbar_id:
                        total_amount = int(bb['amount'])
                
                pprint(total_amount)
    
    
def main():
    always_load()
    # load_page_first()
    # load_all_pages()
    colected_data()
    # test()
    

if __name__ == '__main__':
    main()