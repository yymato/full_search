import sys
from io import BytesIO
from operator import length_hint

import requests
from PIL import Image

from modules.drawer import drawer
from modules.lonlat_dist import lonlat_dist
from modules.size_func import selection_size

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]

# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
self_point = f'{toponym_longitude},{toponym_lattitude}'


search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": self_point,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    #...
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
org_points = []
for organization in json_response["features"][:10]:
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    # Адрес организации.
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    try:
        org_hour = organization["properties"]["CompanyMetaData"]['Hours']['text']
    except Exception:
        org_hour = 'Нет данных'
    # Получаем координаты ответа.
    org_point = f"{organization["geometry"]["coordinates"][0]},{organization["geometry"]["coordinates"][1]}"
    if 'круглосуточно' in org_hour:
        org_points.append(org_point + ',pm2dgl')
    elif org_hour != 'Нет данных':
        org_points.append(org_point + ',pm2bll')
    else:
        org_points.append(org_point + ',pm2grl')
    print('\n'.join([f'адрес {org_address}', f'Название {org_name}', f'Время работы {org_hour}', f'Расстояние {lonlat_dist(self_point, org_point)}']))

map_apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "pt": '~'.join([*org_points, "{0},ya_ru".format(self_point)]),
    "apikey": map_apikey,
}

map_api_server = "https://static-maps.yandex.ru/v1"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
drawer(response.content)