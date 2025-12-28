import pandas as pd
import matplotlib.pyplot as plt

# Biểu đồ xu hướng doanh thu theo thời gian
def visualize_revenue_trend(monthly_revenue):
    fig, ax = plt.subplots()
    if monthly_revenue is None or len(monthly_revenue) == 0:
        ax.text(
            0.5, 0.5,
            "No data available",
            ha="center", va="center",
            transform=ax.transAxes
        )
        return fig

    ax.plot(monthly_revenue.index, monthly_revenue.values)
    ax.set_title("Xu huong doanh thu theo thoi gian")
    ax.set_xlabel("Thoi gian")
    ax.set_ylabel("Doanh thu")
    ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig
