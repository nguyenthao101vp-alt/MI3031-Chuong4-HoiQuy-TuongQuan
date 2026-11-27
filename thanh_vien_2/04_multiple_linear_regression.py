"""
TV2 - Mục 5: Hồi quy tuyến tính bội theo phương pháp tiếp cận ma trận (Slide 4.3 - MI3031).
Cài đặt trực tiếp beta_hat = (X^T X)^(-1) X^T y bằng numpy và đối chiếu với statsmodels.OLS.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm

CLEAN_PATH = Path("data/clean/data_clean.csv")
FIG_DIR = Path("thanh_vien_2/figures")


def mlr_matrix_from_scratch(X_raw: np.ndarray, y: np.ndarray, alpha: float = 0.05) -> dict:
    n, k = X_raw.shape
    p = k + 1

    # Ma trận mô hình X kích thước n x p (cột đầu toàn số 1)
    X = np.column_stack([np.ones(n), X_raw])
    XtX = X.T @ X
    Xty = X.T @ y

    # Kiểm tra điều kiện khả nghịch (Giả thiết 2.4)
    det_XtX = np.linalg.det(XtX)
    cond_num = np.linalg.cond(XtX)
    if np.isclose(det_XtX, 0.0):
        raise np.linalg.LinAlgError("Ma trận X^T X suy biến (đa cộng tuyến hoàn hảo)!")

    C = np.linalg.inv(XtX)
    beta_hat = C @ Xty

    y_hat = X @ beta_hat
    residuals = y - y_hat

    # Phân tích phương sai (ANOVA) dạng ma trận
    y_sum_sq_over_n = (np.sum(y) ** 2) / n
    SS_T = float(y.T @ y - y_sum_sq_over_n)
    SS_R = float(beta_hat.T @ Xty - y_sum_sq_over_n)
    SS_E = float(y.T @ y - beta_hat.T @ Xty)

    MS_R = SS_R / k
    MS_E = SS_E / (n - p)
    s2 = MS_E
    s = np.sqrt(s2)

    # Kiểm định F toàn mô hình
    f0 = MS_R / MS_E
    f_crit = stats.f.ppf(1 - alpha, dfn=k, dfd=n - p)

    # R^2 và R^2 hiệu chỉnh
    R2 = SS_R / SS_T
    R2_adj = 1.0 - (SS_E / (n - p)) / (SS_T / (n - 1))

    # Sai số chuẩn & kiểm định t từng hệ số riêng
    se_beta = np.sqrt(s2 * np.diag(C))
    t0_beta = beta_hat / se_beta
    t_crit = stats.t.ppf(1 - alpha / 2, df=n - p)
    p_values = 2 * (1 - stats.t.cdf(np.abs(t0_beta), df=n - p))

    return {
        "n": n, "k": k, "p": p, "det_XtX": det_XtX, "cond_num": cond_num,
        "beta_hat": beta_hat, "se_beta": se_beta, "t0_beta": t0_beta,
        "t_crit": t_crit, "p_values": p_values,
        "SS_T": SS_T, "SS_R": SS_R, "SS_E": SS_E,
        "MS_R": MS_R, "MS_E": MS_E, "s2": s2, "s": s,
        "f0": f0, "f_crit": f_crit, "R2": R2, "R2_adj": R2_adj,
        "y_hat": y_hat, "residuals": residuals,
    }


def plot_mlr_figures(df: pd.DataFrame, res: dict, fig_dir: Path) -> None:
    fig_dir.mkdir(parents=True, exist_ok=True)
    y = df["Y_close"].to_numpy()

    plt.figure(figsize=(9, 4.8))
    plt.plot(df["x4_time_index"], y, label="Giá đóng cửa thực tế (y)", linewidth=1.6)
    plt.plot(df["x4_time_index"], res["y_hat"], label="Giá dự báo hồi quy bội (ŷ)", linestyle="--", linewidth=1.6)
    plt.xlabel("Chỉ số phiên giao dịch (x4)")
    plt.ylabel("Giá đóng cửa")
    plt.title("So sánh giá đóng cửa thực tế và dự báo (Mô hình hồi quy bội)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_dir / "actual_vs_pred_mlr.png", dpi=300)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.scatter(res["y_hat"], res["residuals"], alpha=0.65)
    plt.axhline(0, color="red", linestyle="--")
    plt.xlabel("Giá trị dự báo (ŷ)")
    plt.ylabel("Phần dư (e)")
    plt.title("Biểu đồ phần dư mô hình hồi quy tuyến tính bội")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_dir / "residuals_mlr.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv(CLEAN_PATH)
    feature_cols = ["x1_open", "x2_prev_volume", "x3_prev_change", "x4_time_index"]
    X_raw = df[feature_cols].to_numpy()
    y = df["Y_close"].to_numpy()

    res = mlr_matrix_from_scratch(X_raw, y, alpha=0.05)
    names = ["Intercept (beta0)"] + [f"{c} (beta{i+1})" for i, c in enumerate(feature_cols)]

    print("=== KẾT QUẢ HỒI QUY TUYẾN TÍNH BỘI (MA TRẬN) ===")
    print(f"R^2 = {res['R2']:.4f} | R^2_adj = {res['R2_adj']:.4f} | s = {res['s']:.4f}")
    print(f"Kiểm định F: f0 = {res['f0']:.4f} (f_crit = {res['f_crit']:.4f})")
    for name, b, se, t0, pv in zip(names, res["beta_hat"], res["se_beta"], res["t0_beta"], res["p_values"]):
        print(f"  {name:24s}: beta_hat = {b:10.4f} | se = {se:8.4f} | t0 = {t0:8.4f} | p = {pv:.4f}")

    # Đối chiếu với statsmodels.OLS
    ols_model = sm.OLS(y, sm.add_constant(X_raw)).fit()
    print(f"
[Đối chiếu statsmodels] R^2 = {ols_model.rsquared:.4f}, R^2_adj = {ols_model.rsquared_adj:.4f}")

    plot_mlr_figures(df, res, FIG_DIR)
