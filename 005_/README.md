
json get запрос
(https://www.youtube.com/watch?v=8LJllhrVJVw)

асихронный запрос
(https://youtu.be/ITELa7JaDm4)
(https://youtu.be/87A1Rq0CGtE)

обработка ошибок srapping
(https://youtu.be/v0ifLIUTHUs)

скачиваем картинки
(https://youtu.be/-T1_JG_qa-s)

# 004. Сводные данные о фестивалях


### `Описание проекта`    
Собрать данные о фестивалях с сайта (https://www.skiddle.com/)


### `Какой кейс решаем?:`    
1. Загружаем список фестивалей с динамически изменяемого сайта
2. Из полученых данных извлекаем ссылки на индивидуальные страницы
3. Загружаем с индивидуальных страниц
   1. Названия фестиваля
   2. Место проведения
   3. Цена, если указана

4. Сохранить данные в формате json

**Что практикуем**     
работу с библиотекой BeautifulSoup 

### `Результаты:`  
[Файл с кодом webscrapping](https://github.com/f999145/cases/blob/main/004_wscrap_festivals/webscrapping.py)

[Файл с итоговым результатом](https://github.com/f999145/cases/blob/main/004_wscrap_festivals/data/festivals.zip)