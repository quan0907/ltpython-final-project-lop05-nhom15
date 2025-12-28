import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
import numpy as np


def visualize_payment_and_location(payment_stats: pd.DataFrame, location_df: pd.DataFrame) -> Figure:
    "
    # Tạo figure với 2 hàng và 2 cột
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('PHÂN TÍCH PHƯƠNG THỨC THANH TOÁN & ĐỊA ĐIỂM GIAO DỊCH',
                 fontsize=16, fontweight='bold', y=1.02)

    # Màu sắc cho biểu đồ
    payment_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    location_colors = ['#A8E6CF', '#DCEDC1', '#FFD3B6', '#FFAAA5', '#FF8B94']

    # ========== BIỂU ĐỒ 1: Phân bố phương thức thanh toán (Bar chart) ==========
    ax1 = axes[0, 0]
    bars1 = ax1.bar(payment_stats['Phương thức thanh toán'],
                    payment_stats['Số lượng giao dịch'],
                    color=payment_colors[:len(payment_stats)],
                    edgecolor='black',
                    linewidth=1.5)

    ax1.set_title('PHÂN BỐ PHƯƠNG THỨC THANH TOÁN', fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel('Phương thức thanh toán', fontsize=12)
    ax1.set_ylabel('Số lượng giao dịch', fontsize=12)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(axis='y', alpha=0.3)

    # Thêm giá trị lên trên mỗi cột
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2., height + 0.1,
                 f'{int(height):,}',
                 ha='center', va='bottom', fontweight='bold')

    # ========== BIỂU ĐỒ 2: Tỷ lệ phương thức thanh toán (Pie chart) ==========
    ax2 = axes[0, 1]
    wedges, texts, autotexts = ax2.pie(payment_stats['Tỷ lệ %'],
                                       labels=payment_stats['Phương thức thanh toán'],
                                       autopct='%1.1f%%',
                                       colors=payment_colors[:len(payment_stats)],
                                       startangle=90,
                                       textprops={'fontsize': 10})

    ax2.set_title('TỶ LỆ PHƯƠNG THỨC THANH TOÁN (%)', fontsize=14, fontweight='bold', pad=20)

    # Tạo legend
    legend_labels = [f'{label}: {percent:.1f}%'
                     for label, percent in zip(payment_stats['Phương thức thanh toán'],
                                               payment_stats['Tỷ lệ %'])]
    ax2.legend(wedges, legend_labels, title="Phương thức",
               loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)

    # ========== BIỂU ĐỒ 3: Top địa điểm giao dịch (Bar chart) ==========
    ax3 = axes[1, 0]

    # Lấy top 10 địa điểm nếu có nhiều
    top_locations = location_df.head(10)
    bars3 = ax3.barh(top_locations['Địa điểm'],
                     top_locations['Số lượng giao dịch'],
                     color=location_colors[:len(top_locations)],
                     edgecolor='black',
                     linewidth=1.5)

    ax3.set_title('TOP 10 ĐỊA ĐIỂM CÓ NHIỀU GIAO DỊCH NHẤT', fontsize=14, fontweight='bold', pad=20)
    ax3.set_xlabel('Số lượng giao dịch', fontsize=12)
    ax3.set_ylabel('Địa điểm', fontsize=12)
    ax3.invert_yaxis()  # Địa điểm có số lượng cao nhất ở trên cùng
    ax3.grid(axis='x', alpha=0.3)

    # Thêm giá trị ở cuối mỗi thanh
    for bar in bars3:
        width = bar.get_width()
        ax3.text(width + max(top_locations['Số lượng giao dịch']) * 0.01,
                 bar.get_y() + bar.get_height() / 2.,
                 f'{int(width):,}',
                 va='center', fontweight='bold')

    # ========== BIỂU ĐỒ 4: Phân bố tỷ lệ địa điểm (Donut chart) ==========
    ax4 = axes[1, 1]

    # Tạo donut chart
    wedges2, texts2, autotexts2 = ax4.pie(location_df.head(8)['Tỷ lệ %'],
                                          labels=location_df.head(8)['Địa điểm'],
                                          autopct='%1.1f%%',
                                          colors=location_colors[:8],
                                          startangle=90,
                                          pctdistance=0.85,
                                          textprops={'fontsize': 9})

    # Vẽ vòng tròn ở giữa để tạo donut chart
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    ax4.add_artist(centre_circle)

    ax4.set_title('PHÂN BỐ TỶ LỆ THEO ĐỊA ĐIỂM (%)', fontsize=14, fontweight='bold', pad=20)

    # Thêm tổng số giao dịch ở giữa donut chart
    total_transactions = location_df['Số lượng giao dịch'].sum()
    ax4.text(0, 0, f'Tổng:\n{total_transactions:,}\ngiao dịch',
             ha='center', va='center', fontsize=10, fontweight='bold')

    # ========== TỔNG QUAN THỐNG KÊ ==========
    # Tạo một text box tổng quan
    stats_text = f"""
    TỔNG QUAN PHÂN TÍCH
    --------------------
    Tổng số giao dịch: {total_transactions:,}

    Phương thức thanh toán phổ biến nhất:
    • {payment_stats.iloc[0]['Phương thức thanh toán']}: {payment_stats.iloc[0]['Tỷ lệ %']}%
    • Số lượng: {payment_stats.iloc[0]['Số lượng giao dịch']:,}

    Địa điểm giao dịch nhiều nhất:
    • {location_df.iloc[0]['Địa điểm']}: {location_df.iloc[0]['Tỷ lệ %']}%
    • Số lượng: {location_df.iloc[0]['Số lượng giao dịch']:,}

    Đa dạng phương thức: {len(payment_stats)} loại
    Đa dạng địa điểm: {len(location_df)} điểm
    """

    # Thêm text box tổng quan vào một vị trí phù hợp
    fig.text(0.02, 0.02, stats_text,
             fontsize=9,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.3),
             verticalalignment='bottom')

    # Điều chỉnh layout
    plt.tight_layout()

    return fig


