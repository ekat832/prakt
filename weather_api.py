import logging
import requests

# Настройка логирования в файл и консоль
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

# Обработчик для записи в файл
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)

# Обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_weather(city: str, api_key: str) -> dict:
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
            "lang": "ru"
        }
        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 401:
            raise ValueError("Неверный API-ключ.")
        elif response.status_code == 404:
            raise ValueError("Город не найден.")
        elif response.status_code != 200:
            raise Exception(f"Ошибка при запросе: {data}")

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка сети: {str(e)}")  
        raise ConnectionError("Ошибка сети. Проверьте соединение с интернетом.")
