"""
TV2 - Mục 4: Phân tích tương quan (bám sát Slide 4.2 - MI3031).
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

CLEAN_PATH = Path("data/clean/data_clean.csv")
FIG_DIR = Path("thanh_vien_2/figures")


def correlation_analysis_from_scratch(x: np.ndarray, y: np.ndarray, rho0: float = 0.95, alpha: float = 0.05) -> dict:
    n = len(x)
    S_xx = np.sum((x - np.mean(x)) ** 2)
    SS_T = np.sum((y - np.mean(y)) ** 2)
    S_xy = np.sum((x - np.mean(x)) * (y - np.mean(y)))

    # Hệ số tương quan mẫu r
    r = S_xy / np.sqrt(S_xx * SS_T)

    # Kiểm định 1: H0: rho = 0 (phân phối t với n - 2 bậc tự do)
    t0 = r * np.sqrt(n - 2) / np.sqrt(1.0 - r ** 2)
    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 2)

    # Kiểm định 2: H0: rho = rho0 (phép biến đổi Fisher, áp dụng khi n >= 25)
    u = 0.5 * np.log((1.0 + r) / (1.0 - r))
    u0 = 0.5 * np.log((1.0 + rho0) / (1.0 - rho0))
    z0 = (u - u0) / np.sqrt(1.0 / (n - 3))
    z_crit = stats.norm.ppf(1 - alpha / 2)

    # Khoảng tin cậy 95% cho rho (n >= 25)
    ci_low = np.tanh(np.arctanh(r) - z_crit / np.sqrt(n - 3))
    ci_high = np.tanh(np.arctanh(r) + z_crit / np.sqrt(n - 3))

    return {
        "n": n, "r": r, "r_squared": r ** 2,
        "t0": t0, "t_crit": t_crit,
        "rho0": rho0, "u": u, "u0": u0, "z0": z0, "z_crit": z_crit,
        "ci_rho": (ci_low, ci_high),
    }


def plot_corr_heatmap(df: pd.DataFrame, fig_dir: Path) -> None:
    fig_dir.mkdir(parents=True, exist_ok=True)
    cols = ["Y_close", "x1_open", "x2_prev_volume", "x3_prev_change", "x4_time_index"]
    corr_mat = df[cols].corr()

    plt.figure(figsize=(7, 5.5))
    sns.heatmap(corr_mat, annot=True, fmt=".4f", cmap="Blues", vmin=-1, vmax=1, square=True)
    plt.title("Ma trận tương quan giữa các biến (MI3031)")
    plt.tight_layout()
    plt.savefig(fig_dir / "heatmap_corr.png", dpi=300)
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv(CLEAN_PATH)
    res = correlation_analysis_from_scratch(df["x1_open"].to_numpy(), df["Y_close"].to_numpy(), rho0=0.95)
    print(f"Hệ số tương quan mẫu r = {res['r']:.4f} | r^2 = {res['r_squared']:.4f} (đối chiếu R^2 của TV1)")
    print(f"Kiểm định H0: rho = 0 -> t0 = {res['t0']:.4f}, t_crit = {res['t_crit']:.4f}")
    print(f"Kiểm định H0: rho = {res['rho0']} -> z0 = {res['z0']:.4f}, z_crit = {res['z_crit']:.4f}")
    print(f"KTC 95% cho rho: ({res['ci_rho'][0]:.4f}, {res['ci_rho'][1]:.4f})")

    plot_corr_heatmap(df, FIG_DIR)
