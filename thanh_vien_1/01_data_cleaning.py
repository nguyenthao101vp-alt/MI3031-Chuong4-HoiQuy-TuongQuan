# -*- coding: utf-8 -*-
"""01_data_cleaning.py - Làm sạch dữ liệu CTG (CafeF) và xuất data/data_clean.csv dùng chung.
Chạy từ thư mục gốc của dự án:  python code/01_data_cleaning.py
"""
import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import glob
files = glob.glob(os.path.join(BASE, "data", "*.xlsx"))
print("File Excel tìm thấy:", files)
RAW = files[0]
OUT = os.path.join(BASE, "data", "data_clean.csv")

# ---- 1. Đọc dữ liệu gốc -------------------------------------------------
raw = pd.read_excel(RAW)
print("Kích thước dữ liệu gốc:", raw.shape)
print(raw.dtypes, "\n")

# ---- 2. Kiểm tra khuyết / trùng ----------------------------------------
print("Số giá trị khuyết theo cột:\n", raw.isna().sum(), "\n")
print("Số dòng trùng lặp hoàn toàn:", raw.duplicated().sum())
print("Số ngày giao dịch trùng:", raw["Ngày"].duplicated().sum())
df = raw.drop_duplicates().dropna().copy()

# ---- 3. Chuẩn hóa kiểu dữ liệu & sắp xếp tăng dần theo thời gian ------
df["Ngay"] = pd.to_datetime(df["Ngày"], format="%d/%m/%Y")
df = df.sort_values("Ngay").reset_index(drop=True)

# Tách cột "Thay đổi" dạng "+0,80 (+2,68%)" thành số tuyệt đối & phần trăm
pat = r"^\s*([+-]?[\d,\.]+)\s*\(\s*([+-]?[\d,\.]+)\s*%\s*\)\s*$"
ext = df["Thay đổi"].astype(str).str.extract(pat)
df["Thay_doi"] = ext[0].str.replace(",", ".", regex=False).astype(float)      # nghìn đồng
df["Thay_doi_pct"] = ext[1].str.replace(",", ".", regex=False).astype(float)  # %
assert df["Thay_doi"].notna().all(), "Có dòng 'Thay đổi' không tách được"

df = df.rename(columns={"Giá đóng cửa": "Gia_dong_cua", "Giá mở cửa": "Gia_mo_cua",
                        "Khối lượng khớp lệnh": "Khoi_luong",
                        "Giá cao nhất": "Gia_cao_nhat", "Giá thấp nhất": "Gia_thap_nhat"})

# Kiểm tra nhất quán: Thay đổi = Giá đóng cửa(t) - Giá đóng cửa(t-1)
chk = (df["Thay_doi"] - df["Gia_dong_cua"].diff()).abs()
print("Sai lệch lớn nhất giữa 'Thay đổi' và chênh lệch giá đóng cửa (từ dòng 2):", chk.iloc[1:].max())
print("Thay đổi ở phiên đầu tiên (mép dữ liệu, không có phiên trước):", df.loc[0, "Thay_doi"])

# Kiểm tra logic giá (Low <= Open, Close <= High)
bad = df[(df.Gia_thap_nhat > df[["Gia_mo_cua", "Gia_dong_cua"]].min(axis=1)) |
         (df.Gia_cao_nhat < df[["Gia_mo_cua", "Gia_dong_cua"]].max(axis=1))]
print("Số dòng vi phạm quan hệ Low <= Open,Close <= High:", len(bad))

# Kiểm tra ngoại lai sơ bộ bằng quy tắc 1,5*IQR
for c in ["Gia_dong_cua", "Gia_mo_cua", "Khoi_luong"]:
    q1, q3 = df[c].quantile([.25, .75]); iqr = q3 - q1
    n_out = ((df[c] < q1 - 1.5 * iqr) | (df[c] > q3 + 1.5 * iqr)).sum()
    print(f"Ngoại lai (1,5*IQR) của {c}: {n_out}")

# ---- 4. Tạo bộ biến cho hai mô hình ------------------------------------
df["Y"] = df["Gia_dong_cua"]                            # Y: giá đóng cửa cùng phiên
df["x"] = df["Gia_mo_cua"]                              # x = x1: giá mở cửa cùng phiên
df["x2"] = df["Khoi_luong"].shift(1)                    # x2: khối lượng phiên trước (lag 1)
# x3: thay đổi giá của phiên liền trước (lag 1) -> không chứa Y_t, tránh rò rỉ dữ liệu.
df["x3"] = df["Thay_doi"].shift(1)
df["x3_pct"] = df["Thay_doi_pct"].shift(1)

# ---- 5. Chốt tập dữ liệu sạch ------------------------------------------
# Loại: (i) dòng đầu do lag x2 bị NaN;
#       (ii) dòng thứ hai vì x3 lấy từ 'Thay đổi' của phiên đầu = 0,00 (giá trị mép dữ liệu,
#            không phản ánh biến động thật vì không có phiên trước đó).
clean = df.iloc[2:].copy().reset_index(drop=True)
clean["x4"] = np.arange(1, len(clean) + 1)              # x4: thứ tự phiên 1..n trong mẫu sạch
clean["x1"] = clean["x"]
cols = ["Ngay", "x4", "Y", "x", "x1", "x2", "x3", "x3_pct",
        "Gia_cao_nhat", "Gia_thap_nhat", "Khoi_luong", "Thay_doi", "Thay_doi_pct"]
clean = clean[cols]
assert clean[["Y", "x", "x1", "x2", "x3", "x4"]].isna().sum().sum() == 0

clean.to_csv(OUT, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")
print(f"\nĐã xuất {OUT}: n = {len(clean)} quan sát, từ {clean.Ngay.min().date()} đến {clean.Ngay.max().date()}")
print(clean.describe().T[["mean", "std", "min", "max"]].round(4))
