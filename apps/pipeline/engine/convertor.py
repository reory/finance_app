import csv
from io import TextIOWrapper


def extract_csv_rows(uploaded_file):
    """
    Convert an uploaded CSV file into a list of row dictionaries.
    Returns (rows, error_message)
    """

    if not uploaded_file:
        return None, "No file uploaded."

    if not uploaded_file.name.endswith(".csv"):
        return None, "Only CSV files are supported."

    try:
        wrapper = TextIOWrapper(uploaded_file.file, encoding="utf-8")
        reader = csv.DictReader(wrapper)
        rows = list(reader)
        return rows, None
    except Exception as e:
        return None, f"Failed to read CSV: {e}"
