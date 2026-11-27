"""
TV1 - Mục 3: Mô hình hồi quy tuyến tính đơn (Y_close theo x1_open).
Cài đặt thủ công theo đúng công thức Slide 4.1 (MI3031) và đối chiếu bằng scipy.stats.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

CLEAN_PATH = Path("data/clean/data_clean.csv")
FIG_DIR = Path("thanh_vien_1/figures")


def simple_linear_regression_from_scratch(x: np.ndarray, y: np.ndarray, alpha: float = 0.05) -> dict:
    n = len(x)
    x_bar = np.mean(x)
    y_bar = np.mean(y)

    # Tổng bình phương & tích chéo
    S_xx = np.sum((x - x_bar) ** 2)
    S_xy = np.sum((x - x_bar) * (y - y_bar))
    SS_T = np.sum((y - y_bar) ** 2)

    # Ước lượng OLS
    beta1_hat = S_xy / S_xx
    beta0_hat = y_bar - beta1_hat * x_bar
    y_hat = beta0_hat + beta1_hat * x
    residuals = y - y_hat

    # Phân tích phương sai (ANOVA)
    SS_R = beta1_hat * S_xy
    SS_E = SS_T - SS_R
    MS_R = SS_R / 1.0
    MS_E = SS_E / (n - 2)
    s2 = MS_E
    s = np.sqrt(s2)

    # Sai số chuẩn của các hệ số
    se_beta1 = s / np.sqrt(S_xx)
    se_beta0 = s * np.sqrt(1.0 / n + (x_bar ** 2) / S_xx)

    # Kiểm định ý nghĩa hồi quy H0: beta1 = 0
    t0_beta1 = beta1_hat / se_beta1
    f0 = MS_R / MS_E
    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 2)
    f_crit = stats.f.ppf(1 - alpha, dfn=1, dfd=n - 2)

    # Khoảng tin cậy 100(1 - alpha)% cho beta0 và beta1
    ci_beta1 = (beta1_hat - t_crit * se_beta1, beta1_hat + t_crit * se_beta1)
    ci_beta0 = (beta0_hat - t_crit * se_beta0, beta0_hat + t_crit * se_beta0)

    # Hệ số xác định & phần dư chuẩn hóa
    R2 = SS_R / SS_T
    d_std = residuals / s

    return {
        "n": n, "x_bar": x_bar, "y_bar": y_bar,
        "S_xx": S_xx, "S_xy": S_xy, "SS_T": SS_T, "SS_R": SS_R, "SS_E": SS_E,
        "MS_R": MS_R, "MS_E": MS_E, "s2": s2, "s": s,
        "beta0_hat": beta0_hat, "beta1_hat": beta1_hat,
        "se_beta0": se_beta0, "se_beta1": se_beta1,
        "t0_beta1": t0_beta1, "t_crit": t_crit, "f0": f0, "f_crit": f_crit,
        "ci_beta0": ci_beta0, "ci_beta1": ci_beta1,
        "R2": R2, "y_hat": y_hat, "residuals": residuals, "d_std": d_std,
    }


def predict_intervals(res: dict, x0: float, alpha: float = 0.05) -> dict:
    y0_hat = res["beta0_hat"] + res["beta1_hat"] * x0
    t_crit = stats.t.ppf(1 - alpha / 2, df=res["n"] - 2)
    term = (x0 - res["x_bar"]) ** 2 / res["S_xx"]

    half_ci = t_crit * np.sqrt(res["s2"] * (1.0 / res["n"] + term))
    half_pi = t_crit * np.sqrt(res["s2"] * (1.0 + 1.0 / res["n"] + term))

    return {
        "x0": x0,
        "y0_hat": y0_hat,
        "ci_mean": (y0_hat - half_ci, y0_hat + half_ci),
        "pi_single": (y0_hat - half_pi, y0_hat + half_pi),
    }


def plot_slr_figures(x: np.ndarray, y: np.ndarray, res: dict, fig_dir: Path) -> None:
    fig_dir.mkdir(parents=True, exist_ok=True)

    # 1. Biểu đồ phân tán + đường hồi quy
    order = np.argsort(x)
    plt.figure(figsize=(7, 5))
    plt.scatter(x, y, alpha=0.65, label="Quan sát thực tế")
    plt.plot(x[order], res["y_hat"][order], color="red", linewidth=2,
             label=f"ŷ = {res['beta0_hat']:.4f} + {res['beta1_hat']:.4f}x")
    plt.xlabel("Giá mở cửa cùng phiên (x)")
    plt.ylabel("Giá đóng cửa cùng phiên (Y)")
    plt.title("Hồi quy tuyến tính đơn: Giá đóng cửa theo Giá mở cửa")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(fig_dir / "scatter_ols.png", dpi=300)
    plt.close()

    # 2. Bộ 4 biểu đồ chẩn đoán phần dư
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes[0, 0].scatter(res["y_hat"], res["residuals"], alpha=0.6)
    axes[0, 0].axhline(0, color="red", linestyle="--")
    axes[0, 0].set_title("Phần dư theo giá trị dự báo ŷ")

    axes[0, 1].scatter(x, res["residuals"], alpha=0.6)
    axes[0, 1].axhline(0, color="red", linestyle="--")
    axes[0, 1].set_title("Phần dư theo biến độc lập x")

    axes[1, 0].plot(res["residuals"], marker="o", markersize=3, linewidth=0.8)
    axes[1, 0].axhline(0, color="red", linestyle="--")
    axes[1, 0].set_title("Phần dư theo trình tự thời gian")

    stats.probplot(res["residuals"], dist="norm", plot=axes[1, 1])
    axes[1, 1].set_title("Biểu đồ xác suất chuẩn (Q-Q Plot)")

    plt.tight_layout()
    plt.savefig(fig_dir / "residuals_4plots.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv(CLEAN_PATH)
    x = df["x1_open"].to_numpy()
    y = df["Y_close"].to_numpy()

    res = simple_linear_regression_from_scratch(x, y, alpha=0.05)
    print(f"Phương trình hồi quy: y_hat = {res['beta0_hat']:.4f} + {res['beta1_hat']:.4f} * x")
    print(f"R^2 = {res['R2']:.4f} | s = {res['s']:.4f} | t0 = {res['t0_beta1']:.4f} | f0 = {res['f0']:.4f}")
    print(f"Kiểm chứng t0^2 == f0: {res['t0_beta1']**2:.4f} vs {res['f0']:.4f}")
    print(f"KTC 95% beta1: ({res['ci_beta1'][0]:.4f}, {res['ci_beta1'][1]:.4f})")

    pred = predict_intervals(res, x0=float(np.mean(x)))
    print(f"Tại x0 = {pred['x0']:.4f}: y0_hat = {pred['y0_hat']:.4f}")
    print(f"  KTC 95% trung bình : ({pred['ci_mean'][0]:.4f}, {pred['ci_mean'][1]:.4f})")
    print(f"  Khoảng dự đoán 95% : ({pred['pi_single'][0]:.4f}, {pred['pi_single'][1]:.4f})")

    # Đối chiếu nhanh với scipy.stats.linregress
    lr = stats.linregress(x, y)
    print(f"[Đối chiếu scipy] beta0 = {lr.intercept:.4f}, beta1 = {lr.slope:.4f}, R^2 = {lr.rvalue**2:.4f}")

    plot_slr_figures(x, y, res, FIG_DIR)
