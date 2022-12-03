import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os, time, random
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from my_decorator import my_decorator

def always_load():
    # изменение рабочего каталога
    file_name = os.path.basename(__file__)
    cwd = os.path.abspath(__file__).replace(file_name, '')
    os.chdir(cwd)

    global url, host, headers
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

    if not os.path.isdir('data'):
        os.mkdir('data')
    
    # создаем буфер в оперативной памяти, где будем формировать зип файл
    archive = BytesIO()
    
    # создаем в этом буфере зип-файл на запись
    with ZipFile(archive, 'w', compression=ZIP_DEFLATED, compresslevel=1) as file:
        # создаем еще один буфер и открываем его на запись
        with BytesIO() as html_buf:
            # записываем в него данные в двоичном коде
            html_buf.write(src.encode())
            # Записываем буфер с файлом в буфер фип-файла
            file.writestr('index.html', html_buf.getbuffer())
    
    # Записываем буфер зип-файла в файл в бинарном режиме
    with open(os.path.join('data', 'index_zip_file.zip'), 'wb') as file:
        file.write(archive.getbuffer())

@my_decorator
def save_all_categories_dict():
    
    with ZipFile(os.path.join('data', 'index_zip_file.zip')) as zfile:
        with zfile.open('index.html') as file:
            src = file.read().decode('utf-8')
    
    page = BeautifulSoup(src, 'html.parser')
    all_products_hrefs = page.find_all(class_="mzr-tc-group-item-href")
    
    all_categories_dict = {}
    
    for item in all_products_hrefs:
        item_text = item.text
        item_href = host + item.get('href')
        all_categories_dict[item_text] = item_href
    
    
    archive = BytesIO()
    
    with ZipFile(archive, 'w', compression=ZIP_DEFLATED, compresslevel=1) as file:
        with BytesIO() as json_buf:
            data = json.dumps(all_categories_dict, indent=4, ensure_ascii=False)
            json_buf.write(data.encode())
            file.writestr('all_categories_dict.json', json_buf.getbuffer())
    
    with open(os.path.join('data', ' all_categories_dict.zip'), 'wb') as file:
        file.write(archive.getbuffer())
        

@my_decorator
def save_pages_all_category():
    
    with ZipFile(os.path.join('data', ' all_categories_dict.zip')) as zfile:
        with zfile.open('all_categories_dict.json') as file:
            data = file.read().decode('utf-8')
            all_categories = json.loads(data)
    
    count = 0
    archive = BytesIO()
    
    for category_name, category_href in all_categories.items():
        
        rep =[', ', ' ', ',', '-', '\'']
        
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, '_')
                
        req = requests.get(url=category_href, headers=headers)
        src = req.text
        
        with ZipFile(archive, 'a', compression=ZIP_DEFLATED, compresslevel=1) as zfile:
            with BytesIO() as html_buf:
                html_buf.write(src.encode())
                zfile.writestr(
                    f'{count:03d}_{category_name}.html',
                    html_buf.getbuffer()
                )
        
        print(f'write \'{count:03d}_{category_name}.html\' completed')
        count += 1
        time.sleep(random.randrange(2,4))
    
    with open(os.path.join('data', ' all_categories_pages.zip'), 'wb') as file:
        file.write(archive.getbuffer())



@my_decorator
def create_table():
    category_page_dict = {}
    health_diet_base_of_food = pd.DataFrame()
    products_json_var1 = {}
    products_json_var2 = []
    
    with ZipFile(os.path.join('data', ' all_categories_pages.zip')) as z:
        for item in z.filelist:
            with z.open(item.filename) as f:
                name = item.filename[4:-5]
                category_page_dict[name] = (f.read().decode('utf-8'))
                
    count = 0          
    for category, item in (category_page_dict.items()):
        
        page = BeautifulSoup(item, 'html.parser')

        try:
            table = page.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
        except Exception as ex:
            print(f'{count:02d} {category} ОШИБКА')
            print('   ', ex)
            count += 1
            continue
        
        products_json_var1[category] = {}
        
        for item in table:
            
            product = (item.find_all('td'))
            
            tmp = pd.DataFrame({
                'Категория': [category],
                'Продукт': [product[0].text.strip()],
                'Калорийность': [product[1].text.strip()],
                'Белки': [product[2].text.strip()],
                'Жиры': [product[3].text.strip()],
                'Углеводы': [product[4].text.strip()]
            })
            
            products_json_var1[category][product[0].text.strip()] = {
                'Калорийность': product[1].text.strip(),
                'Белки': product[2].text.strip(),
                'Жиры': product[3].text.strip(),
                'Углеводы': product[4].text.strip()
            }
            
            products_json_var2.append({
                'Категория': category,
                'Продукт': product[0].text.strip(),
                'Калорийность': product[1].text.strip(),
                'Белки': product[2].text.strip(),
                'Жиры': product[3].text.strip(),
                'Углеводы': product[4].text.strip()
            })
            
            health_diet_base_of_food = pd.concat(
                                                [health_diet_base_of_food, tmp],
                                                ignore_index=True,
                                                sort=False
                                            )

        print(f'{count:02d} \"{category}\" добавлен')
        count += 1
    
    
    dir = os.path.join('data', 'results')
    if not os.path.isdir(dir):
        os.mkdir(dir)
    
    
    archive = BytesIO()
    
    with ZipFile(archive, 'w', compression=ZIP_DEFLATED, compresslevel=1) as z:
        with BytesIO() as json_hub:
            data = json.dumps(products_json_var1, indent=4, ensure_ascii=False)
            json_hub.write(data.encode())
            z.writestr('products_json_var1.json', json_hub.getbuffer())
    
    with open(os.path.join('data', 'results', 'products_json_var1.zip'), 'wb') as file:
        file.write(archive.getbuffer())
    
    
    archive = BytesIO()
    
    with ZipFile(archive, 'w', compression=ZIP_DEFLATED, compresslevel=1) as z:
        with BytesIO() as json_hub:
            data = json.dumps(products_json_var2, indent=4, ensure_ascii=False)
            json_hub.write(data.encode())
            z.writestr('products_json_var2.json', json_hub.getbuffer())
    
    with open(os.path.join('data', 'results', 'products_json_var2.zip'), 'wb') as file:
        file.write(archive.getbuffer())
    
    
    compression_opts = dict(method='zip', archive_name='products.csv')
    health_diet_base_of_food.to_csv(
        os.path.join('data', 'results', 'products.zip'), 
        index=False,
        compression=compression_opts
        )
        
        
if __name__ == '__main__':
    always_load()
    # save_index_html()
    # save_all_categories_dict()
    # save_pages_all_category()
    # create_table()