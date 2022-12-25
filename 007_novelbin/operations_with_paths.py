import os

def MakeDir(path_dir: str) -> None:
    """Проверка на наличие и создание директорий"""
    if not os.path.isdir(path_dir):
            os.makedirs(path_dir)

def GetPath(path_file: str) -> str:
    """Возвращает путь до папки с файлом"""
    file_name = os.path.basename(path_file)
    return os.path.abspath(path_file).replace(file_name, '')

def ChangeDir(path_dir: str | None = None) -> None:
    """Изменение рабочей директории"""
    os.chdir(GetPath(__file__))
    if path_dir:
        MakeDir(path_dir)
        os.chdir(path_dir)
