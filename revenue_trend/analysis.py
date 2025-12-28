import pandas as pd
# Tổng hợp doanh thu theo tháng
def get_monthly_revenue(df):
    monthly_revenue = (
        df.resample("ME", on="Transaction Date")["Total Spent"]
        .sum()
        .sort_index()
    )
    return monthly_revenue
# Xu hướng doanh thu
def get_revenue_summary(monthly_revenue):
    if monthly_revenue is None or len(monthly_revenue) == 0:
        return {}

    summary = {
        "total_revenue": monthly_revenue.sum(),
        "average_monthly_revenue": monthly_revenue.mean(),
        "max_month": monthly_revenue.idxmax(),
        "max_revenue": monthly_revenue.max(),
        "min_month": monthly_revenue.idxmin(),
        "min_revenue": monthly_revenue.min(),
        "number_of_months": monthly_revenue.shape[0],
    }
    return summary
