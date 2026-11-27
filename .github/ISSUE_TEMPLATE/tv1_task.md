---
name: "[TV1] Nhiệm vụ Mục 1-3 & Tổng hợp Báo cáo"
about: Theo dõi tiến độ Thành viên 1 (MI3031 Chương 4)
labels: tv1, slr, report
---

## Checklist chi tiết Thành viên 1
### Mục 1 & 2: Dữ liệu (Hạn 27/11 - 22:00)
- [ ] Thu thập & mô tả dữ liệu gốc (nguồn, mã, số quan sát $n_0$, đơn vị).
- [ ] Làm sạch giá trị khuyết, trùng lặp, sắp xếp theo thời gian.
- [ ] Tạo biến $x_2$ (KL phiên trước), $x_3$ (thay đổi so với phiên trước, không rò rỉ dữ liệu), $x_4$ (thời điểm).
- [ ] Xuất `data/clean/data_clean.csv` và push lên `main`.

### Mục 3: Hồi quy tuyến tính đơn (Hạn 29/11 - 21:00)
- [ ] Viết mô hình $Y = \beta_0 + \beta_1 x + \epsilon$ và Giả thiết 1.
- [ ] Tự code OLS ($S_{xx}, S_{xy}, \hat{\beta}_1, \hat{\beta}_0$).
- [ ] Tự code ANOVA ($SS_T, SS_R, SS_E, MS_R, MS_E, s^2, s, se(\hat{\beta}_0), se(\hat{\beta}_1)$).
- [ ] Kiểm định $H_0: \beta_1 = 0$ bằng cả $t_0$ và $f_0$ ($\alpha = 5\%$).
- [ ] Tính KTC 95% cho $\beta_0, \beta_1$, KTC cho $\mu_{Y|x_0}$ và khoảng dự đoán cho $y_0$.
- [ ] Tính $R^2$, phần dư chuẩn hóa $d_i = e_i/s$ và xuất 3 bộ biểu đồ vào `thanh_vien_1/figures/`.

### Báo cáo & Slide (Hạn 01/12 - 22:00)
- [ ] Viết Mục 1, 2, 3 và gửi dàn ý slide Mục 1–3 cho TV2 (30/11).
- [ ] Tổng hợp, định dạng toàn bộ Báo cáo hoàn chỉnh (01/12).
- [ ] Duyệt chéo Slide của TV2 (02/12).
