# -*- coding: utf-8 -*-
"""Muc 4 (tuong quan) va Muc 5 (hoi quy tuyen tinh boi dang ma tran).
Mo hinh: Y = beta0 + beta1*x1 + beta4*x4 + sai so
    Y  : gia dong cua
    x1 : gia mo cua cung phien
    x4 : thu tu phien giao dich
Chay tu thu muc goc cua du an:  python code/02_tuong_quan_hoi_quy_boi.py
"""
import os
import sys
import numpy as np
import pandas as pd
from scipy import stats

MUC_Y_NGHIA = 0.05
BIEN_GIAI_THICH = ["x1", "x4"]


# ===== MUC 4. TUONG QUAN ==================================================
def he_so_tuong_quan(x, y):
    """r = Sxy / can(Sxx * SST)  (cong thuc 46)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    lech_x, lech_y = x - x.mean(), y - y.mean()
    return (lech_x @ lech_y) / np.sqrt((lech_x @ lech_x) * (lech_y @ lech_y))


def kiem_dinh_rho_bang_0(r, co_mau, alpha=MUC_Y_NGHIA):
    """H0: rho = 0; H1: rho != 0. T0 ~ t(n-2)  (cong thuc 49)."""
    t_quan_sat = r * np.sqrt(co_mau - 2) / np.sqrt(1 - r**2)
    t_toi_han = stats.t.ppf(1 - alpha / 2, co_mau - 2)
    gia_tri_p = 2 * stats.t.sf(abs(t_quan_sat), co_mau - 2)
    return t_quan_sat, t_toi_han, gia_tri_p, abs(t_quan_sat) > t_toi_han


def khoang_tin_cay_rho(r, co_mau, alpha=MUC_Y_NGHIA):
    """Khoang tin cay xap xi cho rho, n >= 25  (cong thuc 54)."""
    if co_mau < 25:
        raise ValueError("Can n >= 25")
    ban_kinh = stats.norm.ppf(1 - alpha / 2) / np.sqrt(co_mau - 3)
    return np.tanh(np.arctanh(r) - ban_kinh), np.tanh(np.arctanh(r) + ban_kinh)


# ===== MUC 5. HOI QUY BOI DANG MA TRAN ====================================
def uoc_luong_binh_phuong_nho_nhat(bang_x, vec_y):
    """beta = (X'X)^(-1) X'y. bang_x chua co cot he so chan."""
    vec_y = np.asarray(vec_y, float)
    ma_tran_x = np.column_stack([np.ones(len(vec_y)), np.asarray(bang_x, float)])
    co_mau, so_tham_so = ma_tran_x.shape
    if np.linalg.matrix_rank(ma_tran_x) < so_tham_so:
        raise ValueError("Ma tran X khong du hang cot")
    xtx = ma_tran_x.T @ ma_tran_x
    xty = ma_tran_x.T @ vec_y
    # Giai he phuong trinh chuan X'X * beta = X'y
    beta = np.linalg.solve(xtx, xty)
    y_du_doan = ma_tran_x @ beta
    phan_du = vec_y - y_du_doan
    sse = phan_du @ phan_du
    sst = np.sum((vec_y - vec_y.mean())**2)
    phuong_sai_sai_so = sse / (co_mau - so_tham_so)
    return {
        "ma_tran_x": ma_tran_x, "xtx": xtx, "xty": xty,
        "nghich_dao_xtx": np.linalg.inv(xtx), "beta": beta,
        "y_du_doan": y_du_doan, "phan_du": phan_du,
        "SST": sst, "SSR": sst - sse, "SSE": sse,
        "phuong_sai_sai_so": phuong_sai_sai_so,
        "R2": 1 - sse / sst,
        "R2_hieu_chinh": 1 - phuong_sai_sai_so / (sst / (co_mau - 1)),
    }


# ===== CHUONG TRINH CHINH =================================================
def chay_chuong_trinh():
    thu_muc_goc = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    duong_dan = (sys.argv[1] if len(sys.argv) > 1
                 else os.path.join(thu_muc_goc, "data", "data_clean.csv"))
    thu_muc_ket_qua = os.path.join(thu_muc_goc, "ket_qua")
    os.makedirs(thu_muc_ket_qua, exist_ok=True)

    def luu_bang(bang, ten_file, **tuy_chon):
        bang.to_csv(os.path.join(thu_muc_ket_qua, ten_file), encoding="utf-8-sig", **tuy_chon)

    du_lieu = pd.read_csv(duong_dan, encoding="utf-8-sig", parse_dates=["Ngay"])
    du_lieu = du_lieu.sort_values("Ngay").reset_index(drop=True)
    cac_cot = ["Y"] + BIEN_GIAI_THICH
    assert du_lieu[cac_cot].notna().all().all(), "Du lieu con gia tri khuyet"
    co_mau = len(du_lieu)
    print(f"n = {co_mau}, alpha = {MUC_Y_NGHIA}")

    print("\n=== MUC 4: TUONG QUAN ===")
    ma_tran_tuong_quan = du_lieu[cac_cot].corr()
    print(ma_tran_tuong_quan.round(4).to_string())
    luu_bang(ma_tran_tuong_quan, "ma_tran_tuong_quan.csv")

    cac_dong = []
    for bien_1, bien_2 in [("x1", "Y"), ("x4", "Y"), ("x1", "x4")]:
        r = he_so_tuong_quan(du_lieu[bien_1], du_lieu[bien_2])
        t_quan_sat, t_toi_han, gia_tri_p, bac_bo = kiem_dinh_rho_bang_0(r, co_mau)
        can_duoi, can_tren = khoang_tin_cay_rho(r, co_mau)
        cac_dong.append({"cap_bien": f"{bien_1}-{bien_2}", "r": r, "t_quan_sat": t_quan_sat,
                         "t_toi_han": t_toi_han, "gia_tri_p": gia_tri_p,
                         "bac_bo_H0": bool(bac_bo), "can_duoi": can_duoi, "can_tren": can_tren})
    bang_kiem_dinh = pd.DataFrame(cac_dong)
    print(bang_kiem_dinh.to_string(index=False, float_format=lambda v: f"{v:.6g}"))
    luu_bang(bang_kiem_dinh, "kiem_dinh_tuong_quan.csv", index=False)

    print("\n=== MUC 5: HOI QUY BOI (MA TRAN) ===")
    mo_hinh = uoc_luong_binh_phuong_nho_nhat(du_lieu[BIEN_GIAI_THICH], du_lieu["Y"])
    for ten, khoa in [("X'X", "xtx"), ("X'y", "xty"),
                      ("(X'X)^(-1)", "nghich_dao_xtx"), ("beta", "beta")]:
        print(f"{ten} =\n{mo_hinh[khoa]}")
    he_so_chan, he_so_x1, he_so_x4 = mo_hinh["beta"]
    print(f"y_du_doan = {he_so_chan:.6f} {he_so_x1:+.6f}*x1 {he_so_x4:+.6f}*x4")
    for khoa in ["SST", "SSR", "SSE", "phuong_sai_sai_so", "R2", "R2_hieu_chinh"]:
        print(f"{khoa} = {mo_hinh[khoa]:.6f}")

    luu_bang(pd.DataFrame({"he_so": ["beta0", "beta1", "beta4"], "uoc_luong": mo_hinh["beta"]}),
             "he_so_hoi_quy.csv", index=False)
    luu_bang(du_lieu[["Ngay", "Y"]].assign(y_du_doan=mo_hinh["y_du_doan"],
             phan_du=mo_hinh["phan_du"]), "gia_tri_du_doan.csv", index=False)
    print(f"\nDa luu ket qua vao {thu_muc_ket_qua}")


if __name__ == "__main__":
    chay_chuong_trinh()
