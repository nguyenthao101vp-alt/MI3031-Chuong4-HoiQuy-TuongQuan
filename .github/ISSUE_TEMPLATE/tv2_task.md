---
name: "[TV2] Nhiệm vụ Mục 4-5 & Thiết kế Slide"
about: Theo dõi tiến độ Thành viên 2 (MI3031 Chương 4)
labels: tv2, mlr, slides
---

## Checklist chi tiết Thành viên 2
### Kiểm tra dữ liệu chung (Hạn 27/11 - 22:00)
- [ ] Kiểm tra chéo `data/clean/data_clean.csv` (không NaN, biến trễ đúng thứ tự thời gian).

### Mục 4: Phân tích tương quan (Hạn 28/11 - 22:00)
- [ ] Tự code hệ số tương quan mẫu $r$, kiểm chứng $r^2 = R^2$ với TV1.
- [ ] Xếp loại mức độ tương quan theo bảng chuẩn slide.
- [ ] Kiểm định $H_0: \rho = 0$ (thống kê $t_0$) và $H_0: \rho = \rho_0$ (biến đổi Fisher $Z_0$, $n \ge 25$).
- [ ] Tính KTC 95% cho $\rho$ bằng hàm $\tanh / \operatorname{arctanh}$.
- [ ] Phân tích tương quan vs. nhân quả và chỉ ra các biến giấu mặt.

### Mục 5: Hồi quy tuyến tính bội dạng ma trận (Hạn 29/11 - 21:00)
- [ ] Thiết lập ma trận $\mathbf{X}$ ($n \times 5$), vectơ $\mathbf{y}$ ($n \times 1$) và nêu Giả thiết 2.
- [ ] Kiểm tra điều kiện khả nghịch $\det(\mathbf{X}^\top \mathbf{X}) \neq 0$ và tính $\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top \mathbf{y}$.
- [ ] Tính $SS_E$, $s^2 = SS_E/(n-5)$, ma trận hiệp phương sai $s^2\mathbf{C}$, $se(\hat{\beta}_j)$.
- [ ] Lập bảng ANOVA bội, kiểm định $F$ toàn mô hình, tính $R^2$ và $R^2_{\text{adj}}$.
- [ ] Kiểm định $t$ từng hệ số hồi quy riêng và so sánh với mô hình đơn.
- [ ] Xuất biểu đồ heatmap, $\hat{y}$ vs $y$ và phần dư vào `thanh_vien_2/figures/`.

### Báo cáo & Slide (Hạn 01/12 - 22:00)
- [ ] Viết Mục 4, 5 và phần so sánh 2 mô hình gửi TV1 (30/11).
- [ ] Chủ trì thiết kế hoàn thiện toàn bộ Slide thuyết trình (01/12).
- [ ] Duyệt chéo Báo cáo & chạy lại toàn bộ code từ đầu (02/12).
