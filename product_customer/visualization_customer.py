import matplotlib.pyplot as plt
import pandas as pd


def visualize_payment_and_location(payment_stats, location_df):
    """
    Visualize payment method và location
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Biểu đồ Pie cho Payment Method
    ax1.pie(payment_stats.values, labels=payment_stats.index, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Payment Method Distribution')
    ax1.axis('equal')

    # Biểu đồ Bar cho Location
    ax2.bar(location_df['Location'], location_df['Count'])
    ax2.set_title('Transaction Count by Location')
    ax2.set_xlabel('Location')
    ax2.set_ylabel('Count')
    ax2.tick_params(axis='x', rotation=45)

    for i, v in enumerate(location_df['Count']):
        ax2.text(i, v, f"{v}", ha='center', va='bottom')

    plt.tight_layout()
    return fig