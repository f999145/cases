url = 'https://www.labirint.ru/genres/2308/?available=1'
pagination = '&page='
ext = '&display=table'
current = None        # дирректория куда будут сохраться файлы проекта 
                        # (None - где находится исполняемый файл)
tmp = 'tmp'             # папка где будут хранитсья скаченные промежуточные данные
result = 'result'       # папка куда сохранятсья результаты
host = '/'.join(url.split(sep='/', maxsplit=3)[:3])
headers = {
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'x-content-type-options': 'nosniff',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}