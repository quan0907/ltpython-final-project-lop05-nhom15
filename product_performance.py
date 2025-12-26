import pandas as pd

def product_performance(df):
    """
    Thống kê doanh thu và số lượng bán ra của tất cả các sản phẩm.

    Args:
        df (pd.DataFrame): DataFrame chứa dữ liệu bán hàng.

    Returns:
        pd.DataFrame: DataFrame chứa thông tin sản phẩm, số lượng bán và doanh thu.
    """

    # Gom nhóm theo sản phẩm và tính tổng
    product_stats = df.groupby('Item').agg({
        'Quantity': 'sum',
        'Total Spent': 'sum'
    }).reset_index()

    # Đổi tên cột cho dễ hiểu hơn khi hiển thị
    product_stats.columns = ['Sản phẩm', 'Tổng số lượng bán', 'Tổng doanh thu']

    # Sắp xếp theo doanh thu giảm dần
    product_stats = product_stats.sort_values(by='Tổng doanh thu', ascending=False)

    return product_stats