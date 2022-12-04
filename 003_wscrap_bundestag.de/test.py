import os
from my_library import *

file_name = os.path.basename(__file__)
cwd = os.path.abspath(__file__).replace(file_name, '')
os.chdir(cwd)

dic1 = {'a': 1, 'b': 2, 'c': 3}
dic2 = {'d': 1, 'e': 2, 'f': 3}
dic = {}
dic['dic1.json'] = dic1
dic['dic2.json'] = dic2
# save_in_zip(dic1, 'dic.json', 'dic_zip.zip')
# save_in_zip_all(dic,'dic_zip.zip')


pp = load_from_zip_all('dic_zip.zip')
print(pp)