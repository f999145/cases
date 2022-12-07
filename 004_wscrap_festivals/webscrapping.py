import requests
from bs4 import BeautifulSoup
import os, re
from time import sleep
from random import randrange
from my_library import *

def always_load():
    
        # изменение рабочего каталога
    file_name = os.path.basename(__file__)
    cwd = os.path.abspath(__file__).replace(file_name, '')
    os.chdir(cwd)

    global url, host, headers
    url = ['https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=&to_date=&maxprice=500&o=','&bannertitle=May']
    host = '/'.join(url[0].split(sep='/', maxsplit=3)[:3])
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }

@spent_time
def save_short_list_pages():
    
    short_list_pages = {}
    
    count = 0
    while True:
        url_test = f'{count}'.join(url)
        req = requests.get(url=url_test, headers=headers)
        req_dict = json.loads(req.text)
        if ('No festivals found' in req_dict['html']):
            break
        short_list_pages[f'{count:03d}.html'] = req_dict['html']
        
        count += 24
        sleep(randrange(1,4))
        
    if not os.path.isdir('data'):
        os.mkdir('data') 
    
    save_in_zip_update(
        short_list_pages,
        os.path.join('data', 'short_list_pages.zip')
    )

@spent_time
def save_all_link():
    src_dict = load_from_zip_all(os.path.join('data', 'short_list_pages.zip'))
    link_list = []
    for item in list(src_dict.values()):
        
        src = BeautifulSoup(item, 'html.parser')
        links = src.find_all(class_ = 'card-details-link')
        for link in links:
            link_list.append(host + link.get('href'))
    
    link_list = (dict(enumerate(link_list)))
    save_in_zip(link_list, 'link_list.json', os.path.join('data', 'link_list.zip'))

@spent_time
def save_all_pages():
    link_list = load_from_zip(os.path.join('data', 'link_list.zip'))
    
    pages_dict = {}
    
    for index, link in enumerate(link_list):
        try:
            page = requests.get(url=link, headers=headers)
        except Exception as ex:
            print()
            print(f'{index:03d}  {ex}')
            continue
            
        page = page.text
        key = f'{index:03d}.html'
        
        pages_dict[key] = page
        print(f'{index:03d} is done')
        sleep(randrange(1,4))
    
    save_in_zip_update(pages_dict, os.path.join('data', 'page_dict.zip'))

def load_data_from_pages():
    pages_dict = load_from_zip_all(os.path.join('data', 'page_dict.zip'))
    
    festival_dict = {}
    
    for page in list(pages_dict.values()):
        page = BeautifulSoup(page, 'html.parser')
        
        title = page.find(class_='MuiTypography-root MuiTypography-body1 css-r2lffm')
        title = title.text.replace('  ', '').strip()
        
        
        
        data = page.find_all(class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-11 css-twt0ol')
        
        
        date = data[0]
        
        date = date.find_all('span')
        date = list(map(lambda x: x.text, date))
        date = ' '.join(date)
        date, year = tuple(map(lambda x: x.strip(), date.split(',', maxsplit=1)))

        place = data[1].text.replace('  ', '').strip()

        
        data = list(map(lambda x: x.text, data[:3]))
        if (len(set(data))) == 3:    
            price = data[2]
        else:
            price = None
        
        about = page.find('div', {'id': 'about'}).find('div').find('div').find_next_siblings()
        about = about[2].text.strip()
        about = about.replace('  ', ' ').replace('\n\n', '\n').replace('\n \n', '')
        
        festival_dict[title] = {
            'year': year,
            'date': date,
            'place': place,
            'price': price,
            'about': about
        }
        print(title, 'complete')
        
        
    save_in_zip(
        festival_dict,
        'festivals.json',
        os.path.join('data', 'festivals.zip')
    )
        
        
        
if __name__ == '__main__':
    always_load()
    # save_short_list_pages()
    # save_all_link()
    # save_all_pages()
    # load_data_from_pages()