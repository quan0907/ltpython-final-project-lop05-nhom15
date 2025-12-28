import pandas as pd
import numpy as np

def calculate_full_stats(df):
    """Tính toán tất cả các chỉ số thống kê mô tả chuyên sâu"""
    # Lọc các cột chứa số
    numeric_df = df.select_dtypes(include=[np.number])
    
    # Thống kê cơ bản (Mean, Std, Min, Max, Quartiles)
    desc_stats = numeric_df.describe().T
    
    # Bổ sung các chỉ số chuyên sâu
    desc_stats['median'] = numeric_df.median()      # Trung vị
    desc_stats['variance'] = numeric_df.var()        # Phương sai
    desc_stats['skewness'] = numeric_df.skew()      # Độ lệch (đánh giá phân phối)
    desc_stats['kurtosis'] = numeric_df.kurt()      # Độ nhọn
    
    return desc_stats

def find_outliers_iqr(df, column):
    """Tìm kiếm các đơn hàng có giá trị bất thường (quá cao hoặc quá thấp)"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

def get_correlation_matrix(df):
    """Tính toán mức độ liên quan giữa các yếu tố (vd: Số lượng và Doanh thu)"""
    return df.select_dtypes(include=[np.number]).corr()