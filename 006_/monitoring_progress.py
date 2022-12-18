import os, json
from config import tmp
from operations_with_paths import MakeDir
"""Тут описаны функции по созданию, контролю прогресса выполнения программы"""

"""
{
    этап1:{
        статус: выполнен
    }
    этап2:{
        статус: выполняется
        пагинация:26
    }
}
"""

def monitor_load(tmp: str = tmp, filename: str = 'monitor.json') -> dict:
    """загрузка из файла"""
    with open(file=os.path.join(tmp, filename), mode='r', encoding='utf-8') as file:
        return dict(json.load(file))
    
def monitor_save(data: dict, tmp: str = tmp, filename: str = 'monitor.json') -> None:
    """Сохранение данных в файл"""
    MakeDir(tmp)
    with open(file=os.path.join(tmp,filename), mode='w', encoding='utf-8') as file:
        json.dump(obj=data, fp=file, indent=4, ensure_ascii=False)

def monitro_make(tmp: str = tmp, filename: str = 'monitor.json') -> None:
    """Создание"""
    if not os.path.isfile(os.path.join(tmp, filename)):
        data = {
            'curstage': 'zero'
        }
        MakeDir(tmp)
        monitor_save(data, tmp)

def monitor_add(tmp: str = tmp, filename: str = 'monitor.json', **kwargs):
    print(tmp, kwargs)
    """дополнение"""
    

"""текущий этап"""

"""проверка"""

