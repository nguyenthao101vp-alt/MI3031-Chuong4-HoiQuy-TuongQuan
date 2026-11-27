# Quy ước làm việc nhóm trên GitHub

## 1. Quy ước nhánh (Branching)
Không push trực tiếp code chưa kiểm tra lên nhánh `main`. Mỗi thành viên làm việc trên nhánh riêng:
- Thành viên 1: `tv1/data-and-slr`
- Thành viên 2: `tv2/corr-and-mlr`

```bash
# Tạo và chuyển sang nhánh riêng
git checkout -b tv1/data-and-slr

# Lưu thay đổi và đẩy lên GitHub
git add thanh_vien_1/ data/clean/
git commit -m "tv1: hoan thien OLS don bien va bang ANOVA"
git push -u origin tv1/data-and-slr
```
Sau khi hoàn thành mỗi mốc bàn giao, mở **Pull Request (PR)** vào `main` để thành viên còn lại duyệt chéo.

## 2. Quy ước đồng bộ kỹ thuật
1. **Làm tròn số liệu:** Thống nhất **4 chữ số thập phân** cho $\hat{\beta}$, $r$, $R^2$, $R^2_{\text{adj}}$, $t_0$, $f_0$, sai số chuẩn.
2. **Kiểm tra chéo bắt buộc:**
   - $r^2$ (Mục 4 – TV2) phải bằng tuyệt đối $R^2$ (Mục 3 – TV1).
   - $t_0^2$ khi kiểm định $H_0: \beta_1 = 0$ phải bằng $f_0$ trong bảng ANOVA Mục 3.
3. **Không xung đột file:**
   - TV1 chỉ sửa file trong `thanh_vien_1/`, `data/clean/` và `report/`.
   - TV2 chỉ sửa file trong `thanh_vien_2/` và `slides/`.
