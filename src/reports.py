import json
from functools import wraps
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional

# Настройка логирования
logging.basicConfig(filename="reports.log", level=logging.INFO)


def save_report_to_file(filename: str = None):
    """Декоратор для записи результата отчета в файл."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Выполняем функцию
            result = func(*args, **kwargs)

            # Определяем имя файла по умолчанию
            if filename is None:
                file_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            else:
                file_name = filename

            # Записываем результат в файл
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(result, file, ensure_ascii=False, indent=4)

            # Логируем успешную запись
            logging.info(f"Отчет сохранен в файл: {file_name}")
            return result

        return wrapper

    return decorator


@save_report_to_file()  # Декоратор по умолчанию сохраняет результат в файл
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> dict:
    """Возвращает траты по заданной категории за последние три месяца от переданной даты."""

    # Если дата не указана, используем текущую дату
    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")

    # Рассчитываем начало периода - три месяца назад
    start_date = end_date - timedelta(days=90)

    # Фильтрация транзакций по категории и диапазону дат
    filtered_transactions = transactions[
        (transactions['Категория'] == category) &
        (pd.to_datetime(transactions['Дата операции']) >= start_date) &
        (pd.to_datetime(transactions['Дата операции']) <= end_date)
        ]

    # Вычисляем общую сумму трат по категории
    total_expenses = filtered_transactions['Сумма операции'].sum()

    # Возвращаем результат в виде словаря
    report = {
        "category": category,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "total_expenses": total_expenses
    }

    return report
