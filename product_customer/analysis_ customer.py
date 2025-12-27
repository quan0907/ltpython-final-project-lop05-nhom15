import pandas as pd
import numpy as np
from scipy import stats  # For additional statistical methods if needed

def process_cafe_sales(input_file='dirty_cafe_sales.csv', output_file='cleaned_cafe_sales.csv'):
    # Load the dataset
    df = pd.read_csv(input_file)

    # Data Cleaning
    # Convert 'Transaction Date' to datetime, coercing errors
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')

    # Drop rows with invalid dates
    df = df.dropna(subset=['Transaction Date'])

    # Handle missing 'Item' using 'Price Per Unit' mapping
    price_to_item = df.groupby('Price Per Unit')['Item'].first().to_dict()
    df['Item'] = df['Item'].fillna(df['Price Per Unit'].map(price_to_item))

    # Handle missing 'Price Per Unit' using 'Item' mean price mapping
    item_to_price = df.groupby('Item')['Price Per Unit'].mean().to_dict()
    df['Price Per Unit'] = df['Price Per Unit'].fillna(df['Item'].map(item_to_price))

    # Handle missing 'Quantity' with median (or 1 as default)
    df['Quantity'] = df['Quantity'].fillna(df['Quantity'].median() if not df['Quantity'].isnull().all() else 1)

    # Calculate or correct 'Total Spent'
    df['Calculated Total'] = df['Quantity'] * df['Price Per Unit']
    df['Total Spent'] = df['Total Spent'].fillna(df['Calculated Total'])
    # Correct inconsistencies
    mask = abs(df['Total Spent'] - df['Calculated Total']) > 0.01  # Allow small floating-point differences
    df.loc[mask, 'Total Spent'] = df['Calculated Total']
    df.drop('Calculated Total', axis=1, inplace=True)

    # Handle missing 'Payment Method' with mode
    mode_payment = df['Payment Method'].mode()[0] if not df['Payment Method'].mode().empty else 'Unknown'
    df['Payment Method'] = df['Payment Method'].fillna(mode_payment)

    # Handle missing 'Location' with mode
    mode_location = df['Location'].mode()[0] if not df['Location'].mode().empty else 'Unknown'
    df['Location'] = df['Location'].fillna(mode_location)

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove invalid values (e.g., negative quantities or prices)
    df = df[(df['Quantity'] > 0) & (df['Price Per Unit'] > 0) & (df['Total Spent'] > 0)]

    # Extract additional features for analysis
    df['Day of Week'] = df['Transaction Date'].dt.day_name()
    df['Hour'] = df['Transaction Date'].dt.hour
    df['Month'] = df['Transaction Date'].dt.month

    # Statistical Analysis (Phương thức thống kê, toán)
    print("Thống kê tổng quát về Total Spent:")
    print(f"Trung bình (Mean): {df['Total Spent'].mean():.2f}")
    print(f"Trung vị (Median): {df['Total Spent'].median():.2f}")
    print(f"Độ lệch chuẩn (Std Dev): {df['Total Spent'].std():.2f}")
    print(f"Mode của Quantity: {stats.mode(df['Quantity'])[0]}")

    # Analysis by Location (Địa điểm)
    grouped_location = df.groupby('Location')
    for location, group in grouped_location:
        print(f"\nPhân tích tại địa điểm: {location}")
        print(f"Trung bình Total Spent: {group['Total Spent'].mean():.2f}")
        print(f"Tổng doanh thu: {group['Total Spent'].sum():.2f}")
        print(f"Số lượng giao dịch: {len(group)}")

    # Popular Items and Purchase Frequency
    item_counts = df['Item'].value_counts()
    print("\nTop 10 món hàng phổ biến nhất:")
    print(item_counts.head(10))

    # Payment Method Distribution
    payment_dist = df['Payment Method'].value_counts(normalize=True) * 100
    print("\nPhân bố phương thức thanh toán (%):")
    print(payment_dist)

    # Time-based Analysis (Math: Aggregation and Trends)
    sales_by_day = df.groupby('Day of Week')['Total Spent'].sum().sort_values(ascending=False)
    print("\nDoanh thu theo ngày trong tuần:")
    print(sales_by_day)

    sales_by_hour = df.groupby('Hour')['Total Spent'].mean()
    print("\nTrung bình chi tiêu theo giờ:")
    print(sales_by_hour)

    # Correlation (Toán học: Tương quan)
    corr_matrix = df[['Quantity', 'Price Per Unit', 'Total Spent']].corr()
    print("\nMa trận tương quan:")
    print(corr_matrix)

    # Save cleaned data for visualization
    df.to_csv(output_file, index=False)
    print(f"\nDữ liệu đã sạch được lưu vào '{output_file}' cho trực quan hóa.")

    return df  # Return the cleaned DataFrame if needed for further use