# BTL CSDL - Bookstore / Library Project

SQL (DDL, constraints, **stored procedures**, triggers, functions) và Flask backend nhẹ kèm frontend tĩnh cho đồ án.

**README — bản cập nhật workflow frontend/backend:** CRUD sản phẩm đi qua **stored procedure**; Admin có **tìm kiếm sách** và **thống kê bán hàng** gọi thủ tục chỉ đọc (phần 2.3).

---

## Layout (file quan trọng)

- `sql/` — schema và routine (`01_create_tables.sql` … `07_init_users.sql`; thủ tục BTL trong `04_procedures.sql`)
- `python/` — backend và HTML tĩnh
- `tools/extract_docx.py` — trích DOCX → text
- `requirements.txt`

File liên quan trực tiếp:

- [python/setup_db.py](python/setup_db.py) — chạy toàn bộ SQL (routine tách block `END;`)
- [python/init_users.py](python/init_users.py) — seed user demo (thường đã chạy trong `setup_db` qua `07_init_users.sql`)
- [python/auth_app.py](python/auth_app.py) — API Flask + `CALL` procedure
- [python/db.py](python/db.py) — kết nối MySQL (đọc `.env` từ **thư mục gốc repo**; Windows nên `MYSQL_HOST=127.0.0.1` để tránh named pipe)
- [python/login.html](python/login.html), [python/admin.html](python/admin.html), [python/customer.html](python/customer.html)

---

## Thủ tục (Procedure) — phần BTL 2.1 & 2.3 (`sql/04_procedures.sql`)

### Phần 2.1 — Một bảng `VatPham`: INSERT, UPDATE, DELETE + validate

| Thủ tục | Mục đích |
|---------|-----------|
| `sp_btl21_vat_pham_insert` | Thêm vật phẩm: kiểm tra tên không rỗng / độ dài, giá > 0, tồn ≥ 0, không trùng `TenVatPham`; trả `IDVatPham` qua `SELECT LAST_INSERT_ID()` |
| `sp_btl21_vat_pham_update` | Cập nhật theo ID: cùng rule; không trùng tên với bản ghi khác |
| `sp_btl21_vat_pham_delete` | Xóa chỉ khi **không** còn dòng trong `DonHangChiTiet`; lỗi dùng `SIGNAL` cụ thể (ví dụ đã có trong đơn hàng) |

Lỗi nghiệp vụ dùng `SIGNAL SQLSTATE '45000'` với `MESSAGE_TEXT` tiếng Việt có nghĩa (không chung chung).

### Phần 2.3 — Chỉ `SELECT`, tham số cho WHERE / HAVING

| Thủ tục | Mục đích |
|---------|-----------|
| `sp_btl23_tim_sach` | `VatPham` **JOIN** `Sach`: lọc từ khóa (tên hoặc tác giả), năm XB min/max, giá min/max; **ORDER BY** giá, tên |
| `sp_btl23_thong_ke_ban_vat_pham` | Join `VatPham`, `DonHangChiTiet`, `DonMuaHang`; **WHERE** khoảng `NgayMua`; **GROUP BY** vật phẩm; **HAVING** tổng doanh ≥ tham số; **ORDER BY** doanh giảm dần |

**Ví dụ gọi trong MySQL / báo cáo:**

```sql
CALL sp_btl23_tim_sach(NULL, NULL, NULL, NULL, NULL);
CALL sp_btl23_tim_sach('Sách', 2020, 2026, 50000, 500000);
CALL sp_btl23_thong_ke_ban_vat_pham('2025-01-01', '2025-12-31', 100000);
```

**Lưu ý deploy SQL:** `setup_db.py` khi chạy file routine **bỏ qua** khối có `strip()` bắt đầu bằng `--`; các thủ tục BTL được đặt sao cho khối thực thi không chỉ là comment.

---

## Prerequisites

- Python 3.8+
- MySQL 5.7+ (hoặc tương thích)

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # PowerShell Windows
python -m pip install -r requirements.txt
python -m pip install python-docx
```

```sql
CREATE DATABASE IF NOT EXISTS btl2_db;
```

`.env` ở **gốc repo** (đã có trong `.gitignore`, không commit mật khẩu):

```env
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=btl2_db
MYSQL_USER=root
MYSQL_PASSWORD=your_password
```

có thể dùng các lệnh sau để khởi chạy và tắt mysql thủ công (trên Administator Powershell):

net start MySQL80

net stop MySQL80

---

## Database setup

```bash
python python/setup_db.py
```

(`setup_db` có thể đã chạy `07_init_users.sql`; chỉ cần `python python/init_users.py` nếu bạn muốn chạy riêng.)

---

## Chạy backend

```bash
python python/auth_app.py
```

Mặc định: `http://127.0.0.1:5000`

### API — luồng frontend/backend

**Auth / khách**

- `POST /api/auth/login` — đăng nhập (JWT)
- `GET/PATCH /api/customers/me` — profile khách (customer)
- `POST /api/orders` — tạo đơn (customer)

**Sản phẩm (`VatPham`)**

- `GET /api/products` — danh sách
- `GET /api/products/<id>` — một dòng
- `POST /api/products` — **Admin**, gọi `sp_btl21_vat_pham_insert`
- `PUT /api/products/<id>` — **Admin**, gọi `sp_btl21_vat_pham_update` (kể cả tăng tồn từ Admin UI)
- `DELETE /api/products/<id>` — **Admin**, gọi `sp_btl21_vat_pham_delete`
- `GET /api/products/search-books?tu_khoa=&nam_xb_min=&nam_xb_max=&gia_min=&gia_max=` — `sp_btl23_tim_sach` (đã đăng nhập)
- `GET /api/products/stats-sales?tu_ngay=&den_ngay=&doanh_toi_thieu=` — `sp_btl23_thong_ke_ban_vat_pham`

Phản hồi lỗi từ procedure (SIGNAL) trả HTTP **400** và JSON `{ "error": "..." }`.

---

## Frontend (static)

Mở file HTML trong `python/` (hoặc phục vụ tĩnh):

- **login.html** — đăng nhập, nút demo
- **admin.html** — nhân viên, khách, **Products** (form thêm, tăng tồn, xóa), **tìm sách** & **thống kê bán** (gọi hai GET trên), mượn/thuê
- **customer.html** — profile (Edit/Save), giỏ, checkout

---

## Trích DOCX (mô tả BTL)

```bash
python tools/extract_docx.py "Mô tả BTL2-2.docx" docs/btl2.txt
```

---

## Kiểm tra nhanh

1. `python python/setup_db.py`, bật MySQL
2. `python python/auth_app.py`
3. Đăng nhập **admin** qua `login.html` → `admin.html` → tab Products: thêm sản phẩm, tìm sách, thống kê
4. Khách: `customer.html` — sửa profile, đặt hàng

Ví dụ tạo sản phẩm (Bearer Admin):

```bash
curl -X POST http://localhost:5000/api/products \
  -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d "{\"TenVatPham\":\"New Book\",\"SoLuongKhaDung\":10,\"GiaNiemYet\":120000}"
```

---

## Troubleshooting

- `mysql.connector` thiếu: `pip install mysql-connector-python`
- Không kết nối DB: kiểm tra `.env`, dịch vụ MySQL, database tồn tại
- Windows lỗi named pipe / `host: .`: dùng `MYSQL_HOST=127.0.0.1` (đã xử lý thêm trong `db.py`)
- Lỗi khi `setup_db.py` với routine: xem file SQL được in trong log

---

**Made for BTL CSDL** — README cập nhật: thủ tục 2.1/2.3, endpoint gọi `CALL`, workflow Admin tìm kiếm / thống kê.
