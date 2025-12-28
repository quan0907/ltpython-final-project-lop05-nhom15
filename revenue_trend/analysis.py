import pandas as pd
# Tổng hợp doanh thu theo tháng
def get_monthly_revenue(df):
    monthly_revenue = (
        df.resample("ME", on="Transaction Date") # nhom du lieu theo thang
        ["Total Spent"]
        .sum()
        .sort_index()
    )
    return monthly_revenue
# Xu hướng doanh thu
def get_revenue_summary(monthly_revenue):
    # Neu khong co du lieu -> dict rong
    if monthly_revenue is None or len(monthly_revenue) == 0:
        return {}

    # Tao dict chua chi so doanh thu
    summary = {
        # Tong
        "total_revenue": monthly_revenue.sum(),

        # Trung binh
        "average_monthly_revenue": monthly_revenue.mean(),

        # Thang co doanh thu cao & thap nhat
        "max_month": monthly_revenue.idxmax(),
        "max_revenue": monthly_revenue.max(),
        "min_month": monthly_revenue.idxmin(),
        "min_revenue": monthly_revenue.min(),

        # So thang phan tich
        "number_of_months": monthly_revenue.shape[0],
    }
    return summary

