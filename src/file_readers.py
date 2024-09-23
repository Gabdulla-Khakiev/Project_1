import pandas as pd
import logging


logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат вывода
    filename='app.log',  # Логи будут сохраняться в файл 'app.log'
    filemode='a'  # Режим записи (a - добавление к файлу)
)


def read_transactions_from_excel(file_path: str):
    """Читает данные из Excel и возвращает их в виде списка словарей."""
    try:
        logging.info(f"Попытка чтения файла: {file_path}")
        df = pd.read_excel(file_path, engine='openpyxl')
        transactions = df.to_dict(orient='records')  # Преобразуем в список словарей
        logging.info(f"Файл {file_path} успешно прочитан. Загружено {len(transactions)} транзакций.")
        return transactions
    except FileNotFoundError:
        logging.error(f"Файл {file_path} не найден.")
        return []
    except Exception as e:
        logging.error(f"Ошибка чтения Excel-файла: {e}")
        return []


if __name__ == "__main__":
    transactions = read_transactions_from_excel("data/operations.xlsx")
    if transactions:
        logging.info("Транзакции успешно загружены и готовы к обработке.")
    else:
        logging.warning("Не удалось загрузить транзакции.")
