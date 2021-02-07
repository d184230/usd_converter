import re
from datetime import date, datetime
from urllib import parse, request

from config import CONFIG


class UtilsError(Exception):
    """ Ошибки в модуле utils.py """

    def __init__(self, text):
        self.txt = text


def get_html_from_url(url: str, params: dict = None) -> str:
    """
    Получение содержимого html c указанного url
    :param url: str адрес сайта
    :param params: dict параметры для запроса
    :return: str html c сайта
    """
    if params:
        url = '{}?{}'.format(url, parse.urlencode(params))
    r = request.urlopen(url)
    return r.read().decode('UTF-8')


def get_money_rate_from_cb(money_code: str, dt: date = date.today()) -> float:
    """
    Получение курса валюты по его коду c сайта ЦБ РФ, со страницы https://cbr.ru/currency_base/daily за указанную дату
    :param dt: datetime.date (optional) за какую дату получить курс, по умолчанию - сегодня
    :param money_code: 3 символьный код валюты с сайта ЦБ РФ (USD, CAD ...)
    :return: float курс валюты
    """
    params = {'UniDbQuery.Posted': True, 'UniDbQuery.To': dt.strftime('%d.%m.%Y')}
    html = get_html_from_url(CONFIG['cb_rates_url'], params)
    re_pattern = r'<td>{}</td>\s+<td>(\d+)</td>\s+<td>.+</td>\s+<td>(\d+,?\d+)</td>'.format(money_code.upper())
    find = re.search(re_pattern, html)
    if not find or len(find.groups()) != 2:
        raise UtilsError('Currency not found')
    usd_cnt = find.groups()[0]
    try:
        usd_rate = round(float(find.groups()[1].replace(',', '.')) / float(usd_cnt), 2)
    except ValueError:
        raise UtilsError('Rate value is error')
    return usd_rate


def log(text: str) -> None:
    """
    Логирование в stdout c указанием метки времени
    :param text: str Текст для логирования
    :return: None
    """
    print('{} - {}'.format(datetime.now(), text))
