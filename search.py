import sys
from io import BytesIO
import requests
from PIL import Image



def param(response):
    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_latitude = toponym_coodrinates.split(" ")
    spn = ",".join(sys.argv[-2:])
    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_latitude]),
        "spn": spn,
        "l": "map",
        'pt': ",".join([toponym_longitude, toponym_latitude, "pm2dbm"])
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()
    # Создадим картинку
    # и тут же ее покажем встроенным просмотрщиком операционной системы

