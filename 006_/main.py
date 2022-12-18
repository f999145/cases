# import os
from operations_with_paths import ChangeDir
from config import url, pagination, current, tmp, result



"""
Структура:
    Конфиг.ини содержащий информацию:
        юрл
        хост
    json- о выполненых этапах и сохранении полезных данных
        функция обновления данных
        Сохранения
        Загрузки
        Проверки этапов выполнения
    обновление до рабочей директории
    Сохранить все страницы с книгами
        Можно получить количество страниц
    Собрать все карты книг в список
    
"""

def main():
    ChangeDir(current)
    

if __name__ == '__main__':
    main()