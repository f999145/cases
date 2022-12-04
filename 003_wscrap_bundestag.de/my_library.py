import time
import os, json
from io import BytesIO
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



def save_in_zip(file: str, filename: str, zipfilename: str = 'default.zip'):
    _, file_extension = os.path.splitext(filename)
    if file_extension == '.json':
        file = json.dumps(file, indent=4, ensure_ascii=False)
    
    archive = BytesIO()
    with ZipFile(archive, 'w', compression=ZIP_DEFLATED, compresslevel=1) as zf:
        with BytesIO() as f:
            f.write(file.encode())
            zf.writestr(filename, f.getbuffer())
    
    with open(zipfilename, 'wb') as zf:
        zf.write(archive.getbuffer())



def save_in_zip_all(file: dict, zipfilename: str = 'default.zip'):
    archive = BytesIO()
    with ZipFile(archive, 'w', compression=ZIP_DEFLATED, compresslevel=1) as zf:
        for key, value in file.items():
            _, file_extension = os.path.splitext(key)
            if file_extension == '.json':
                value = json.dumps(value, indent=4, ensure_ascii=False)
            with BytesIO() as f:
                f.write(value.encode())
                zf.writestr(key, f.getbuffer())
    
    with open(zipfilename, 'wb') as zf:
        zf.write(archive.getbuffer())
                


def save_in_zip_add(file: dict, zipfilename: str = 'default.zip'):
    if os.path.exists(zipfilename):
        dict_temp = load_from_zip_all(zipfilename)
        dict_temp.update(file)
        file = dict_temp
    save_in_zip_all(file, zipfilename)



def load_from_zip(filename: str, zipfilename: str):
    with ZipFile(zipfilename) as zf:
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