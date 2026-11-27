# MI3031 – Chương 4: Hồi quy và Tương quan (Dự án Nhóm 2 Thành viên)

Kho lưu trữ mã nguồn Python, dữ liệu, biểu đồ và tài liệu báo cáo cho bài tập nhóm học phần **MI3031 – Suy luận thống kê** (Chương 4: Hồi quy và Tương quan).

- **Hạn nộp bài:** Thứ 4, ngày **02/12/2026**
- **Bài toán hồi quy đơn:** Dự đoán **Giá đóng cửa** ($Y$) dựa vào **Giá mở cửa cùng phiên** ($x$).
- **Bài toán hồi quy bội (ma trận):** Dự đoán **Giá đóng cửa** ($Y$) dựa vào 4 biến:
  - $x_1$: Giá mở cửa cùng phiên
  - $x_2$: Khối lượng phiên trước đó (`lag 1`)
  - $x_3$: Thay đổi so với phiên trước
  - $x_4$: Thời điểm tại phiên giao dịch (mã hóa từ ngày giao dịch)

---

## 1. Cấu trúc thư mục (Tách riêng theo từng thành viên)

```text
MI3031_Chuong4_HoiQuy_TuongQuan/
├── README.md
├── CONTRIBUTING.md
├── requirements.txt
├── .gitignore
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
│       ├── tv1_task.md
│       └── tv2_task.md
├── data/
│   ├── raw/                             # Dữ liệu gốc (chưa xử lý)
│   └── clean/                           # data_clean.csv dùng chung (TV1 tạo, TV2 đọc)
├── thanh_vien_1/                        # Không gian làm việc của Thành viên 1
│   ├── README.md
│   ├── 01_data_cleaning.py
│   ├── 02_simple_linear_regression.py
│   └── figures/
├── thanh_vien_2/                        # Không gian làm việc của Thành viên 2
│   ├── README.md
│   ├── 03_correlation_analysis.py
│   ├── 04_multiple_linear_regression.py
│   └── figures/
├── report/                              # Báo cáo cuối cùng (TV1 chủ trì tổng hợp)
└── slides/                              # Slide thuyết trình (TV2 chủ trì thiết kế)
```

---

## 2. Phân công công việc tổng quan (50 / 50)

| Hạng mục | Thành viên 1 (`thanh_vien_1/`) | Thành viên 2 (`thanh_vien_2/`) |
| :--- | :--- | :--- |
| **Chuyên môn** | Mục 1 (Giới thiệu dữ liệu), Mục 2 (Làm sạch dữ liệu), Mục 3 (Hồi quy tuyến tính đơn) | Mục 4 (Phân tích tương quan), Mục 5 (Hồi quy tuyến tính bội dạng ma trận) |
| **Code Python** | `01_data_cleaning.py`, `02_simple_linear_regression.py` | `03_correlation_analysis.py`, `04_multiple_linear_regression.py` |
| **Báo cáo** | Viết Mục 1–3 & **Chủ trì tổng hợp, định dạng Báo cáo** | Viết Mục 4–5, so sánh 2 mô hình & duyệt chéo Báo cáo |
| **Slide** | Soạn ý chính, bảng, hình Mục 1–3 & duyệt chéo Slide | Soạn Mục 4–5 & **Chủ trì thiết kế toàn bộ Slide** |

---

## 3. Lịch trình & Mốc bàn giao (27/11 – 02/12/2026)

| Ngày | Thành viên 1 | Thành viên 2 | Mốc bàn giao (Git Push / PR) |
| :--- | :--- | :--- | :--- |
| **Thứ 6 (27/11)** | Làm sạch dữ liệu, tạo biến trễ $x_2, x_3, x_4$ | Rà soát chéo dữ liệu sạch, chốt khung báo cáo & slide | `data/clean/data_clean.csv` trước 22:00 |
| **Thứ 7 (28/11)** | Code lõi Mục 3 (OLS, ANOVA, kiểm định $t/F$, KTC, dự đoán) | Code lõi Mục 4 ($r$, kiểm định $ho$, KTC) & Mục 5 (OLS ma trận) | PR code lõi chạy ra đủ số liệu trước 22:00 |
| **Chủ nhật (29/11)** | Vẽ biểu đồ Mục 3 (300 DPI), đối chiếu `scipy`/`statsmodels` | Code $F$-test, $R^2_{	ext{adj}}$, $t$-test Mục 5; vẽ heatmap & đồ thị $\hat{y}$ vs $y$ | Hoàn thiện 100% code & thư mục `figures/` trước 21:00 |
| **Thứ 2 (30/11)** | Viết Báo cáo Mục 1–3; gửi dàn ý slide Mục 1–3 | Viết Báo cáo Mục 4–5; bắt đầu dựng khung Slide | Gửi chéo bản nháp trước 22:00 |
| **Thứ 3 (01/12)** | **Tổng hợp & định dạng toàn bộ Báo cáo** | **Hoàn thiện thiết kế toàn bộ Slide** | Bản v1 hoàn chỉnh trước 22:00 |
| **Thứ 4 (02/12)** | Duyệt chéo Slide | Duyệt chéo Báo cáo & chạy lại toàn bộ code từ đầu | Chốt bản Final & nộp bài |

---

## 4. Hướng dẫn cài đặt & chạy nhanh

```bash
# 1. Cài đặt thư viện
pip install -r requirements.txt

# 2. Chạy tuần tự theo pipeline
python thanh_vien_1/01_data_cleaning.py
python thanh_vien_1/02_simple_linear_regression.py
python thanh_vien_2/03_correlation_analysis.py
python thanh_vien_2/04_multiple_linear_regression.py
```
