import requests
import json
from Cb_token import keys
class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, ammount: str):
        #Формируем исключение - если валюты равны друг друг (доллар=доллару, биткоин=биткоину и т.д.):
        if quote == base:
            raise ConvertionException(f'Нельзя конвертировать одинаковые валюты {base}!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}!')

        try:
            ammount = float(ammount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {ammount}!')

        #Формируем парсерный, динамический(c помощью f) запрос:
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')  #Динамический запрос формируется с помощью f и подстановки в API-строку ключей: вместо ВТС {keys[quote]}, а вместо USD {keys[base]}
        total_base = json.loads(r.content)[keys[base]]

        return total_base

    #EUR&to=GBP