# cleaner.py
import pandas as pd
import numpy as np
from pathlib import Path

# Logging setup
LOG_FILE = Path("clean_logging/clean.log")
CLEANING_LOGS = []

# Ghi vào file log
def log_issue(txn_id, issue, value=None):
    message = f"{txn_id} | {issue}"
    if value is not None:
        message += f" | {value}"

    CLEANING_LOGS.append(message)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")

# Đọc dataset
def load_data(filepath):
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None

def clean_categorical(series: pd.Series, invalid_values):
    """
    Chuẩn hoá các giá trị bị thiếu,
    không hợp lệ thành Unknown ở các cột categorical
    """
    return (
        series
        .replace(invalid_values, np.nan)
        .astype("string")          
        .str.strip()
        .str.title()
        .fillna("Unknown")
    )

# Làm sạch dữ liệu
def clean_data(df: pd.DataFrame):
    """
    1. Làm sạch các giá trị không hợp lệ ở các cột Categorical (Item, Payment Method, Location) chuẩn hoá thành Unknown
    2. Làm sạch các cột numeric:
        - Quantity, Price Per Unit: Giá trị không hợp lệ -> NaN
        - Total Spent: 
            + Nếu chứa giá trị không hợp lệ mà có đầy đủ Quantity, Price Per Unit -> Điền theo công thức Quantity * Price Per Unit
            + Nếu chứa giá trị không hợp lệ mà thiếu Quantity hoặc Price Per Unint -> NaN
    3. Làm sạch cột Transaction Date: Chứa giá trị không hợp lệ -> NaN
    4. Loại trùng lặp dựa vào cột Transaction ID
    """

    df = df.copy()

    # Reset logs
    CLEANING_LOGS.clear()
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Làm sạch file log
    with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("")  

    # Các giá trị không hợp lệ
    invalid_values = [
        "ERROR", "UNKNOWN", "NONE", "", "N/A",
        "null", "NULL", "nan", "NaN"
    ]

    # 1. Làm sạch các cột categorical
    if "Item" in df.columns:
        df["Item"] = clean_categorical(df["Item"], invalid_values)

    if "Payment Method" in df.columns:
        df["Payment Method"] = clean_categorical(df["Payment Method"], invalid_values)

    if "Location" in df.columns:
        df["Location"] = clean_categorical(df["Location"], invalid_values)
        df["Location"] = df["Location"].replace(
            {"In Store": "In-Store", "Take Away": "Takeaway"}
        )
    cat_logs = []

    if "Item" in df.columns:
        count_item_unknown = (df["Item"] == "Unknown").sum()
        cat_logs.append(
            f"Item: {count_item_unknown} values standardized to 'Unknown' ({(count_item_unknown/10000)*100:.2f}%)"
        )

    if "Payment Method" in df.columns:
        count_payment_unknown = (df["Payment Method"] == "Unknown").sum()
        cat_logs.append(
            f"Payment Method: {count_payment_unknown} values standardized to 'Unknown' ({(count_payment_unknown/10000)*100:2f}%)"
        )

    if "Location" in df.columns:
        count_location_unknown = (df["Location"] == "Unknown").sum()
        cat_logs.append(
            f"Location: {count_location_unknown} values standardized to 'Unknown' ({(count_location_unknown/10000)*100:.2f}%)"
        )

    if cat_logs:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("TÓM TẮT LOGS TRONG QUÁ TRÌNH DATA CLEANING\n")
            for line in cat_logs:
                f.write(line + "\n")

    # 2. Xử lý các cột numeric
    # Chuyển đổi các cột số    
    numeric_cols = ["Quantity", "Price Per Unit", "Total Spent"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Chuẩn hoá + Log
    for col in ["Quantity", "Price Per Unit", "Total Spent"]:
        if col in df.columns:
            bad = df[col].notna() & (df[col] <= 0)
            for idx in df[bad].index:
                log_issue(
                    df.at[idx, "Transaction ID"],
                    f"Invalid {col}",
                    df.at[idx, col]
                )
            df.loc[bad, col] = np.nan

    # Điền Total Spent (Nếu đầy đủ thông tin)
    if {"Quantity", "Price Per Unit", "Total Spent"}.issubset(df.columns):
        can_calc = (
            df["Total Spent"].isna() &
            df["Quantity"].notna() &
            df["Price Per Unit"].notna()
        )

        for idx in df[can_calc].index:
            log_issue(
                df.at[idx, "Transaction ID"],
                "Total Spent Recalculated",
                f"{df.at[idx, 'Quantity']} x {df.at[idx, 'Price Per Unit']}"
            )

        df.loc[can_calc, "Total Spent"] = (
            df.loc[can_calc, "Quantity"] *
            df.loc[can_calc, "Price Per Unit"]
        )  

    # 3. Xử lý cột Transaction Date
    date_logs = []
    if "Transaction Date" in df.columns:
        df["Transaction Date"] = pd.to_datetime(
            df["Transaction Date"], errors="coerce"
        )

        total_rows = len(df)
        count_bad = df["Transaction Date"].isna().sum()

        if count_bad > 0:
            date_logs.append(
                f"Transaction Date: {count_bad} missing or invalid values "
                f"({count_bad / total_rows * 100:.2f}%)"
            )

    if date_logs:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for line in date_logs:
                f.write(line + "\n")

    # 4. Loại bỏ các dòng có Transaction ID bị lặp
    if "Transaction ID" in df.columns:
        dup = df.duplicated(subset="Transaction ID", keep="first")
        for idx in df[dup].index:
            log_issue(
                df.at[idx, "Transaction ID"],
                "Duplicate Transaction ID Removed"
            )
        df = df[~dup]

    df = df.reset_index(drop=True)

    return df, CLEANING_LOGS

# Lưu vào file cleaned mới
def save_cleaned_data(df, output_path):
    df.to_csv(output_path, index=False, encoding="utf-8")
