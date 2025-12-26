import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_product_performance(df, metric='Tổng doanh thu'):
    """
    Vẽ biểu đồ Top 10 + nhóm 'Các sản phẩm khác'.
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
        # Chỉ cần tạo dictionary với các cột cần thiết cho biểu đồ
        others_row = pd.DataFrame({
            'Sản phẩm': ['Các sản phẩm khác'],
            metric: [rest_value]
        })

        # Gộp Top 10 và dòng Khác lại
        plot_data = pd.concat([top_10, others_row], ignore_index=True)
    else:
        # Nếu tổng sản phẩm <= 10 thì vẽ hết, không cần gộp
        plot_data = df_sorted

    # 3. Vẽ biểu đồ
    fig, ax = plt.subplots(figsize=(10, 6))
    color = '#27AE60' if metric == 'Tổng doanh thu' else '#E67E22'

    # Vẽ biểu đồ với dữ liệu đã xử lý (plot_data)
    sns.barplot(data=plot_data, x=metric, y='Sản phẩm', ax=ax, color=color)

    # Format lại tiêu đề
    ax.set_title(f'Top 10 sản phẩm theo {metric.lower()}', fontsize=14)

    # Thêm nhãn giá trị lên biểu đồ cho dễ nhìn
    for i, v in enumerate(plot_data[metric]):
        # Định dạng tiền tệ hoặc số lượng tùy theo metric
        label = f"${v:,.0f}" if metric == 'Tổng doanh thu' else f"{v:,.0f}"
        ax.text(v, i, f" {label}", va='center', fontsize=9)

    plt.tight_layout()
    return fig
