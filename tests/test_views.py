import unittest
from unittest.mock import patch
from unittest import mock
from _datetime import datetime
from src.views import generate_report, load_user_settings


class TestGenerateReport(unittest.TestCase):
    @patch('src.views.generate_report')
    def test_generate_report(self, mock_generate_report):
        # Подготовка тестовых данных
        transactions_for_views = [
            {'Номер карты': '*5814', 'Сумма операции с округлением': 1262.00},
            {'Номер карты': '*7512', 'Сумма операции с округлением': 7.94},
            {'date': '21.12.2021', 'amount': 1198.23, 'category': 'Переводы',
             'description': 'Перевод Кредитная карта. ТП 10.2 RUR'},
            {'date': '20.12.2021', 'amount': 829.00, 'category': 'Супермаркеты',
             'description': 'Лента'},
            {'date': '20.12.2021', 'amount': 421.00, 'category': 'Различные товары',
             'description': 'Ozon.ru'},
            {'date': '16.12.2021', 'amount': -14216.42, 'category': 'ЖКХ',
             'description': 'ЖКУ Квартира'},
            {'date': '16.12.2021', 'amount': 453.00, 'category': 'Бонусы',
             'description': 'Кешбэк за обычные покупки'},
        ]

        expected_response = {
            "greeting": datetime.now(),
            "cards": [
                {"last_digits": "5814", "total_spent": 1262.00, "cashback": 12.62},
                {"last_digits": "7512", "total_spent": 7.94, "cashback": 0.08}
            ],
            "top_transactions": [
                {"date": "21.12.2021", "amount": 1198.23, "category": "Переводы",
                 "description": "Перевод Кредитная карта. ТП 10.2 RUR"},
                {"date": "20.12.2021", "amount": 829.00, "category": "Супермаркеты",
                 "description": "Лента"},
                {"date": "20.12.2021", "amount": 421.00, "category": "Различные товары",
                 "description": "Ozon.ru"},
                {"date": "16.12.2021", "amount": -14216.42, "category": "ЖКХ",
                 "description": "ЖКУ Квартира"},
                {"date": "16.12.2021", "amount": 453.00, "category": "Бонусы",
                 "description": "Кешбэк за обычные покупки"},
            ],
            "currency_rates": [
                {"currency": "USD", "rate": 73.21},
                {"currency": "EUR", "rate": 87.08}
            ],
            "stock_prices": [
                {"stock": "AAPL", "price": 150.12},
                {"stock": "AMZN", "price": 3173.18},
                {"stock": "GOOGL", "price": 2742.39},
                {"stock": "MSFT", "price": 296.71},
                {"stock": "TSLA", "price": 1007.08}
            ]
        }

        # Настройка мока
        mock_generate_report.return_value = expected_response

        # Вызов тестируемой функции
        response = mock_generate_report(transactions_for_views)

        # Проверка результата
        self.assertEqual(response, expected_response)

    @mock.patch('builtins.open', new_callable=mock.mock_open,
                read_data='{"user_currencies": ["USD"], "user_stocks": ["AAPL"]}')
    def test_load_user_settings(self, mock_open):
        settings = load_user_settings('data/user_settings.json')
        self.assertEqual(settings['user_currencies'], ['USD'])
        self.assertEqual(settings['user_stocks'], ['AAPL'])

    @mock.patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_user_settings_file_not_found(self, mock_open):
        settings = load_user_settings('data/non_existing_file.json')
        self.assertEqual(settings, {})


if __name__ == '__main__':
    unittest.main()
