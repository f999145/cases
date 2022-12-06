import time
import os, json
from zipfile import ZipFile, ZIP_DEFLATED

def spent_time(func):
    """ Декорирующая функция
        Считает время затрачиваемое функцией на выполнение
    """
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        total = int(round(((end - start) * 1000), 0))
        print()
        if total < 1000:
            print(f'function "{func.__name__}" take: {total} ms')
        elif (total//1000) < 60:
            print(f'function "{func.__name__}" take: {total//1000:02d}:{total%1000:03d} sec')
        elif ((total//1000)//60) < 60:
            print(f'function "{func.__name__}" take: {(total//1000)//60:02d}:{(total//1000)%60:02d} min')
        else:
            print(f'function "{func.__name__}" take: {((total//1000)//60)//60}:{((total//1000)//60)%60:02d} h')
        print('-' * 20)
    return wrapper



def save_in_zip(file: str, filename: str, zipfilename: str):
    _, file_extension = os.path.splitext(filename)
    if file_extension == '.json':
        file = json.dumps(file, indent=4, ensure_ascii=False)
    with ZipFile(zipfilename, 'w', compression=ZIP_DEFLATED, compresslevel=1) as zf:
        zf.writestr(filename, file.encode())



def save_in_zip_all(file: dict, zipfilename: str):
    with ZipFile(zipfilename, 'w', compression=ZIP_DEFLATED, compresslevel=1) as zf:
        for key, value in file.items():
            _, file_extension = os.path.splitext(key)
            if file_extension == '.json':
                value = json.dumps(value, indent=4, ensure_ascii=False)
            zf.writestr(key, value.encode())
                


def save_in_zip_update(file: dict, zipfilename: str):
    if os.path.exists(zipfilename):
        dict_temp = load_from_zip_all(zipfilename)
        dict_temp.update(file)
        file = dict_temp
    save_in_zip_all(file, zipfilename)



def load_from_zip(zipfilename: str):
    with ZipFile(zipfilename) as zf:
        item = zf.filelist[0]
        filename = item.filename
        with zf.open(filename) as f:
            data = f.read().decode('utf-8')
            _, file_extension = os.path.splitext(filename)
            if file_extension == '.json':
                data = json.loads(data)
            return data



def load_from_zip_all(zipfilename: str) -> dict:
    return_dict = {}
    with ZipFile(zipfilename) as zf:
        for item in zf.filelist:
            with zf.open(item.filename) as f:
                data = f.read().decode('utf-8')
                _, file_extension = os.path.splitext(item.filename)
                if file_extension == '.json':
                    data = json.loads(data)
                return_dict[item.filename] = data
    return return_dict

if __name__ == '__main__':
    pass