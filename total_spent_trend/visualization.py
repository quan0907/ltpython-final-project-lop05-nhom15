import pandas as pd
import matplotlib.pyplot as plt

# Biểu đồ xu hướng gia tri giao dich theo thời gian
def visualize_total_spent_trend(monthly_total_spent):
    fig, ax = plt.subplots()
    if monthly_total_spent is None or len(monthly_total_spent) == 0:
        ax.text(
            0.5, 0.5,
            "No data available",
            ha="center", va="center",
            transform=ax.transAxes
        )
        return fig

    # Bieu do duong - Xu huong theo thoi gian
    ax.plot(monthly_total_spent.index, monthly_total_spent.values)
    ax.set_title("Xu huong gia tri giao dich theo thoi gian")
    ax.set_xlabel("Thoi gian")
    ax.set_ylabel("Gia tri giao dich")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig

