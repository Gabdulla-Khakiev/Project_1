import pandas as pd

from src.views import generate_report, get_date_range, load_user_settings
from src.reports import save_report_to_file, spending_by_category
from src.services import find_phone_numbers
from src.file_readers import read_transactions_from_excel

if __name__ == "__main__":
    transactions = read_transactions_from_excel("data/operations.xlsx")
    df = pd.DataFrame(transactions)
    date_str = "2020-05-20 14:30:00"
    result = generate_report(date_str, transactions)
    services_result = find_phone_numbers(transactions)
    reports_result = spending_by_category(df)
    print(result)
