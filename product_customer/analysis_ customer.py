import pandas as pd


def analyze_payment_method(df):


    payment_col = 'payment_method'

    # Kiểm tra xem cột có tồn tại không
    if payment_col not in df.columns:
        # Tìm cột có tên tương tự
        possible_cols = [col for col in df.columns if 'payment' in col.lower() or 'thanh_toan' in col.lower()]
        if possible_cols:
            payment_col = possible_cols[0]
        else:
            raise ValueError("Không tìm thấy cột phương thức thanh toán trong DataFrame")

    # Tính toán phân bố
    payment_distribution = df[payment_col].value_counts(normalize=True) * 100
    payment_distribution = payment_distribution.round(2)

    # Tạo DataFrame kết quả
    result_df = pd.DataFrame({
        'Phương thức thanh toán': payment_distribution.index,
        'Tỷ lệ %': payment_distribution.values
    })

    # Sắp xếp theo tỷ lệ giảm dần
    result_df = result_df.sort_values('Tỷ lệ %', ascending=False).reset_index(drop=True)

    return result_df


def analyze_location(df):


    location_col = 'location'

    # Kiểm tra xem cột có tồn tại không
    if location_col not in df.columns:
        # Tìm cột có tên tương tự
        possible_cols = [col for col in df.columns if 'location' in col.lower() or
                         'dia_diem' in col.lower() or 'address' in col.lower() or
                         'city' in col.lower() or 'thanh_pho' in col.lower()]
        if possible_cols:
            location_col = possible_cols[0]
        else:
            raise ValueError("Không tìm thấy cột địa điểm trong DataFrame")

    # Thống kê số lượng giao dịch theo địa điểm
    location_stats = df[location_col].value_counts()

    # Tạo DataFrame kết quả
    result_df = pd.DataFrame({
        'Địa điểm': location_stats.index,
        'Số lượng giao dịch': location_stats.values
    })

    # Sắp xếp theo số lượng giảm dần
    result_df = result_df.sort_values('Số lượng giao dịch', ascending=False).reset_index(drop=True)

    return result_df


# Hàm bổ trợ để tìm cột phù hợp
def find_column(df, keywords):

    for col in df.columns:
        col_lower = col.lower()
        for keyword in keywords:
            if keyword in col_lower:
                return col
    return None