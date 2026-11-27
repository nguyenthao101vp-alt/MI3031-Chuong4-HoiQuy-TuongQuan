# Không gian làm việc – Thành viên 2

**Phạm vi phụ trách:** Mục 4 (Phân tích tương quan), Mục 5 (Hồi quy tuyến tính bội dạng ma trận) & Chủ trì thiết kế Slide thuyết trình.

## Danh sách file
1. `03_correlation_analysis.py`: Tính hệ số tương quan mẫu $r$, kiểm định $H_0: \rho = 0$ và $H_0: \rho = \rho_0$ (biến đổi Fisher), KTC 95% cho $\rho$, vẽ heatmap tương quan.
2. `04_multiple_linear_regression.py`: Xây dựng ma trận $\mathbf{X}$ ($n \times 5$), kiểm tra khả nghịch, tính $\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top \mathbf{y}$, ANOVA bội, $R^2_{\text{adj}}$, kiểm định $t$ từng hệ số riêng và đối chiếu với `statsmodels.OLS`.

## Biểu đồ cần xuất (300 DPI)
- `figures/heatmap_corr.png`
- `figures/actual_vs_pred_mlr.png`
- `figures/residuals_mlr.png`
