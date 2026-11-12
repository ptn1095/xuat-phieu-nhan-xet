# Xuất Phiếu Nhận Xét · Tiểu học

Webapp tạo **phiếu nhận xét PDF** cho từng học sinh từ file Excel nhận xét (STEM, Tin học, Công nghệ, Robotics).
Tải Excel lên, chỉnh mẫu phiếu, rồi tải về một file ZIP chứa PDF của cả lớp hoặc cả trường.

**Dùng ngay:** https://ptn1095.github.io/xuat-phieu-nhan-xet/

Hoặc tải file [`index.html`](index.html) về máy và mở bằng Chrome hay Edge. App chạy offline hoàn toàn. Dữ liệu học sinh chỉ được xử lý trong trình duyệt, không gửi lên máy chủ nào.

## Cách dùng

1. **Tải Excel**: kéo thả file `.xlsx` vào ô "Tải file Excel nhận xét". Mỗi sheet là một lớp, mỗi dòng là một học sinh.
2. **Chọn thời điểm**: GHKI, HKI, GHKII hoặc HKII. Tiêu đề phiếu và tên file đổi theo.
3. **Chọn môn**: chọn 1, 2, 3 hoặc cả 4 môn (STEM, Tin học, CN, Robotics). Môn nào học sinh không có dữ liệu sẽ tự bỏ khỏi phiếu.
4. **Chỉnh phiếu** nếu cần: tiêu đề, lời gửi, các cột, các tiêu chí (bật/tắt, đổi tên, đổi thứ tự, thêm mới), phụ lục và chữ ký.
5. Bấm vào một học sinh để **xem trước**, rồi bấm **Xuất … phiếu (ZIP)**.

Cài đặt tự lưu trên trình duyệt. Dùng **Lưu mẫu / Mở mẫu** để gửi mẫu phiếu (file `.json`) cho đồng nghiệp.

### Phiếu tạo ra

- Khổ A4, có dải trang trí ở đầu và chân trang, logo nằm trên nền trắng.
- Mỗi môn một trang, có dòng tiêu đề cột riêng.
- Ô trống (ví dụ chưa có điểm) tự ẩn dòng đó.
- Phần tiêu chí, thang đánh giá và chữ ký ở cuối phiếu.

Xem ví dụ: [`examples/Nguyễn Minh Anh_GHKI_STEM Tin học.pdf`](examples/).

### Tên file

Mẫu mặc định là `{HoTen}_{ThoiDiem}_{Mon}`, ví dụ `Nguyễn Minh Anh_HKI_STEM Tin học.pdf`.
Các biến dùng được: `{HoTen}`, `{Lop}`, `{MaHS}`, `{STT}`, `{ThoiDiem}`, `{Mon}`, `{NamHoc}`. Có tuỳ chọn bỏ dấu tiếng Việt. Tên trùng nhau thì app tự thêm `_2`, `_3`.

Khi xuất, bạn chọn được: mỗi học sinh 1 file PDF, mỗi lớp 1 file PDF gộp (để in), hoặc cả hai. Trong file ZIP, mỗi lớp nằm trong một thư mục riêng.

## Định dạng file Excel

Xem file mẫu [`examples/mau-nhan-xet.xlsx`](examples/mau-nhan-xet.xlsx).

App nhận cột theo **tên tiêu đề**, không theo vị trí, nên các cột có thể xếp theo thứ tự bất kỳ. Dấu, chữ hoa/thường và khoảng trắng đều được bỏ qua.

| Cột | Ví dụ tiêu đề |
|---|---|
| Họ tên (bắt buộc) | `Họ và tên` |
| Lớp | `Lớp` (nếu không có cột này, app lấy tên sheet) |
| Mã học sinh | `Mã HS` |
| Nội dung học | `Nội dung họcS`, `Nội dung họcTin`, `Nội dung học Robot` |
| 5 tiêu chí (T / H / K) | `Tinh thầnS`, `Khả năng tiếp thuTin`, `Thái độ hợp tác Robot`, `Khả năng sáng tạoS`, `Kết quả học tậpS` |
| Mức đánh giá chung | `Mức đánh giá chungS` |
| Nhận xét | `Nhận xétS` |
| Điểm | `Điểm STEM`, `Điểm Tin` |

Phần đuôi của tên cột (**hậu tố**) cho biết cột đó thuộc môn nào. Hậu tố mặc định:

| Môn | Hậu tố |
|---|---|
| STEM | `S`, `STEM` |
| Tin học | `Tin`, `Tin học` |
| Công nghệ | `CN`, `Công nghệ` |
| Robotics | `Robot`, `Robotics` |

Bạn sửa được hậu tố của từng môn ngay trong app. Trước khi xuất, app hiện danh sách những chỗ cần kiểm tra: ô tiêu chí không phải T/H/K, thiếu nhận xét, học sinh không có dữ liệu, tên file trùng, cột không nhận ra.

## Phát triển

```bash
npm ci
```

```bash
pip install fonttools
```

```bash
python3 build.py
```

Lệnh `build.py` gộp `src/app.src.html`, các thư viện trong `node_modules`, font và ảnh trong `assets/` thành một file `index.html` duy nhất.

```
src/app.src.html     Giao diện và logic của app
assets/fonts/        Font Liberation Serif gốc và giấy phép OFL
assets/img/          Dải đầu trang, chân trang, logo
examples/            File Excel mẫu và phiếu PDF mẫu (dữ liệu giả)
build.py             Script đóng gói
index.html           Bản đã build, dùng cho GitHub Pages
```

Thư viện dùng: [SheetJS](https://sheetjs.com) 0.18.5 để đọc Excel, [pdfmake](https://pdfmake.github.io) 0.3.10 để tạo PDF, [JSZip](https://stuk.github.io/jszip/) 3.10.1 để nén ZIP.

## Giấy phép font

Font trong PDF là bản cắt gọn của **Liberation Serif**, phát hành theo giấy phép SIL Open Font License 1.1 (xem [`assets/fonts/OFL.txt`](assets/fonts/OFL.txt)). Vì "Liberation" là tên font được giữ bản quyền, bản cắt gọn được đổi tên thành *PNX Serif*.
