import pandas as pd

DATA_PATH = "data/cafe_sales_cleaned.csv"
df = pd.read_csv(
    DATA_PATH,
    parse_dates=["Transaction Date"]
)

# 1. Tổng hợp doanh thu theo tháng
monthly_revenue = (
    df.resample("ME", on="Transaction Date")["Total Spent"]
    .sum()
    .sort_index()
)

# 2. Thống kê mô tả xu hướng
total_revenue = monthly_revenue.sum()
avg_revenue = monthly_revenue.mean()
max_month = monthly_revenue.idxmax()
min_month = monthly_revenue.idxmin()

# 3. KQ
print("PHAN TICH XU HUONG DOANH THU THEO THOI GIAN")
print("-" * 50)
print(f"So thang: {monthly_revenue.shape[0]}")
print(f"Tong doanh thu: {total_revenue:.2f}")
print(f"Doanh thu trung binh/thang: {avg_revenue:.2f}")
print(f"Thang co doanh thu cao nhat: {max_month.strftime('%Y-%m')} "
      f"({monthly_revenue.loc[max_month]:.2f})")
print(f"Thang co doanh thu thap nhat: {min_month.strftime('%Y-%m')} "
      f"({monthly_revenue.loc[min_month]:.2f})")

# 4. Phân tích xu hướng bằng trung bình trượt
monthly_revenue_ma3 = monthly_revenue.rolling(3).mean()
print("\nNhan Xet:")
if monthly_revenue.iloc[-1] > monthly_revenue.iloc[0]:
    print("Doanh thu co xu huong tang nhe theo thoi gian.")
elif monthly_revenue.iloc[-1] < monthly_revenue.iloc[0]:
    print("Doanh thu co xu huong giam nhe theo thoi gian.")
else:
    print("Doanh thu duy tri tuong doi on dinh theo thoi gian.")
