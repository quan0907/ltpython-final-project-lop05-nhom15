# app.py
import streamlit as st

from data_cleaning import cleaner
from product_performance.product_performance import product_performance
from product_performance.visualization import plot_product_performance
from STATS_METRICS import analysis as stats_analysis
from STATS_METRICS import visualization as stats_viz
from revenue_trend import analysis as revenue_analysis
from revenue_trend import visualization as revenue_viz
from product_customer import analysis as customer_analysis
from product_customer import visualization as customer_viz

# config trang
st.set_page_config(
    page_title="Bài tập lớn Lập trình Python",
    layout="wide"
)

st.title("Phân tích sản phẩm và hành vi khách hàng")

# Đọc và làm sạch data
DATA_FILE = "data/sales_data.csv"

raw_df = cleaner.load_data(DATA_FILE)

if raw_df is None:
    st.error("Không thể load dữ liệu gốc.")
    st.stop()

cleaned_df, cleaning_logs = cleaner.clean_data(raw_df)
cleaner.save_cleaned_data(cleaned_df, "data/sales_data_cleaned.csv")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Dữ liệu gốc",
    "Dữ liệu sau khi làm sạch",
    "Hiệu suất sản phẩm",
    "Phân bố & thống kê",
    "Xu hướng giá trị giao dịch",
    "Hành vi khách hàng"
])

# TAB 1: Dataset gốc
with tab1:
    st.subheader("Dữ liệu gốc")
    st.dataframe(raw_df, use_container_width=True)

# TAB 2: Dataset sau khi làm sạch
with tab2:
    st.subheader("Dữ liệu sau khi làm sạch")
    display_df = cleaned_df.copy()

    if "Transaction Date" in display_df.columns:
        display_df["Transaction Date"] = (
            display_df["Transaction Date"]
            .dt.strftime("%Y-%m-%d")
        )
    st.dataframe(display_df, use_container_width=True)

    st.markdown("### 🪵 Cleaning log (xem nhanh)")
    if cleaning_logs:
        st.text_area(
            label="Cleaning Log",
            value="\n".join(cleaning_logs[:200]),
            height=300
        )
    else:
        st.success("Không phát hiện lỗi dữ liệu 🎉")

# TAB 3: Hiệu suất sản phẩm theo giá trị giao dịch và số lượng
with tab3:
    product_df = product_performance(cleaned_df)

    top_n = min(10, len(product_df))

    st.markdown(f"### Top {top_n} sản phẩm theo giá trị giao dịch")

    fig_rev = plot_product_performance(
        product_df,
        metric="Tổng doanh thu"
    )
    st.pyplot(fig_rev)

    st.divider()

    st.markdown(f"### Top {top_n} sản phẩm theo số lượng bán")
    fig_qty = plot_product_performance(
        product_df,
        metric="Tổng số lượng bán"
    )
    st.pyplot(fig_qty)

# TAB 4: Phân bố và thống kê
with tab4:
    st.subheader("Phân tích phân bố và thống kê giá trị đặc trưng")

    # Thống kê mô tả
    st.markdown("### Thống kê mô tả giá trị giao dịch")

    stats_df = stats_analysis.calculate_full_stats(cleaned_df)
    st.dataframe(stats_df, use_container_width=True)

    st.divider()

    # Phân bố
    st.markdown("### Phân bố giá trị giao dịch")

    fig_dist = stats_viz.plot_stat_distribution(
        cleaned_df,
        column="Total Spent"
    )
    st.pyplot(fig_dist)

    st.divider()

    # Biểu đồ nhiệt tương quan
    st.markdown("### Tương quan giữa các biến số")

    corr_matrix = stats_analysis.get_correlation_matrix(cleaned_df)
    fig_corr = stats_viz.plot_heatmap(corr_matrix)
    st.pyplot(fig_corr)

# TAB 5: Revenue Trend
with tab5:
    st.subheader("Xu hướng giá trị giao dịch theo thời gian")

    monthly_revenue = revenue_analysis.get_monthly_revenue(cleaned_df)

    # Tóm tắt xu hướng
    summary = revenue_analysis.get_revenue_summary(monthly_revenue)

    st.markdown("### Tóm tắt xu hướng")

    if summary:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Tổng giá trị giao dịch",
            f"${summary['total_revenue']:,.2f}"
        )
        col2.metric(
            "Trung bình / tháng",
            f"${summary['average_monthly_revenue']:,.2f}"
        )
        col3.metric(
            "Tháng cao nhất",
            summary['max_month'].strftime("%Y-%m")
        )
        col4.metric(
            "Tháng thấp nhất",
            summary['min_month'].strftime("%Y-%m")
        )
    else:
        st.warning("Không có đủ dữ liệu để phân tích xu hướng.")

    st.divider()

    # Biểu đồ xu hướng
    st.markdown("### Biểu đồ xu hướng theo tháng")

    fig_trend = revenue_viz.visualize_revenue_trend(monthly_revenue)
    st.pyplot(fig_trend)

with tab6:
    st.subheader("Hành vi khách hàng")

    payment_method = customer_analysis.analyze_payment_method(cleaned_df)
    location = customer_analysis.analyze_location(cleaned_df)
    
    fig_payment_method_and_location = customer_viz.visualize_payment_and_location(payment_method, location)
    st.pyplot(fig_payment_method_and_location)

