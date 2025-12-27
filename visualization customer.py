import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data (from analysis.py)
df = pd.read_csv('cleaned_cafe_sales.csv')

# Ensure datetime
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])

# Set style for plots
sns.set(style="whitegrid")

# Visualization 1: Top 10 Items (Bar Chart)
item_counts = df['Item'].value_counts().head(10)
plt.figure(figsize=(10, 6))
item_counts.plot(kind='bar', color='skyblue')
plt.title('Top 10 Món Hàng Phổ Biến Nhất')
plt.xlabel('Món Hàng')
plt.ylabel('Số Lượng Bán')
plt.xticks(rotation=45)
plt.show()

# Visualization 2: Payment Methods Distribution (Pie Chart)
payment_counts = df['Payment Method'].value_counts()
plt.figure(figsize=(8, 8))
payment_counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen', 'lightblue', 'lightcoral'])
plt.title('Phân Bố Phương Thức Thanh Toán')
plt.ylabel('')
plt.show()

# Visualization 3: Total Spent by Location (Box Plot)
plt.figure(figsize=(10, 6))
sns.boxplot(x='Location', y='Total Spent', data=df, palette='Set3')
plt.title('Phân Bố Chi Tiêu Theo Địa Điểm')
plt.xlabel('Địa Điểm')
plt.ylabel('Total Spent')
plt.xticks(rotation=45)
plt.show()

# Visualization 4: Daily Sales Trend (Line Plot)
daily_sales = df.groupby(df['Transaction Date'].dt.date)['Total Spent'].sum()
plt.figure(figsize=(12, 6))
daily_sales.plot(kind='line', marker='o', color='purple')
plt.title('Xu Hướng Doanh Thu Hàng Ngày')
plt.xlabel('Ngày')
plt.ylabel('Tổng Doanh Thu')
plt.xticks(rotation=45)
plt.show()

# Visualization 5: Distribution of Total Spent (Histogram)
plt.figure(figsize=(10, 6))
df['Total Spent'].hist(bins=20, color='orange', edgecolor='black')
plt.title('Phân Bố Chi Tiêu Tổng (Histogram)')
plt.xlabel('Total Spent')
plt.ylabel('Tần Suất')
plt.show()

# Visualization 6: Average Spent by Hour (Bar Plot)
sales_by_hour = df.groupby('Hour')['Total Spent'].mean()
plt.figure(figsize=(10, 6))
sales_by_hour.plot(kind='bar', color='teal')
plt.title('Trung Bình Chi Tiêu Theo Giờ')
plt.xlabel('Giờ Trong Ngày')
plt.ylabel('Trung Bình Total Spent')
plt.show()

# Visualization 7: Heatmap of Correlations
corr_matrix = df[['Quantity', 'Price Per Unit', 'Total Spent']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Heatmap Tương Quan Giữa Các Biến Số')
plt.show()