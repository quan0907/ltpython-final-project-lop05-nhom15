import pandas as pd

def analyze_payment_method(df):
    """
    Phân tích phân bố % theo phương thức thanh toán
    """
    payment_stats = df[df['Payment Method'] != 'Unknown']['Payment Method'].value_counts(normalize=True) * 100
    return payment_stats.round(2)

def analyze_location(df):
    """
    Phân tích số lượng giao dịch theo địa điểm (In-store/Takeaway)
    """
    location_df = df[df['Location'] != 'Unknown']['Location'].value_counts().reset_index()
    location_df.columns = ['Location', 'Count']
    return location_df