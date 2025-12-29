import matplotlib.pyplot as plt
import pandas as pd

def plot_product_performance(df, metric='Tổng doanh thu'):
    """
    Vẽ biểu đồ top 10 + nhóm các sản phẩm khác .
    """
    # 1. Đảm bảo dữ liệu đã được sắp xếp giảm dần
    df_sorted = df.sort_values(by=metric, ascending=False).copy()

    # 2. Xử lý logic gộp nhóm "Khác"
    if len(df_sorted) > 10:
        # Lấy Top 10
        top_10 = df_sorted.head(10)

        # Tính tổng cho phần còn lại
        rest_value = df_sorted.iloc[10:][metric].sum()

        # Tạo dòng mới cho nhóm "Khác"
        others_row = pd.DataFrame({
            'Sản phẩm': ['Các sản phẩm khác'],
            metric: [rest_value]
        })

        # Gộp Top 10 và dòng Khác lại
        plot_data = pd.concat([top_10, others_row], ignore_index=True)
    else:
        plot_data = df_sorted

    # 3. Vẽ biểu đồ bằng Matplotlib 
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Chọn màu
    color = '#27AE60' if metric == 'Tổng doanh thu' else '#E67E22'

    # Vẽ biểu đồ ngang (barh)
    # Lưu ý: Matplotlib mặc định vẽ từ dưới lên, nên ta sẽ đảo trục sau
    bars = ax.barh(plot_data['Sản phẩm'], plot_data[metric], color=color)

    # Đảo ngược trục Y để sản phẩm Top 1 nằm trên cùng
    ax.invert_yaxis()

    # Trang trí biểu đồ (Mô phỏng style gọn gàng)
    ax.set_title(f'Top 10 sản phẩm theo {metric.lower()}', fontsize=14, fontweight='bold')
    ax.set_xlabel(metric, fontsize=11)
    
    # Ẩn các đường viền (spines) phía trên và bên phải cho thoáng mắt
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Thêm lưới dọc mờ
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    # Thêm nhãn giá trị lên biểu đồ
    for i, v in enumerate(plot_data[metric]):
        # Định dạng tiền tệ hoặc số lượng
        label = f"${v:,.0f}" if metric == 'Tổng doanh thu' else f"{v:,.0f}"
        
        # padding=3: khoảng cách giữa chữ và cột
        ax.text(v, i, f" {label}", va='center', fontsize=9, color='black')

    plt.tight_layout()
    return fig
