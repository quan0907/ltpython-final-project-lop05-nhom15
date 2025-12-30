import pandas as pd
# Tổng hợp gia tri giao dich theo tháng
def get_monthly_total_spent(df):
    monthly_total_spent = (
        df.resample("ME", on="Transaction Date") # nhom du lieu theo thang
        ["Total Spent"]
        .sum()
        .sort_index()
    )
    return monthly_total_spent
# Xu hướng gia tri giao dich
def get_total_spent_summary(monthly_total_spent):
    # Neu khong co du lieu -> dict rong
    if monthly_total_spent is None or len(monthly_total_spent) == 0:
        return {}

    # Tao dict chua chi so gia tri giao dich
    summary = {
        # Tong
        "total_total_spent": monthly_total_spent.sum(),

        # Trung binh
        "average_monthly_total_spent": monthly_total_spent.mean(),

        # Thang co gia tri giao dich cao & thap nhat
        "max_month": monthly_total_spent.idxmax(),
        "max_total_spent": monthly_total_spent.max(),
        "min_month": monthly_total_spent.idxmin(),
        "min_total_spent": monthly_total_spent.min(),

        # So thang phan tich
        "number_of_months": monthly_total_spent.shape[0],
    }
    return summary

