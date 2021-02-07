import json
import unittest
from urllib import request
from urllib.error import HTTPError

from config import CONFIG

SERVER_URL = 'http://localhost:{}'.format(CONFIG['server_port'])


class TestUtils(unittest.TestCase):
    """Тестирование сервера main.py"""
    def test_server_ok(self):
        """Тестирование валидных запросов"""
        url = '{}?value=10'.format(SERVER_URL)
        r = request.urlopen(url)
        self.assertEqual(r.code, 200)
        json_data = json.loads(r.read().decode('UTF-8'))
        self.assertEqual(json_data['status'], 'ok')
        self.assertEqual(json_data['currency_in'], 'usd')
        self.assertEqual(json_data['currency_out'], 'rub')
        self.assertIsInstance(json_data['value_in'], float)
        self.assertIsInstance(json_data['value_out'], float)
        url = '{}?value=10.1'.format(SERVER_URL)
        r = request.urlopen(url)
        self.assertEqual(r.code, 200)
        json_data = json.loads(r.read().decode('UTF-8'))
        self.assertEqual(json_data['status'], 'ok')
        self.assertEqual(json_data['currency_in'], 'usd')
        self.assertEqual(json_data['currency_out'], 'rub')
        self.assertIsInstance(json_data['value_in'], float)
        self.assertIsInstance(json_data['value_out'], float)
        url = '{}?value=10,1'.format(SERVER_URL)
        r = request.urlopen(url)
        self.assertEqual(r.code, 200)
        json_data = json.loads(r.read().decode('UTF-8'))
        self.assertEqual(json_data['status'], 'ok')
        self.assertEqual(json_data['currency_in'], 'usd')
        self.assertEqual(json_data['currency_out'], 'rub')
        self.assertIsInstance(json_data['value_in'], float)
        self.assertIsInstance(json_data['value_out'], float)

    def test_server_errors(self):
        """Тестирование невалидных запросов"""
        # Отсутствие параметра value
        url = SERVER_URL
        with self.assertRaises(HTTPError):
            request.urlopen(url)

        url = '{}?value='.format(SERVER_URL)
        with self.assertRaises(HTTPError):
            request.urlopen(url)

        # Неверный формат параметра value
        url = '{}?value= '.format(SERVER_URL)
        with self.assertRaises(HTTPError):
            request.urlopen(url)

        url = '{}?value=test'.format(SERVER_URL)
        with self.assertRaises(HTTPError):
            request.urlopen(url)


if __name__ == '__main__':
    unittest.main()
