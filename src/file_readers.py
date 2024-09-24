import logging

import pandas as pd

file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[file_handler])


def read_transactions_from_excel(file_path: str):
    """Читает данные из Excel и возвращает их в виде списка словарей."""
    try:
        logging.info(f"Попытка чтения файла: {file_path}")
        df = pd.read_excel(file_path, engine="openpyxl")
        transactions = df.to_dict(orient="records")  # Преобразуем в список словарей
        logging.info(f"Файл {file_path} успешно прочитан. Загружено {len(transactions)} транзакций.")
        return transactions
    except FileNotFoundError:
        logging.error(f"Файл {file_path} не найден.")
        return []
    except Exception as e:
        logging.error(f"Ошибка чтения Excel-файла: {e}")
        return []


if __name__ == "__main__":
    print(read_transactions_from_excel("data/operations.xlsx"))
