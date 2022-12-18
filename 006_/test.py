from save_and_load import filetuple
from operations_with_paths import ChangeDir
import json
from monitoring_progress import monitor_save
from config import tmp
test1 =(
    filetuple('1', 'a1'),
    filetuple('2', 'a2'),
    filetuple('3', 'a3'),
    filetuple('4', 'a4'),
)
test2 =(
    filetuple('3', 'b3'),
    filetuple('4', 'b4'),
    filetuple('5', 'b5'),
    filetuple('1', 'b6'),
)


test3 = dict(test1)
test3.update(dict(test2))

ChangeDir()
monitor_save(test3)

print(tuple(filetuple(x, y) for x, y in  test3.items()))
# print(test3)
# print(tuple(test3.items()))