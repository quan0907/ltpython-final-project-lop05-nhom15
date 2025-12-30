# app.py
import streamlit as st

from data_cleaning import cleaner
from product_performance import product_performance as product_perf_analysis
from product_performance import visualization as product_perf_viz
from STATS_METRICS import analysis as stats_analysis
from STATS_METRICS import visualization as stats_viz
from total_spent_trend import analysis as total_spent_analysis
from total_spent_trend import visualization as total_spent_viz
from product_customer import analysis_customer as customer_analysis
from product_customer import visualization_customer as customer_viz


# Page config
st.set_page_config(
    page_title="Bài tập lớn Lập trình Python",
    layout="wide"
)

st.title("Phân tích sản phẩm và hành vi khách hàng")


# Load & clean data
DATA_FILE = "data/sales_data.csv"

raw_df = cleaner.load_data(DATA_FILE)
if raw_df is None:
    st.error("Không thể load dữ liệu gốc.")
    st.stop()

cleaned_df, cleaning_logs = cleaner.clean_data(raw_df)
cleaner.save_cleaned_data(cleaned_df, "data/sales_data_cleaned.csv")

# TAB RENDER 
def render_raw_data_tab(df):
    st.subheader("Dữ liệu gốc")
    st.dataframe(df, use_container_width=True)


def render_cleaned_data_tab(df, logs):
    st.subheader("Dữ liệu sau khi làm sạch")

    display_df = df.copy()
    if "Transaction Date" in display_df.columns:
        display_df["Transaction Date"] = (
            display_df["Transaction Date"]
            .dt.strftime("%Y-%m-%d")
        )

    st.dataframe(display_df, use_container_width=True)

    st.markdown("### Cleaning log (Preview)")
    if logs:
        logs_show = logs[:10] + logs[-1:]
        st.text_area(
            label="Cleaning Log",
            value="\n".join(logs_show),
            height=300
        )
    else:
        st.success("Không phát hiện lỗi dữ liệu 🎉")


def render_product_performance_tab(df):
    st.subheader("Hiệu suất sản phẩm")

    product_df = product_perf_analysis.product_performance(df)
    top_n = min(10, len(product_df))

    st.markdown(f"### Top {top_n} sản phẩm theo giá trị giao dịch")
    fig_rev = product_perf_viz.plot_product_performance(
        product_df,
        "Tổng giá trị giao dịch"
    )
    st.pyplot(fig_rev)

    st.divider()

    st.markdown(f"### Top {top_n} sản phẩm theo số lượng bán")
    fig_qty = product_perf_viz.plot_product_performance(
        product_df,
        metric="Tổng số lượng bán"
    )
    st.pyplot(fig_qty)


def render_stats_metrics_tab(df):
    st.subheader("Phân bố và thống kê giá trị đặc trưng")

    st.markdown("### Thống kê mô tả giá trị giao dịch")
    stats_df = stats_analysis.calculate_full_stats(df)
    st.dataframe(stats_df, use_container_width=True)

    st.divider()

    st.markdown("### Phân bố giá trị giao dịch")
    fig_dist = stats_viz.plot_stat_distribution(
        df,
        column="Total Spent"
    )
    st.pyplot(fig_dist)

    st.divider()

    st.markdown("### Tương quan giữa các biến số")
    corr_matrix = stats_analysis.get_correlation_matrix(df)
    fig_corr = stats_viz.plot_heatmap(corr_matrix)
    st.pyplot(fig_corr)


def render_total_spent_trend_tab(df):
    st.subheader("Xu hướng giá trị giao dịch theo thời gian")

    monthly_total_spent = total_spent_analysis.get_monthly_total_spent(df)
    summary = total_spent_analysis.get_total_spent_summary(monthly_total_spent)

    st.markdown("### Tóm tắt xu hướng")
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Tổng giá trị giao dịch", f"${summary['total_total_spent']:,.2f}")
        col2.metric("Trung bình / tháng", f"${summary['average_monthly_total_spent']:,.2f}")
        col3.metric("Tháng cao nhất", summary['max_month'].strftime("%Y-%m"))
        col4.metric("Tháng thấp nhất", summary['min_month'].strftime("%Y-%m"))
    else:
        st.warning("Không có đủ dữ liệu để phân tích xu hướng.")

    st.divider()

    st.markdown("### Biểu đồ xu hướng theo tháng")
    fig_trend = total_spent_viz.visualize_total_spent_trend(monthly_total_spent)
    st.pyplot(fig_trend)


def render_customer_behavior_tab(df):
    st.subheader("Hành vi khách hàng")

    payment_stats = customer_analysis.analyze_payment_method(df)
    location_stats = customer_analysis.analyze_location(df)

    fig = customer_viz.visualize_payment_and_location(
        payment_stats,
        location_stats
    )
    st.pyplot(fig)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Dữ liệu gốc",
    "Dữ liệu sau khi làm sạch",
    "Hiệu suất sản phẩm",
    "Phân bố & thống kê",
    "Xu hướng giá trị giao dịch",
    "Hành vi khách hàng"
])

with tab1:
    render_raw_data_tab(raw_df)

with tab2:
    render_cleaned_data_tab(cleaned_df, cleaning_logs)

with tab3:
    render_product_performance_tab(cleaned_df)

with tab4:
    render_stats_metrics_tab(cleaned_df)

with tab5:
    render_total_spent_trend_tab(cleaned_df)

with tab6:
    render_customer_behavior_tab(cleaned_df)
