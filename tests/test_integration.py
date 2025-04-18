import logging
import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import RequestException
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import weather_api


logger = logging.getLogger()
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler('error.log', encoding='utf-8')
file_handler.setLevel(logging.ERROR)


console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

class TestWeatherIntegration(unittest.TestCase):

    @patch('weather_api.requests.get')
    def test_correct_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Москва",
            "main": {"temp": 10},
            "weather": [{"description": "ясно"}]
        }
        mock_get.return_value = mock_response

        result = weather_api.get_weather("Москва", "fake_api_key")
        self.assertEqual(result['city'], "Москва")
        self.assertEqual(result['temperature'], 10)
        self.assertEqual(result['description'], "ясно")

    @patch('weather_api.requests.get', side_effect=RequestException("Сетевая ошибка"))
    def test_logging_on_exception(self, mock_get):
        with self.assertRaises(ConnectionError):
            weather_api.get_weather("Москва", "fake_api_key")

        with open("error.log", "r", encoding="utf-8", errors="ignore") as f:
            logs = f.read()
            self.assertIn("Ошибка сети: Сетевая ошибка", logs)


if __name__ == '__main__':
    unittest.main()
