import requests
import json
from config import CURRENCY_CODES

class APIException(Exception):
    """Ошибка пользователя при взаимодействии с ботом."""
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        # Валюты должны быть разными
        if base == quote:
            raise APIException("Невозможно перевести одинаковые валюты.")
        # Проверяем наличие валюты в списке
        try:
            base_code = CURRENCY_CODES[base]
        except KeyError:
            raise APIException(f'Валюта "{base}" не поддерживается.')
        try:
            quote_code = CURRENCY_CODES[quote]
        except KeyError:
            raise APIException(f'Валюта "{quote}" не поддерживается.')

        # Проверяем число
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: "{amount}". Введите число.')

        # Запрос курса через API
        url = f'https://min-api.cryptocompare.com/data/price?fsym={base_code}&tsyms={quote_code}'
        resp = requests.get(url)
        if resp.status_code != 200:
            raise APIException("Сервис конвертации недоступен. Попробуйте позже.")
        try:
            result = json.loads(resp.content)[quote_code]
        except (KeyError, ValueError, json.JSONDecodeError):
            raise APIException("Сервис не вернул ожидаемый ответ.")

        return round(result * amount, 4)