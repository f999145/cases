import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random
from my_decorator import my_decorator

# изменение рабочего каталога
file_name = os.path.basename(__file__)
cwd = os.path.abspath(__file__).replace(file_name, '')
os.chdir(cwd)


# сохраним индексную страницу

url = 'http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
host = '/'.join(url.split(sep='/', maxsplit=3)[:3])

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

@my_decorator
def save_index_html():
    req = requests.get(url=url, headers=headers)
    src = req.text
    # print(src)

    if not os.path.isdir('data'):
        os.mkdir('data')
    
    with open('data/index.html', 'w', encoding='utf-8') as file:
        file.write(src)

@my_decorator
def save_all_categories_dict():
    with open('data/index.html', encoding='utf-8') as file:
        src = file.read()
    
    page = BeautifulSoup(src, 'html.parser')
    
    all_products_hrefs = page.find_all(class_="mzr-tc-group-item-href")
    all_categories_dict = {}
    
    for item in all_products_hrefs:
        # print(item)
        item_text = item.text
        item_href = host + item.get('href')
        all_categories_dict[item_text] = item_href
    
    with open('data/all_categories_dict.json', 'w', encoding='utf-8') as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

@my_decorator
def save_pages_all_category():
    with open('data/all_categories_dict.json', encoding='utf-8') as file:
        all_categories = json.load(file)
    
    if not os.path.isdir('data/cat_folder'):
        os.mkdir('data/cat_folder')
    
    count = 0
    for category_name, category_href in all_categories.items():
        rep =[', ', ' ', ',', '-', '\'']
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, '_')
        req = requests.get(url=category_href, headers=headers)
        src = req.text
        with open(f'data/cat_folder/{count:03d}_{category_name}.html', 'w', encoding='utf-8') as file:
            file.write(src)
            print(f'write \'{count:03d}_{category_name}.html\' completed')

        count += 1
        time.sleep(random.randrange(2,4))

@my_decorator
def main():
    print(os.path.isdir('data\cat_folder'))
    print(os.path.abspath('scraping.py'))
        
if __name__ == '__main__':
    main()