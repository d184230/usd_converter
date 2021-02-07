import unittest
from datetime import date
from http.client import RemoteDisconnected
from urllib.error import URLError, HTTPError
import utils


class TestUtils(unittest.TestCase):
    """ Тестирование модуля utils.py """
    def test_utils_get_html_from_url(self):
        """ Тестирование функции utils.get_html_from_url """
        html = utils.get_html_from_url('https://ya.ru')
        self.assertGreater(len(html), 0)
        with self.assertRaises(URLError):
            utils.get_html_from_url('https://ya5.ru')
        with self.assertRaises(HTTPError):
            utils.get_html_from_url('https://httpbin.org/status/code')
        html = utils.get_html_from_url('https://httpbin.org/status/200')
        self.assertEqual(html, '')
        with self.assertRaises(RemoteDisconnected):
            utils.get_html_from_url('https://httpbin.org/status/100')
        with self.assertRaises(HTTPError):
            utils.get_html_from_url('https://httpbin.org/status/400')
        with self.assertRaises(HTTPError):
            utils.get_html_from_url('https://httpbin.org/status/500')
        html_url = utils.get_html_from_url('https://cbr.ru/search?text=usd')
        html_params = utils.get_html_from_url('https://cbr.ru/search', {'text': 'usd'})
        self.assertEqual(html_url, html_params)

    def test_utils_get_money_rate_from_html_cb(self):
        """ Тестирование функции utils.get_money_rate_from_html_cb """
        usd_rate = utils.get_money_rate_from_cb('USD')
        self.assertIsInstance(usd_rate, float)
        usd_rate = utils.get_money_rate_from_cb('USD', date.fromisoformat('2021-01-01'))
        self.assertEqual(usd_rate, 73.88)
        cad_rate = utils.get_money_rate_from_cb('CAD', date.fromisoformat('2021-01-01'))
        self.assertEqual(cad_rate, 57.96)
        with self.assertRaises(utils.UtilsError):
            utils.get_money_rate_from_cb('SSD')


if __name__ == '__main__':
    unittest.main()
