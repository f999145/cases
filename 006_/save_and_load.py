import os, json
from zipfile import ZipFile, ZIP_DEFLATED
from typing import NamedTuple
from operations_with_paths import GetPath, MakeDir


class filetuple(NamedTuple):
    filename: str
    content: str


def _dict_to_str(file: filetuple) -> filetuple:
    _, file_extension = os.path.splitext(file.filename)
    if file_extension == '.json':
        data = json.dumps(file, indent=4, ensure_ascii=False)
        return filetuple(file.filename, data)
    return file


def _str_to_dict(file: filetuple) -> filetuple:
    _, file_extension = os.path.splitext(file.filename)
    if file_extension == '.json':
        data = json.loads(file.content)
        return filetuple(file.filename, data)
    return file


def save_in_zip(file: filetuple, zipfilename: str) -> None:
    MakeDir(GetPath(zipfilename))
    file = _dict_to_str(file)
    with ZipFile(zipfilename, 'w', compression=ZIP_DEFLATED, compresslevel=1) as zf:
        zf.writestr(file.filename, file.content.encode())


def save_in_zip_all(files: tuple[filetuple, ...], zipfilename: str) -> None:
    MakeDir(GetPath(zipfilename))
    with ZipFile(zipfilename, 'w', compression=ZIP_DEFLATED, compresslevel=1) as zf:
        for file in files:
            file = _dict_to_str(file)
            zf.writestr(file.filename, file.content.encode())
                

def save_in_zip_update(file: tuple[filetuple, ...], zipfilename: str) -> None:
    if os.path.exists(zipfilename):
        temp = load_from_zip_all(zipfilename)
        dict_temp = dict(temp)
        dict_temp.update(dict(file))
        file = tuple(filetuple(x, y) for x, y in dict_temp.items())
    MakeDir(GetPath(zipfilename))
    save_in_zip_all(file, zipfilename)


def load_from_zip(zipfilename: str) -> filetuple:
    with ZipFile(zipfilename) as zf:
        item = zf.filelist[0]
        filename = item.filename
        with zf.open(filename) as f:
            data = f.read().decode('utf-8')
            file = _str_to_dict(filetuple(f.name, data))
            return file


def load_from_zip_all(zipfilename: str) -> tuple[filetuple, ...]:
    return_list = []
    with ZipFile(zipfilename) as zf:
        for item in zf.filelist:
            with zf.open(item.filename) as f:
                data = f.read().decode('utf-8')
                file = _str_to_dict(filetuple(f.name, data))
                return_list.append(file)
    return tuple(return_list)

if __name__ == '__main__':
    pass