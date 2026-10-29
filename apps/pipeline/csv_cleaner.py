import csv
import io
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

import pandas as pd

EXPECTED_HEADERS = ["date", "description", "category", "amount"]

def clean_amount(amount_str, raw_type=None):
    """
    Cleans strings like ' £2,500.00', 'USD 1587.39', '-$1,653.63', '(850)', 
    or '3,186.93 USD' into a Python Decimal 
    and determines whether it's Credit or Debit.
    """

    if not amount_str:
        return None, None

    cleaned = str(amount_str).strip()
    
    # Handle accounting format for negatives in parentheses, e.g. (850) -> -850
    is_negative = False
    if cleaned.startswith("(") and cleaned.endswith(")"):
        is_negative = True
        cleaned = cleaned[1:-1]

    if cleaned.startswith("-"):
        is_negative = True
        cleaned = cleaned[1:]

    # Remove currency symbols, text codes (USD, EUR), commas, and whitespace
    cleaned = re.sub(r"[£$€a-zA-Z,\s]", "", cleaned)

    if is_negative and not cleaned.startswith("-"):
        cleaned = "-" + cleaned

    try:
        val = Decimal(cleaned)

        # Respect explicit Tx_Type column if provided in the CSV
        if raw_type:
            norm_type = str(raw_type).strip().lower()
            if any(term in norm_type for term in ["expense", "debit"]):
                if val > 0:
                    val = -val
                return val, "Debit"
            elif any(term in norm_type for term in ["income", "credit"]):
                if val > 0:
                    val = -val
                return val, "Credit"

        # Fallback to sign inference if Tx_Type is blank or unrecognised
        txn_type = "Debit" if val < 0 else "Credit"
        return val, txn_type
    except (InvalidOperation, ValueError):
        return None, None

def parse_date(date_str):
    """
    Attempts to parse multiple common date formats found in messy CSVs.
    """
    if not date_str:
        return None
    
    date_str = str(date_str).strip()
    formats = [
        "%Y-%m-%d",          # 2024-01-15
        "%m/%d/%Y",          # 01/15/2024
        "%d/%m/%Y",          # 15/01/2024
        "%Y/%m/%d",          # 2024/01/15
        "%Y/%m/%d %H:%M",    # 2024/01/15 14:30
        "%d-%b-%Y",          # 15-Jan-2024
        "%b %d, %Y",         # Jan 15, 2024
        "%B %d, %Y"          # January 15, 2024
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt) #noqa
            return dt.date()
        except ValueError:
            continue
            
    # Fallback to pandas with specific exception catching
    try:
        parsed_dt = pd.to_datetime(date_str, errors="coerce")
        if not pd.isna(parsed_dt):
            return parsed_dt.date()
    except (ValueError, TypeError):
        pass

    return None

def find_column_index(headers, possible_names):
    """
    Helper function to locate column index dynamically based on header keywords.
    """
    for idx, header in enumerate(headers):
        clean_h = header.strip().lower()
        for name in possible_names:
            if name in clean_h:
                return idx
    return None

def clean_csv_content(file_bytes):
    """
    Cleans a raw CSV byte stream, filtering out comments, blank rows, 
    duplicate headers, and returning valid transaction dicts and skipped errors.
    """

    data_set = file_bytes.decode("UTF-8", errors="ignore")
    io_string = io.StringIO(data_set)
    
    # Filter out comment lines starting with #
    filtered_lines = [
        line for line in io_string 
        if not line.strip().startswith("#")
    ]
    
    reader = csv.reader(filtered_lines, delimiter=",")
    
    valid_rows = []
    skipped_rows = []

    headers = None
    date_idx, desc_idx, cat_idx, amt_idx, type_idx = None, None, None, None, None
    
    row_number = 0
    for row in reader:
        row_number += 1
        
        # Skip empty rows
        if not row or all(not field.strip() for field in row):
            continue

        # Check if this row is a header row
        joined_header_str = "".join(row).lower()
        if headers is None and (
            "date" in joined_header_str or 
            "amount" in joined_header_str or 
            "trans" in joined_header_str or 
            "category" in joined_header_str
        ):
            headers = [h.strip() for h in row]
            date_idx = find_column_index(headers, ["date", "trans_date", "transaction_date"])
            desc_idx = find_column_index(headers, ["desc", "notes", "memo", "details"])
            cat_idx = find_column_index(headers, ["cat", "category", "account"])
            amt_idx = find_column_index(headers, ["amount", "sum", "value", "raw"])
            type_idx = find_column_index(headers, ["type", "tx_type", "transaction_type"])
            continue

        # Fallback to standard default positions if header wasn't caught
        if date_idx is None: date_idx = 0
        if cat_idx is None: cat_idx = 1
        if amt_idx is None: amt_idx = 2
        if desc_idx is None: desc_idx = 4 if len(row) > 4 else 1

        max_idx = max(filter(None, [date_idx, desc_idx, cat_idx, amt_idx, type_idx]), default=3)
        if len(row) <= max_idx:
            skipped_rows.append(f"Row {row_number}: Insufficient columns")
            continue

        raw_date = row[date_idx]
        category = row[cat_idx] if cat_idx < len(row) else "Unassigned"
        raw_amount = row[amt_idx] if amt_idx < len(row) else "0"
        description = row[desc_idx] if desc_idx < len(row) else ""
        raw_type = row[type_idx] if type_idx is not None and type_idx < len(row) else None
        
        parsed_date = parse_date(raw_date)
        if not parsed_date:
            skipped_rows.append(f"Row {row_number}: Invalid date format '{raw_date}'")
            continue
            
        # Pass raw_type into clean_amount so expenses become 
        # negative and debits are tagged correctly
        amount_val, txn_type = clean_amount(raw_amount, raw_type=raw_type)
        if amount_val is None:
            skipped_rows.append(f"Row {row_number}: Invalid amount '{raw_amount}'")
            continue
            
        valid_rows.append({
            "date": parsed_date,
            "description": description.strip() if description else "",
            "category": category.strip().title() if category and category.strip() else "Unassigned",
            "amount": amount_val,
            "type": txn_type
        })
        
    return valid_rows, skipped_rows