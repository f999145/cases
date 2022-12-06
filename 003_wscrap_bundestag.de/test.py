import os
from my_library import *

file_name = os.path.basename(__file__)
cwd = os.path.abspath(__file__).replace(file_name, '')
os.chdir(cwd)

with ZipFile(os.path.join('data', 'individual_page.zip')) as zf:
    return_dict = {}
    for item in zf.filelist[:400]:
        with zf.open(item.filename) as f:
            data = f.read().decode('utf-8')
            _, file_extension = os.path.splitext(item.filename)
            if file_extension == '.json':
                data = json.loads(data)
            return_dict[item.filename] = data
    src_01 = return_dict

print(len(list(src_01.keys())))

with ZipFile(os.path.join('data', 'individual_page.zip')) as zf:
    return_dict = {}
    for item in zf.filelist[300:]:
        with zf.open(item.filename) as f:
            data = f.read().decode('utf-8')
            _, file_extension = os.path.splitext(item.filename)
            if file_extension == '.json':
                data = json.loads(data)
            return_dict[item.filename] = data
    src_02 = return_dict

print(len(list(src_02.keys())))

# save_in_zip_update(src_02, os.path.join('data', 'test.zip'))

# src = load_from_zip_all(os.path.join('data', 'test.zip'))
# print(len(list(src.keys())))


save_in_zip_update(
    src_01,
    os.path.join('data', 'test2.zip')
)
save_in_zip_update(
    src_02,
    os.path.join('data', 'test2.zip')
)
# print(list(src_01.items())[0][0])