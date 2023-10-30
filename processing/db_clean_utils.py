import re
import pandas as pd
from datetime import datetime, timedelta

# Function to clean and split date string
def clean_date(date_str):
    # Check if date_str contains any number
    if not re.search(r'\d', date_str):
        return None, None

    today = datetime.today().date()
    date_start, date_end = None, None

    # For format like "1 Dec 2023 – 14 Apr 2024"
    if "–" in date_str:
        dates = date_str.split("–")
        date_start = pd.to_datetime(dates[0].strip(), errors='coerce', dayfirst=True).date()
        date_end = pd.to_datetime(dates[1].strip(), errors='coerce', dayfirst=True).date()

    # For format like "2022-01-01to2025-12-31"
    elif "to" in date_str:
        dates = date_str.split("to")
        date_start = pd.to_datetime(dates[0], errors='coerce').date()
        date_end = pd.to_datetime(dates[1], errors='coerce').date()

    # Handle single date
    elif re.search(r'\d', date_str):
        date_start = pd.to_datetime(date_str, errors='coerce', dayfirst=True).date()
        date_end = date_start + timedelta(days=365)  # Add 365 days

    # Check if either date is NaT and return None in that case
    if pd.isna(date_start) or pd.isna(date_end):
        return None, None

    return date_start, date_end