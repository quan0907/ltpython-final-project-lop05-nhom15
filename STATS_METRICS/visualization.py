import pandas as pd
import numpy as np

def calculate_full_stats(df):
    # Lấy dữ liệu cột Total Spent
    target_col = df['Total Spent']
    
    # Tính các chỉ số mô tả mặc định
    desc_stats = target_col.describe().to_frame().T
    
    # Tính thêm median và mode
    desc_stats['median'] = target_col.median()
    desc_stats['mode'] = target_col.mode()[0]
    
    # Sắp xếp và giữ lại đúng các cột bạn yêu cầu
    ordered_cols = ["count", "mean", "median", "mode", "min", "25%", "50%", "75%", "max"]
    return desc_stats[ordered_cols]

def find_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

def get_correlation_matrix(df):
    return df.select_dtypes(include=[np.number]).corr()
