import re
import pandas as pd
from datetime import datetime, timedelta

# Updated combined function to clean and split date string with all cases

def clean_date(date_str):
    # Normalize the string to remove non-breaking spaces and other unicode characters
    date_str = re.sub(r'\s+', ' ', date_str).strip()
    
    # Check if date_str contains any number
    if not re.search(r'\d', date_str):
        return None, None

    date_start, date_end = None, None

    # For format like "2022-01-01to2025-12-31"
    if "to" in date_str:
        dates = date_str.split("to")
        date_start = pd.to_datetime(dates[0].strip(), format='%Y-%m-%d', errors='coerce').date()
        date_end = pd.to_datetime(dates[1].strip(), format='%Y-%m-%d', errors='coerce').date()

    # For format like "1 Dec 2023 – 14 Apr 2024" or "03/10/2024 — 26/01/2025"
    elif any(delimiter in date_str for delimiter in ["–", "—", "-"]):
        delimiter = next((d for d in ["–", "—", "-"] if d in date_str), None)
        dates = date_str.split(delimiter)
        # Check for different date formats separately
        # For "1 Dec 2023 – 14 Apr 2024"
        if all(re.search(r'\b\d{1,2}\s+[a-zA-Z]{3}\s+\d{4}\b', date) for date in dates):
            date_start = pd.to_datetime(dates[0].strip(), format='%d %b %Y', errors='coerce').date()
            date_end = pd.to_datetime(dates[1].strip(), format='%d %b %Y', errors='coerce').date()
        # For "03/10/2024 — 26/01/2025"
        elif all(re.search(r'\b\d{1,2}/\d{1,2}/\d{4}\b', date) for date in dates):
            date_start = pd.to_datetime(dates[0].strip(), format='%d/%m/%Y', errors='coerce').date()
            date_end = pd.to_datetime(dates[1].strip(), format='%d/%m/%Y', errors='coerce').date()
        # For "06/03 — 16/06/2024", where one date might not have a year
        elif delimiter and re.search(r'\d', dates[1]):
            date_end = pd.to_datetime(dates[1].strip(), format='%d/%m/%Y', errors='coerce').date()
            if date_end and dates[0].count('/') == 1:
                date_start = pd.to_datetime(dates[0].strip() + f'/{date_end.year}', format='%d/%m/%Y', errors='coerce').date()

    # Handle single date
    elif re.search(r'\d', date_str):
        date_start = pd.to_datetime(date_str, format='%d/%m/%Y', errors='coerce', dayfirst=True).date()
        date_end = date_start + timedelta(days=365) if date_start else None  # Add 365 days

    # Check if either date is NaT and return None in that case
    if pd.isna(date_start) or pd.isna(date_end):
        return None, None

    return date_start, date_end

# Test the function with different date formats
# date_str1 = "1 Dec 2023 – 14 Apr 2024"
# date_str2 = "03/10/2024 — 26/01/2025"
# date_str3 = "06/03 — 16/06/2024"
# date_str4 = "2022-01-01to2025-12-31"
# date_str5 = "15/07/2025"

# print(clean_date(date_str1))
# print(clean_date(date_str2))
# print(clean_date(date_str3))
# print(clean_date(date_str4))
# print(clean_date(date_str5))