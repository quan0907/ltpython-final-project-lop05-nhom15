import matplotlib.pyplot as plt

def plot_stat_distribution(df, column):
    fig, (ax_hist, ax_box) = plt.subplots(2, 1, figsize=(10, 7), 
                                          gridspec_kw={"height_ratios": (.7, .3)})
    
    # Vẽ Histogram bằng Matplotlib thuần
    ax_hist.hist(df[column], bins=20, color='skyblue', edgecolor='black')
    ax_hist.set_title(f'Distribution Analysis: {column}')
    ax_hist.set_ylabel('Frequency')
    
    # Vẽ Boxplot bằng Matplotlib thuần
    ax_box.boxplot(df[column], vert=False, patch_artist=True, 
                   boxprops=dict(facecolor='lightcoral'))
    ax_box.set_xlabel(f'Value {column}')
    
    plt.tight_layout()
    return fig

def plot_heatmap(corr_matrix):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Sử dụng imshow của Matplotlib để thay thế Heatmap Seaborn
    im = ax.imshow(corr_matrix, cmap='coolwarm')
    
    # Hiển thị thanh giá trị bên cạnh
    plt.colorbar(im)
    
    # Thiết lập nhãn trục
    ax.set_xticks(range(len(corr_matrix.columns)))
    ax.set_yticks(range(len(corr_matrix.columns)))
    ax.set_xticklabels(corr_matrix.columns)
    ax.set_yticklabels(corr_matrix.columns)
    
    # Ghi giá trị tương quan vào từng ô bằng vòng lặp
    for i in range(len(corr_matrix.columns)):
        for j in range(len(corr_matrix.columns)):
            ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', 
                    ha="center", va="center", color="black")
    
    ax.set_title('Correlation Matrix')
    plt.tight_layout()
    return fig
