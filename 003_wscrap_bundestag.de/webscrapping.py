import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os, time, random
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from my_library import *

def always_load():
    # изменение рабочего каталога
    file_name = os.path.basename(__file__)
    cwd = os.path.abspath(__file__).replace(file_name, '')
    os.chdir(cwd)

    global url, host, headers
    url = 'https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset='
    host = '/'.join(url.split(sep='/', maxsplit=3)[:3])
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

@spent_time
def load_table_page():
    
    member_list = []
    
    count = 0
    while True:
        try:
            print(f'load get: {count}')
            req = requests.get(url=f'{url}{count}', headers=headers)
            if ('bt-slide-error' in req.text):
                print(f'load stop, count: {count-20}')
                break
        except Exception as ex:
            print(ex)
            print(f'load stop, count: {count-20}')
            break
        page = BeautifulSoup(req.text, 'html.parser')
        src_20 = page.find_all(class_= 'col-xs-4')
        for item in src_20:
            item = item.find(class_= 'bt-slide-content')
            item = item.find('a')
            
            name = str(item.get('title').strip())
            name = name.split(', ')
            name = {
                'surname': name[0],
                'name': name[1]
            }
            
            href = item.get('href')
            
            item = item.find(class_= 'bt-bild-info-text').find_all('p')
            info = item[-1].text.strip()
            
            member_list.append({
                'name': name,
                'info': info,
                'href': href
            })
        
        
        count += 20
        time.sleep(random.randrange(1,3))
        
    
    if not os.path.isdir('data'):
        os.mkdir('data')

    save_in_zip(
        member_list,
        'member_list.json',
        os.path.join('data', 'member_list.zip')
        )

@spent_time
def load_individual_page():
    # на будующее, необходимо создать id ключ что бы можно было мержить файлы
    src = load_from_zip(
        'member_list.json',
        os.path.join('data', 'member_list.zip')
    )
    
    individual_page_dict = {}
    
    for index, item in enumerate(src):
        name = ' '.join(list(item['name'].values()))
        name = f'{index:03d}_{name}.html'
        try:
            page = requests.get(url=item['href'])
        except Exception as ex:
            print(f'\t{ex}')
            print(f'Erore \'{name}\'')

        individual_page_dict[name] = page.text
        print(f'page: \'{name}\' loaded')
        time.sleep(random.randrange(1,3))

    save_in_zip_update(
        individual_page_dict,
        os.path.join('data', 'individual_page.zip')
        )

@spent_time
def load_info_of_members():
    members_list = load_from_zip('member_list.json', os.path.join('data', 'member_list.zip'))
    members_page = load_from_zip_all(os.path.join('data', 'individual_page.zip'))
    
    for index, item in enumerate(members_list[:10]):
        name = item['name']
        info = item['info']
        key = ' '.join(list(item['name'].values()))
        key = f'{index:03d}_{key}.html'
        
        src = BeautifulSoup(members_page[key], 'html.parser')
        party = src.find(class_='bt-biografie-name').find('h3')
        post = party.find_next_sibling()
        party = party.text.split(',')[-1].strip()
        post = post.text.strip()
        print(party)
        # print(f'{name} -> {info}')
    
if __name__ == '__main__':
    always_load()
    # load_table_page()
    # load_individual_page()
    load_info_of_members()