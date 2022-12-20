from os.path import join, isfile
import json
from config import tmp
from operations_with_paths import MakeDir
from typing import NamedTuple
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
class monitor_inf(NamedTuple):
    name: bool
    completed: bool


def _monitor_load(tmp: str, filename: str = 'monitor.json') -> dict:
    """загрузка из файла"""
    with open(file=join(tmp, filename), mode='r', encoding='utf-8') as file:
        return dict(json.load(file))
    
def _monitor_save(data: dict, tmp: str, filename: str = 'monitor.json') -> None:
    """Сохранение данных в файл"""
    MakeDir(tmp)
    with open(file=join(tmp,filename), mode='w', encoding='utf-8') as file:
        json.dump(obj=data, fp=file, indent=4, ensure_ascii=False)

def _monitor_make(tmp: str, filename: str = 'monitor.json') -> None:
    """Создание"""
    if not isfile(join(tmp, filename)):
        monitor = {
            'curstage': False
        }
        MakeDir(tmp)
        _monitor_save(monitor, tmp, filename)

def monitor_add(
    name: str | None = None,
    tmp: str =  tmp,
    filename: str = 'monitor.json',
    **kwargs) -> bool:
    """Добавление этапа в монитор"""
    _monitor_make(tmp, filename)
    if name:
        monitor = _monitor_load(tmp, filename)
        if _monitor_if(monitor, name):
            monitor = _monitor_mod(name, monitor, kwargs)
            _monitor_save(monitor, tmp, filename)
            return True
    return False
        
def _monitor_if(monitor: dict, name: str) -> bool:
    if monitor.get(monitor['curstage'], {}).get('completed', False):
        if not name == monitor['curstage']:
            return True
    if not monitor['curstage']:
        return True
    return False
        
def monitor_control(name: str, tmp: str = tmp, filename: str = 'monitor.json') -> monitor_inf:
    monitor = _monitor_load(tmp, filename)
    if name == monitor['curstage']:
        return monitor_inf(True, monitor.get(name, {}).get('completed', False))
    return monitor_inf(False, monitor.get(name, {}).get('completed', False))

    
def _monitor_mod(name: str, monitor: dict,  kwargs: dict | None = None) -> dict:
    monitor[name] = {
        'completed': False,
    }
    monitor['curstage'] = name
    if kwargs:
        monitor[name].update(kwargs)
    return monitor


def monitor_check(
    name: str | None = None,
    tmp: str = tmp,
    filename: str = 'monitor.json',
    **kwargs) -> bool:
    monitor = _monitor_load(tmp, filename)
    monitor[name]['completed'] = True
    if kwargs:
        monitor[name].update(kwargs)
    _monitor_save(monitor, tmp, filename)
    return True

def monitor_load_args(
    name: str | None = None,
    tmp: str = tmp,
    filename: str = 'monitor.json') -> dict:
    monitor = _monitor_load(tmp, filename)
    return monitor.get(name, False)
        
