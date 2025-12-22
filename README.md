# BÀI TẬP LỚN LẬP TRÌNH PYTHON LỚP 05 NHÓM 15

## 1. Giới thiệu đề tài
Trong bài tập lớn môn "Lập trình Python", nhóm 15 chúng em lựa chọn một tập dữ liệu thực tế từ Kaggle để thực hiện việc phân tích, làm sạch, chuẩn hóa dữ liệu, trực quan hóa và xây dựng giao diện chương trình.

## 2. Thành viên nhóm
- Trần Phúc Bảo - 24133005 - Trực quan hoá dữ liệu
- Phạm Quốc Duy - 24133008 - Phân tích dữ liệu
- Võ Lê Hoàng Đức - 24133013 - Phân tích dữ liệu
- Trần Anh Khoa - 24133031 - Phân tích dữ liệu
- Phạm Thế Quân - 24134057 - Làm sạch dữ liệu

## 3. Thông tin về dataset
- **Tên dataset**: cafe_sales.csv
- **Nguồn**: Kaggle
- **Link**: [Cafe Sales – Dirty Data for Cleaning Training](https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training)
- **Lĩnh vực**: Kinh doanh
- **Mục đích của dataset**: Mô phỏng các giao dịch bán hàng tại một quán cà phê

### Mô tả dữ liệu
- Dataset bao gồm các cột chính:
  - Transaction ID (string): Mã giao dịch, là mã định danh duy nhất cho mỗi giao dịch, ví dụ: "TXN_8989148"
  - Item (string): Tên của mặt hàng, ví dụ: "Coffee" , "Sandwich"
  - Quantity (int): Số lượng mặt hàng đã mua, ví dụ: 1, 3
  - Price Per Unit (float): Giá của một đơn vị sản phẩm, ví dụ: 2.00, 4.00
  - Total Spent (float): Tổng số tiền chi tiêu cho giao dịch. Được tính bằng công thức: Số lượng * Giá mỗi đơn vị, ví dụ 8.00
  - Payment Method (string): Phương thức thanh toán đã sử dụng, ví dụ "Cash", "Credit Card"
  - Location (string): Địa điểm diễn ra giao dịch (Tại cửa hàng hoặc mang đi), ví dụ "In-store", "Takeaway"
  - Transaction Date (datetime): Ngày giao dịch, ví dụ "2023-01-01"

### Hạn chế & khiếm khuyết
- Có dữ liệu bị thiếu
- Có giá trị không hợp lệ, ví dụ như: "ERROR", "UNKNOWN"
- Có dữ liệu trùng lặp
- Một số cột cần chuẩn hóa

## 4. Nhiệm vụ và mục tiêu của bài tập lớn
### Nhiệm vụ
- Đọc và phân tích tập dữ liệu
- Làm sạch và chuẩn hóa dữ liệu
- Trực quan hóa dữ liệu bằng biểu đồ
- Áp dụng Numpy, Pandas trong xử lý dữ liệu
- Xây dựng giao diện chương trình bằng Streamlit
### Mục tiêu
- Biến đổi dữ liệu thô có nhiều lỗi, giá trị không hợp lệ,... thành bộ dữ liệu sạch, đồng nhất.
- Phát hiện kịp thời bộ dữ liệu có đáng tin cho việc đưa ra quyết định kinh doanh không.
## 5. Công nghệ sử dụng
- Python
- Pandas
- Numpy
- Matplotlib
- Streamlit
## 6. Cấu trúc thư mục và chương trình
```text
.
├── data/
│   ├── cafe_sales.csv # Dataset gốc
│   ├── cafe_sales_cleaned.csv # Dataset sau khi làm sạch
├── analysis/
│   ├── customer_behavior.py # Phân tích hành vi khách hàng trong việc lựa chọn phương thức thanh toán và địa điểm giao dịch
│   ├── product_performance.py # Phân tích sản phẩm bán chạy, ế theo 2 loại là số lượng và doanh thu
│   ├── revenue_trend.py # Phân tích doanh thu hàng tháng
│   └── stats_metrics.py # Phân tích phân bố và giá trị tổng chi đặc trưng
├── data_processing/
│   └── cleaner.py # Làm sạch và chuẩn hoá dữ liệu
├── clean_logging/
│   └── clean.log
├── visualization/
│   └── visualizer.py # Trực quan hoá dữ liệu
├── app.py # Giao diện Streamlit
├── requirements.txt # Các thư viện cần thiết để chạy chương trình
└── README.md
```
## 7. Hướng dẫn chạy chương trình

### Bước 1: Clone repository
```bash
git clone https://github.com/quan0907/ltpython-final-project-lop05-nhom15
cd ltpython-final-project-lop05-nhom15
```
### Bước 2: Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```
### Bước 3: Chạy file app.py
```bash
streamlit run app.py
```
