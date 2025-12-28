import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_stat_distribution(df, column):
    """Vẽ biểu đồ phân bổ và biểu đồ hộp để soi lỗi dữ liệu (Outliers)"""
    fig, (ax_hist, ax_box) = plt.subplots(2, 1, figsize=(10, 7), 
                                          gridspec_kw={"height_ratios": (.7, .3)})
    
    # Biểu đồ cột tần suất
    sns.histplot(df[column], kde=True, ax=ax_hist, color='#3498db')
    ax_hist.set_title(f'Phân tích Phân phối & Outliers: {column}', fontsize=12)
    
    # Biểu đồ hộp (Boxplot) - Cái này giúp thấy các điểm dữ liệu "rác"
    sns.boxplot(x=df[column], ax=ax_box, color='#e74c3c')
    
    plt.tight_layout()
    st.pyplot(fig)

def plot_heatmap(corr_matrix):
    """Vẽ biểu đồ nhiệt thể hiện sự tương quan"""
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title('Ma trận tương quan giữa các biến số')
    st.pyplot(fig)s