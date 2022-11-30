import requests
from bs4 import BeautifulSoup
import os

# сохраним индексную страницу

url = 'http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}
def save_index_html():
    req = requests.get(url=url, headers=headers)
    src = req.text
    # print(src)

    if not os.path.isdir('data'):
        os.mkdir('data')
    
    with open('data/index.html', 'w', encoding='utf-8') as file:
        file.write(src)

def main():
    with open('data/index.html', encoding='utf-8') as file:
        src = file.read()
    
    page = BeautifulSoup(src, 'html.parser')
    all_products_hrefs = page.find_all(class_="mzr-tc-group-item-href")
    for item in all_products_hrefs[]:
        print(item)

if __name__ == '__main__':
    main()