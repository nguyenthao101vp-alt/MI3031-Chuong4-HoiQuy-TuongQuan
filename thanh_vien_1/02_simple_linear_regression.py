# -*- coding: utf-8 -*-
"""
TV1 - Mục 3: Mô hình hồi quy tuyến tính đơn (Y_close theo x1_open).
Cài đặt thủ công theo đúng công thức Slide 4.1 (MI3031), đối chiếu bằng scipy.stats / statsmodels.
Chạy: python 02_simple_linear_regression.py   (đặt cạnh data_clean.csv hoặc trong code\\, data\\)
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams.update({"font.family": "DejaVu Sans", "axes.grid": True, "grid.alpha": 0.3})

# ---------- Đường dẫn: tự tìm data_clean.csv ----------
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent if HERE.name.lower() == "code" else HERE
CANDIDATES = [ROOT / "data" / "data_clean.csv", ROOT / "data" / "clean" / "data_clean.csv", HERE / "data_clean.csv"]
CLEAN_PATH = next((p for p in CANDIDATES if p.exists()), CANDIDATES[0])
FIG_DIR = ROOT / "figures"
ALPHA = 0.05


def simple_linear_regression_from_scratch(x: np.ndarray, y: np.ndarray, alpha: float = ALPHA) -> dict:
    n = len(x)
    x_bar, y_bar = np.mean(x), np.mean(y)

    # Tổng bình phương & tích chéo
    S_xx = np.sum((x - x_bar) ** 2)
    S_xy = np.sum((x - x_bar) * (y - y_bar))
    SS_T = np.sum((y - y_bar) ** 2)

    # Ước lượng OLS
    beta1_hat = S_xy / S_xx
    beta0_hat = y_bar - beta1_hat * x_bar
    y_hat = beta0_hat + beta1_hat * x
    residuals = y - y_hat

    # ANOVA
    SS_R = beta1_hat * S_xy
    SS_E = SS_T - SS_R
    MS_R = SS_R / 1.0
    MS_E = SS_E / (n - 2)
    s2 = MS_E
    s = np.sqrt(s2)

    # Sai số chuẩn
    se_beta1 = s / np.sqrt(S_xx)
    se_beta0 = s * np.sqrt(1.0 / n + (x_bar ** 2) / S_xx)

    # Kiểm định
    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 2)
    f_crit = stats.f.ppf(1 - alpha, dfn=1, dfd=n - 2)
    t0_beta1 = beta1_hat / se_beta1                      # H0: beta1 = 0
    p_t = 2 * stats.t.sf(abs(t0_beta1), n - 2)
    f0 = MS_R / MS_E
    p_f = stats.f.sf(f0, 1, n - 2)
    t0_beta0 = beta0_hat / se_beta0                      # H0: beta0 = 0
    p_b0 = 2 * stats.t.sf(abs(t0_beta0), n - 2)
    t0_eq1 = (beta1_hat - 1.0) / se_beta1                # H0: beta1 = 1
    p_eq1 = 2 * stats.t.sf(abs(t0_eq1), n - 2)

    # Khoảng tin cậy
    ci_beta1 = (beta1_hat - t_crit * se_beta1, beta1_hat + t_crit * se_beta1)
    ci_beta0 = (beta0_hat - t_crit * se_beta0, beta0_hat + t_crit * se_beta0)

    # R2, phần dư chuẩn hóa
    R2 = SS_R / SS_T
    d_std = residuals / s

    return {
        "n": n, "x_bar": x_bar, "y_bar": y_bar,
        "S_xx": S_xx, "S_xy": S_xy, "SS_T": SS_T, "SS_R": SS_R, "SS_E": SS_E,
        "MS_R": MS_R, "MS_E": MS_E, "s2": s2, "s": s,
        "beta0_hat": beta0_hat, "beta1_hat": beta1_hat, "se_beta0": se_beta0, "se_beta1": se_beta1,
        "t_crit": t_crit, "f_crit": f_crit,
        "t0_beta1": t0_beta1, "p_t": p_t, "f0": f0, "p_f": p_f,
        "t0_beta0": t0_beta0, "p_b0": p_b0, "t0_eq1": t0_eq1, "p_eq1": p_eq1,
        "ci_beta0": ci_beta0, "ci_beta1": ci_beta1,
        "R2": R2, "y_hat": y_hat, "residuals": residuals, "d_std": d_std,
    }


def predict_intervals(res: dict, x0: float, alpha: float = ALPHA) -> dict:
    y0_hat = res["beta0_hat"] + res["beta1_hat"] * x0
    t_crit = stats.t.ppf(1 - alpha / 2, df=res["n"] - 2)
    term = (x0 - res["x_bar"]) ** 2 / res["S_xx"]
    half_ci = t_crit * np.sqrt(res["s2"] * (1.0 / res["n"] + term))
    half_pi = t_crit * np.sqrt(res["s2"] * (1.0 + 1.0 / res["n"] + term))
    return {"x0": x0, "y0_hat": y0_hat,
            "ci_mean": (y0_hat - half_ci, y0_hat + half_ci),
            "pi_single": (y0_hat - half_pi, y0_hat + half_pi)}


def residual_diagnostics(res: dict, dates=None) -> dict:
    e, d = res["residuals"], res["d_std"]
    idx = np.where(np.abs(d) > 2)[0]
    sw = stats.shapiro(e)
    dw = np.sum(np.diff(e) ** 2) / np.sum(e ** 2)                  # Durbin-Watson
    sp = stats.spearmanr(np.abs(e), res["y_hat"])                   # gợi ý hình phễu
    return {"n_out": int(len(idx)), "pct_out": len(idx) / len(e) * 100, "idx": idx.tolist(),
            "dates": [str(dates[i])[:10] for i in idx] if dates is not None else None,
            "d_out": [float(d[i]) for i in idx], "max_abs_d": float(np.abs(d).max()),
            "shapiro_W": float(sw.statistic), "shapiro_p": float(sw.pvalue), "DW": float(dw),
            "spearman_rho": float(sp.statistic), "spearman_p": float(sp.pvalue)}


def five_steps(name, h0, h1, stat, region, value, reject, note=""):
    print(f"\n[{name}]\n 1) H0: {h0};  H1: {h1}\n 2) Mức ý nghĩa alpha = {ALPHA}\n 3) Tiêu chuẩn: {stat}"
          f"\n 4) Miền bác bỏ: {region}\n 5) Tính toán: {value}  =>  {'BÁC BỎ H0' if reject else 'KHÔNG BÁC BỎ H0'}. {note}")


def plot_slr_figures(x, y, res, t_index, fig_dir: Path) -> None:
    fig_dir.mkdir(parents=True, exist_ok=True)
    n, s, tc = res["n"], res["s"], res["t_crit"]
    xs = np.linspace(x.min() - 0.2, x.max() + 0.2, 200)
    ys = res["beta0_hat"] + res["beta1_hat"] * xs
    h = 1 / n + (xs - res["x_bar"]) ** 2 / res["S_xx"]
    label_eq = f"ŷ = {res['beta0_hat']:.4f} + {res['beta1_hat']:.4f}x"

    # (1) Phân tán + đường hồi quy
    plt.figure(figsize=(7, 5))
    plt.scatter(x, y, s=28, alpha=0.8, label="Quan sát thực tế")
    plt.plot(xs, ys, color="red", linewidth=2, label=label_eq)
    plt.xlabel("Giá mở cửa cùng phiên (x)"); plt.ylabel("Giá đóng cửa cùng phiên (Y)")
    plt.title("Hồi quy tuyến tính đơn: Giá đóng cửa theo Giá mở cửa"); plt.legend()
    plt.tight_layout(); plt.savefig(fig_dir / "fig1_scatter_regression.png", dpi=300); plt.close()

    # (2) Dải KTC & dải khoảng dự đoán 95%
    plt.figure(figsize=(7, 5))
    plt.scatter(x, y, s=24, alpha=0.8, label="Quan sát")
    plt.plot(xs, ys, color="red", linewidth=2, label="Đường hồi quy")
    plt.fill_between(xs, ys - tc * s * np.sqrt(h), ys + tc * s * np.sqrt(h), color="green", alpha=0.35,
                     label="Dải KTC 95% cho trung bình")
    plt.plot(xs, ys - tc * s * np.sqrt(1 + h), "--", color="orange", label="Dải khoảng dự đoán 95%")
    plt.plot(xs, ys + tc * s * np.sqrt(1 + h), "--", color="orange")
    plt.xlabel("Giá mở cửa (x)"); plt.ylabel("Giá đóng cửa (Y)"); plt.title("Khoảng tin cậy và khoảng dự đoán 95%")
    plt.legend(loc="upper left", fontsize=9)
    plt.tight_layout(); plt.savefig(fig_dir / "fig2_ci_pi_bands.png", dpi=300); plt.close()

    # (3) Bộ 4 biểu đồ chẩn đoán phần dư
    e = res["residuals"]
    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    axes[0, 0].scatter(res["y_hat"], e, alpha=0.7); axes[0, 0].axhline(0, color="red", linestyle="--")
    axes[0, 0].set_title("(a) Phần dư theo giá trị dự báo ŷ")
    axes[0, 1].scatter(x, e, alpha=0.7); axes[0, 1].axhline(0, color="red", linestyle="--")
    axes[0, 1].set_title("(b) Phần dư theo biến độc lập x")
    axes[1, 0].plot(t_index, e, marker="o", markersize=3, linewidth=0.8); axes[1, 0].axhline(0, color="red", linestyle="--")
    axes[1, 0].set_title("(c) Phần dư theo trình tự thời gian")
    stats.probplot(res["d_std"], dist="norm", plot=axes[1, 1]); axes[1, 1].set_title("(d) Biểu đồ xác suất chuẩn (Q–Q)")
    for ax in axes.ravel()[:3]:
        ax.set_ylabel("Phần dư e")
    plt.tight_layout(); plt.savefig(fig_dir / "fig3_residual_diagnostics.png", dpi=300); plt.close()


if __name__ == "__main__":
    df = pd.read_csv(CLEAN_PATH, parse_dates=["Ngay"] if "Ngay" in pd.read_csv(CLEAN_PATH, nrows=0).columns else None)
    df = df.rename(columns={"x1_open": "x", "Y_close": "Y"})          # chấp nhận cả hai cách đặt tên cột
    x, y = df["x"].to_numpy(float), df["Y"].to_numpy(float)
    t_index = np.arange(1, len(x) + 1)
    dates = df["Ngay"].to_numpy() if "Ngay" in df.columns else None

    res = simple_linear_regression_from_scratch(x, y)
    print(f"n = {res['n']}  x_bar = {res['x_bar']:.4f}  y_bar = {res['y_bar']:.4f}  S_xx = {res['S_xx']:.4f}  S_xy = {res['S_xy']:.4f}")
    print(f"Phương trình hồi quy: y_hat = {res['beta0_hat']:.4f} + {res['beta1_hat']:.4f} * x")
    print(f"se(b0) = {res['se_beta0']:.4f} | se(b1) = {res['se_beta1']:.4f}")

    print("\n=== BẢNG ANOVA ===")
    print(f"Hồi quy : SS = {res['SS_R']:.4f} | df = 1      | MS = {res['MS_R']:.4f} | f0 = {res['f0']:.4f}")
    print(f"Sai số  : SS = {res['SS_E']:.4f} | df = {res['n']-2:<4d} | MS = {res['MS_E']:.4f}")
    print(f"Tổng    : SS = {res['SS_T']:.4f} | df = {res['n']-1}")
    print(f"s^2 = {res['s2']:.4f} | s = {res['s']:.4f} | R^2 = {res['R2']:.4f} | r = {np.sign(res['beta1_hat'])*np.sqrt(res['R2']):.4f}")

    five_steps("Kiểm định t: ý nghĩa hồi quy", "beta1 = 0", "beta1 != 0", "t0 = b1/se(b1) ~ t(n-2)",
               f"|t0| > {res['t_crit']:.4f}", f"t0 = {res['t0_beta1']:.4f}, p = {res['p_t']:.3e}", abs(res['t0_beta1']) > res['t_crit'])
    five_steps("Kiểm định F: ý nghĩa hồi quy", "beta1 = 0", "beta1 != 0", "f0 = MSR/MSE ~ F(1, n-2)",
               f"f0 > {res['f_crit']:.4f}", f"f0 = {res['f0']:.4f}, p = {res['p_f']:.3e}", res['f0'] > res['f_crit'],
               f"Kiểm chứng t0^2 = {res['t0_beta1']**2:.4f} = f0 = {res['f0']:.4f}")
    five_steps("Kiểm định t: biến động 1-1", "beta1 = 1", "beta1 != 1", "t0 = (b1 - 1)/se(b1) ~ t(n-2)",
               f"|t0| > {res['t_crit']:.4f}", f"t0 = {res['t0_eq1']:.4f}, p = {res['p_eq1']:.4f}", abs(res['t0_eq1']) > res['t_crit'])
    print(f"\n[Kiểm định beta0 = 0] t0 = {res['t0_beta0']:.4f}, p = {res['p_b0']:.4f}")

    print(f"\nKTC 95% beta1: ({res['ci_beta1'][0]:.4f}, {res['ci_beta1'][1]:.4f})")
    print(f"KTC 95% beta0: ({res['ci_beta0'][0]:.4f}, {res['ci_beta0'][1]:.4f})")

    print("\n=== DỰ ĐOÁN ===")
    for x0 in (31.0, 29.5, res["x_bar"]):
        p = predict_intervals(res, x0)
        print(f"x0 = {p['x0']:.4f}: y0_hat = {p['y0_hat']:.4f}")
        print(f"  KTC 95% trung bình : ({p['ci_mean'][0]:.4f}, {p['ci_mean'][1]:.4f})  rộng {p['ci_mean'][1]-p['ci_mean'][0]:.4f}")
        print(f"  Khoảng dự đoán 95% : ({p['pi_single'][0]:.4f}, {p['pi_single'][1]:.4f})  rộng {p['pi_single'][1]-p['pi_single'][0]:.4f}")

    dg = residual_diagnostics(res, dates)
    print("\n=== PHẦN DƯ ===")
    print(f"Số phiên |d| > 2: {dg['n_out']} ({dg['pct_out']:.2f}%), ngày: {dg['dates']}, d = {[round(v,4) for v in dg['d_out']]}, max|d| = {dg['max_abs_d']:.4f}")
    print(f"Shapiro-Wilk W = {dg['shapiro_W']:.4f} (p = {dg['shapiro_p']:.4f}) | Durbin-Watson = {dg['DW']:.4f} | Spearman(|e|, y_hat) = {dg['spearman_rho']:.4f} (p = {dg['spearman_p']:.4f})")

    # Đối chiếu thư viện
    lr = stats.linregress(x, y)
    ok = np.allclose([lr.slope, lr.intercept, lr.stderr, lr.intercept_stderr, lr.rvalue**2],
                     [res["beta1_hat"], res["beta0_hat"], res["se_beta1"], res["se_beta0"], res["R2"]], atol=1e-9)
    print(f"\n[Đối chiếu scipy.stats.linregress] beta0 = {lr.intercept:.4f}, beta1 = {lr.slope:.4f}, R^2 = {lr.rvalue**2:.4f} -> {'KHỚP' if ok else 'LỆCH'}")
    try:
        import statsmodels.api as sm
        m = sm.OLS(y, sm.add_constant(x)).fit()
        ok2 = np.allclose(m.params, [res["beta0_hat"], res["beta1_hat"]]) and np.isclose(m.fvalue, res["f0"]) and np.isclose(m.rsquared, res["R2"])
        print(f"[Đối chiếu statsmodels.OLS] -> {'KHỚP' if ok2 else 'LỆCH'}")
    except ImportError:
        print("(Chưa cài statsmodels: py -m pip install statsmodels để đối chiếu thêm)")

    plot_slr_figures(x, y, res, t_index, FIG_DIR)
    print(f"\nĐã lưu 3 biểu đồ (300 DPI) vào: {FIG_DIR}")
