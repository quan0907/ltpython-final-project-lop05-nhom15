import pandas as pd

def product_performance(df):
    """
    Thống kê giá trị giao dịch và số lượng bán ra của tất cả các sản phẩm.

    Args:
        df (pd.DataFrame): DataFrame chứa dữ liệu bán hàng.

    Returns:
        pd.DataFrame: DataFrame chứa thông tin sản phẩm, số lượng bán và giá trị giao dịch.
    """

    # Gom nhóm theo sản phẩm và tính tổng
    product_stats = df[df['Item'] != 'Unknown'].groupby('Item').agg({
        'Quantity': 'sum',
        'Total Spent': 'sum'
    }).reset_index()

    # Đổi tên cột cho dễ hiểu hơn khi hiển thị
    product_stats.columns = ['Sản phẩm', 'Tổng số lượng bán', 'Tổng giá trị giao dịch']

    # Sắp xếp theo giá trị giao dịch giảm dần
    product_stats = product_stats.sort_values(by='Tổng giá trị giao dịch', ascending=False)


    return product_stats