# Hàm tiện ích để lưu và hiển thị figure
def save_and_show_figure(fig: Figure, filename: str = 'payment_location_analysis.png', dpi: int = 300):

    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    plt.show()


# Hàm ví dụ để demo cách sử dụng
def create_sample_data() -> Tuple[pd.DataFrame, pd.DataFrame]:

    # Tạo dữ liệu phương thức thanh toán
    payment_data = {
        'Phương thức thanh toán': ['Thẻ tín dụng', 'Tiền mặt', 'Ví điện tử', 'Chuyển khoản', 'Thẻ ghi nợ'],
        'Số lượng giao dịch': [1250, 980, 750, 420, 300],
        'Tỷ lệ %': [33.78, 26.49, 20.27, 11.35, 8.11]
    }
    payment_stats = pd.DataFrame(payment_data)

    # Tạo dữ liệu địa điểm
    location_data = {
        'Địa điểm': ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ', 'Nha Trang', 'Đà Lạt', 'Huế', 'Vũng Tàu',
                     'Quảng Ninh'],
        'Số lượng giao dịch': [850, 1200, 450, 320, 280, 210, 190, 170, 150, 130],
        'Tỷ lệ %': [22.97, 32.43, 12.16, 8.65, 7.57, 5.68, 5.14, 4.59, 4.05, 3.51]
    }
    location_df = pd.DataFrame(location_data)

    return payment_stats, location_df


# Hàm main để chạy demo
def main():

    # Tạo dữ liệu mẫu
    payment_stats, location_df = create_sample_data()

    # Tạo visualization
    fig = visualize_payment_and_location(payment_stats, location_df)

    # Lưu và hiển thị
    save_and_show_figure(fig, 'payment_location_analysis.png')


    return fig


if __name__ == "__main__":
    fig = main()