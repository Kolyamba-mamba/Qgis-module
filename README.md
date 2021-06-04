# Qgis-module
Данная программа предназначена для объединения osm файла города и csv файла реестра домов города из источника https://www.reformagkh.ru/opendata, и последующего определения координат зданий по адресу.
## Формат входных данных
Входыми данными являются:
* `.osm` файл города с домами. Рекомендуется брать данные из ресурса https://overpass-turbo.eu/ используя запрос типа: 
```
area[name = "Белгород"];
(way
  ["building"~"house|terrace|detached|apartments"]
  ({{bbox}});
rel
  ["building"~"house|terrace|detached|apartments"]
  ({{bbox}}););
out;
```
* `.csv` файл реестра домов соответсвующего города из источника https://www.reformagkh.ru/opendata.
## Формат выходных данных
Выходными данными является файл building.csv, который содержит в себе: 
* id здания из osm;
* координаты (найдены геокодером);
* адрес (найден геокодером);
* рассчитанное кол-во жильцов в доме;
* поля из `.csv` файла с сайта  https://www.reformagkh.ru/opendata.
## Запуск
Для запуска программы введите в ее директории команду аналогичную следующей `python3 main.py -osmPath C:/Users/mrkol/Downloads/export.osm -jkhPath C:/Users/mrkol/Downloads/export-reestrmkd-31-20210601/export-reestrmkd-31-20210601.csv`, где параметры:
* `-osmPath` - абсолютный путь до `.osm` файла;
* `-jkhPath` - абсолютный путь до `.csv` файла Реформы ЖКХ.
## Используемые сторонние библиотеки
* pandas;
* geopy;
