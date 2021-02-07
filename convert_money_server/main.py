import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse
from urllib.error import HTTPError

from config import CONFIG
from utils import get_money_rate_from_cb, UtilsError


class server_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """ Обработка get запросов """
        q = parse.parse_qs(parse.urlparse(self.path).query)
        value_usd_list = q.get('value')
        # Проверка на наличие параметра value
        if not value_usd_list:
            status_code = 400
            data_json = {'status': 'error', 'error': 'param value not found'}
            self.send_response_to_user(status_code, data_json)
            return

        # Проверка на тип параметра
        try:
            value_usd = float(value_usd_list[0].replace(',', '.'))
        except ValueError:
            status_code = 400
            data_json = {'status': 'error', 'error': 'param value is not float'}
            self.send_response_to_user(status_code, data_json)
            return

        # Получение текущего курса
        try:
            usd_rate = get_money_rate_from_cb('USD')
        except HTTPError:
            status_code = 400
            data_json = {'status': 'error', 'error': 'site https://cbr.ru is not avaliable'}
            self.send_response_to_user(status_code, data_json)
            return
        except UtilsError:
            status_code = 400
            data_json = {'status': 'error', 'error': 'error with get usd rate'}
            self.send_response_to_user(status_code, data_json)
            return

        value_rub = round(value_usd * usd_rate, 2)
        data_json = {'status': 'ok', 'currency_in': 'usd', 'value_in': value_usd,
                     'currency_out': 'rub', 'value_out': value_rub}
        status_code = 200
        self.send_response_to_user(status_code, data_json)

    def send_response_to_user(self, status_code: int, data_json: dict) -> None:
        """
        Отправка ответа на запрос
        :param status_code: int статус код ответа
        :param data_json: dist json данные ответа
        :return: None
        """
        self.send_response(status_code)
        self.send_header('content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data_json).encode())


def main():
    # Запуск сервера
    server = HTTPServer(('', CONFIG['server_port']), server_handler)
    server.serve_forever()


if __name__ == '__main__':
    main()
