"""
TV1 - Mục 1 & 2: Làm sạch dữ liệu gốc và tạo tập biến dùng chung cho cả 2 mô hình.
Đầu vào : data/raw/raw_stock_data.csv (cập nhật đúng tên file dữ liệu gốc của nhóm)
Đầu ra  : data/clean/data_clean.csv
"""

from pathlib import Path
import pandas as pd

RAW_PATH = Path("data/raw/raw_stock_data.csv")
CLEAN_PATH = Path("data/clean/data_clean.csv")


def clean_and_prepare_data(raw_path: Path, clean_path: Path) -> pd.DataFrame:
    if not raw_path.exists():
        raise FileNotFoundError(
            f"Chưa tìm thấy file dữ liệu gốc tại: {raw_path}. "
            "Hãy đặt file CSV gốc vào thư mục data/raw/ và cập nhật tên cột tương ứng."
        )

    df = pd.read_csv(raw_path)

    # TODO: Cập nhật tên cột cho khớp với file dữ liệu gốc của nhóm
    # Giả định các cột gốc: ['Date', 'Open', 'Close', 'Volume']
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").drop_duplicates(subset=["Date"]).reset_index(drop=True)

    # Xử lý giá trị khuyết cơ bản
    df = df.dropna(subset=["Open", "Close", "Volume"]).copy()

    # Tạo biến cho mô hình hồi quy đơn & hồi quy bội:
    # Y  : Giá đóng cửa cùng phiên
    # x1 : Giá mở cửa cùng phiên (cũng là biến x của hồi quy đơn)
    # x2 : Khối lượng phiên trước đó (lag 1)
    # x3 : Thay đổi so với phiên trước (ví dụ: Open_t - Close_{t-1} hoặc Close_{t-1} - Close_{t-2} để tránh rò rỉ từ Y_t)
    # x4 : Thời điểm tại phiên giao dịch (chỉ số thứ tự phiên t = 1, 2, ..., n)
    df["Y_close"] = df["Close"].astype(float)
    df["x1_open"] = df["Open"].astype(float)
    df["x2_prev_volume"] = df["Volume"].shift(1).astype(float)
    df["x3_prev_change"] = (df["Close"].shift(1) - df["Close"].shift(2)).astype(float)

    # Loại bỏ các dòng đầu bị NaN do phép dịch trễ
    df_clean = df.dropna(subset=["x2_prev_volume", "x3_prev_change"]).reset_index(drop=True)
    df_clean["x4_time_index"] = range(1, len(df_clean) + 1)

    cols_out = ["Date", "Y_close", "x1_open", "x2_prev_volume", "x3_prev_change", "x4_time_index"]
    df_clean = df_clean[cols_out]

    clean_path.parent.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(clean_path, index=False)

    print(f"Đã xuất dữ liệu sạch: {clean_path} (n = {len(df_clean)} quan sát)")
    print(df_clean.describe().round(4))
    return df_clean


if __name__ == "__main__":
    clean_and_prepare_data(RAW_PATH, CLEAN_PATH)
