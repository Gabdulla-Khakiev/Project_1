import os
import unittest
from unittest import mock
from unittest.mock import patch

import requests

from src.external_api import get_exchange_rate, get_sp500_stock_price


# Тест для успешного получения курса валюты
@patch("src.external_api.requests.get")
def test_get_exchange_rate_success(mock_get):
    # Определяем, что должен вернуть mock-запрос
    mock_response = {
        "base": "USD",
        "date": "2021-03-17",
        "rates": {"RUB": 75.0, "EUR": 0.813399, "GBP": 0.72007, "JPY": 107.346001},
        "success": True,
        "timestamp": 1519296206,
    }

    # Настройка mock-ответа для requests.get
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    # Тестируем функцию
    result = get_exchange_rate("USD", "RUB")

    assert result == {"base": "USD", "rates": 75.0}
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD",
        headers={"apikey": os.getenv("EXCHANGES_API")},
    )


# Тест для обработки ошибки RequestException
@patch("src.external_api.requests.get")
def test_get_exchange_rate_failure(mock_get):
    # Настройка mock-ответа для requests.get
    mock_get.side_effect = requests.RequestException("Ошибка сети")

    # Тестируем функцию
    result = get_exchange_rate("USD", "RUB")

    assert result is None
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base=USD",
        headers={"apikey": os.getenv("EXCHANGES_API")},
    )


class TestGetSP500StockPrice(unittest.TestCase):

    @mock.patch("requests.get")
    def test_get_sp500_stock_price_success(self, mock_get):
        # Имитация ответа API
        mock_response = {
            "Global Quote": {
                "01. symbol": "IBM",
                "02. open": "217.9300",
                "03. high": "220.6200",
                "04. low": "217.2700",
                "05. price": "220.4400",
                "06. volume": "4072958",
                "07. latest trading day": "2024-09-23",
                "08. previous close": "217.7000",
                "09. change": "2.7400",
                "10. change percent": "1.2586%",
            }
        }

        # Настройка mock-объекта
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Вызов функции
        price = get_sp500_stock_price("IBM")

        # Проверка
        self.assertEqual(price, 220.44)
        mock_get.assert_called_once()  # Проверка, что запрос был выполнен один раз

    @mock.patch("requests.get")
    def test_get_sp500_stock_price_error(self, mock_get):
        # Имитация ошибки при запросе
        mock_get.side_effect = requests.exceptions.RequestException("Ошибка сети")

        # Вызов функции
        price = get_sp500_stock_price("IBM")

        # Проверка
        self.assertEqual(price, 0.0)
        mock_get.assert_called_once()  # Проверка, что запрос был выполнен один раз

    @mock.patch("requests.get")
    def test_get_sp500_stock_price_no_price(self, mock_get):
        # Имитация ответа API без цены
        mock_response = {
            "Global Quote": {
                "01. symbol": "IBM",
                "02. open": "217.9300",
                "03. high": "220.6200",
                "04. low": "217.2700",
                # "05. price": "220.4400",  # Нет цены
                "06. volume": "4072958",
                "07. latest trading day": "2024-09-23",
                "08. previous close": "217.7000",
                "09. change": "2.7400",
                "10. change percent": "1.2586%",
            }
        }

        # Настройка mock-объекта
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        # Вызов функции
        price = get_sp500_stock_price("IBM")

        # Проверка
        self.assertEqual(price, 0.0)  # Ожидаем, что вернется 0.0
        mock_get.assert_called_once()  # Проверка, что запрос был выполнен один раз


if __name__ == "__main__":
    unittest.main()
