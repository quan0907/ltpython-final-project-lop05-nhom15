import pandas as pd
import matplotlib.pyplot as plt

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

# 2. Xu hướng doanh thu
plt.figure()
plt.plot(monthly_revenue.index, monthly_revenue.values)
plt.xlabel("Thoi gian")
plt.ylabel("Doanh thu")
plt.title("Xu huong doanh thu theo thoi gian")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. So sánh doanh thu giữa các tháng
plt.figure()
plt.bar(monthly_revenue.index, monthly_revenue.values)
plt.xlabel("Thoi gian")
plt.ylabel("Doanh thu")
plt.title("So sanh doanh thu theo thang")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Trung bình trượt
ma3 = monthly_revenue.rolling(3).mean()
plt.figure()
plt.plot(monthly_revenue.index, monthly_revenue.values, label="Doanh thu thang")
plt.plot(ma3.index, ma3.values, label="Trung binh truot 3 thang")
plt.xlabel("Thoi gian")
plt.ylabel("Doanh thu")
plt.title("Xu huong doanh thu")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()