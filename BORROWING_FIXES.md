# Sửa Lỗi Borrowing vs Rental - Chi Tiết Thay Đổi

## 🔴 Vấn Đề Gốc
- **Borrowing (Mượn)** bị lỗi 500 khi khách hàng/admin truy cập
- **Rental (Thuê)** chạy được bình thường
- Lý do: Database schema không khớp với backend query

## ✅ Các Sửa Lỗi Được Thực Hiện

### 1. **Sửa Database Schema (01_create_tables.sql)**
**Vấn đề:** Bảng `LanMuon` dùng tên cột `MaSoBanCopy` nhưng bảng `BanCopy` dùng `MaBanCopy`

**Sửa:**
```sql
-- TRƯỚC: MaSoBanCopy
CREATE TABLE IF NOT EXISTS LanMuon (
    IDVatPham INT,
    MaSoBanCopy VARCHAR(20),  -- ❌ Sai
    ...
    FOREIGN KEY (IDVatPham, MaSoBanCopy) REFERENCES BanCopy(IDVatPham, MaBanCopy)
);

-- SAU: MaBanCopy (thống nhất)
CREATE TABLE IF NOT EXISTS LanMuon (
    IDVatPham INT,
    MaBanCopy VARCHAR(20),     -- ✅ Đúng
    ...
    FOREIGN KEY (IDVatPham, MaBanCopy) REFERENCES BanCopy(IDVatPham, MaBanCopy)
);
```

### 2. **Sửa Backend Query - Get Borrowing (auth_app.py)**
**Vấn đề:** Query dùng `IDKhachHang` nhưng bảng `LanMuon` không có cột này

**Sửa - Trước:**
```python
if request.user['role'] == 'KhachHang':
    cur.execute("""
        SELECT l.*, vp.TenVatPham
        FROM LanMuon l
        JOIN VatPham vp ON l.IDVatPham = vp.IDVatPham
        WHERE l.IDKhachHang=%s  # ❌ Cột không tồn tại!
    """, (customer_id,))
```

**Sửa - Sau:**
```python
if request.user['role'] == 'KhachHang':
    customer_id = request.user['reference_id']
    # Bước 1: Tìm CCCD từ CaNhan
    cur.execute("SELECT CCCD_CMND FROM CaNhan WHERE IDKhachHang = %s", (customer_id,))
    ca_nhan = cur.fetchone()
    
    if not ca_nhan:
        borrowings = []
    else:
        cccd = ca_nhan['CCCD_CMND']
        # Bước 2: Query LanMuon bằng CCCD_CMND ✅
        cur.execute("""
            SELECT l.*, vp.TenVatPham
            FROM LanMuon l
            JOIN VatPham vp ON l.IDVatPham = vp.IDVatPham
            WHERE l.CCCD_CMND=%s
            ORDER BY l.NgayMuon DESC
        """, (cccd,))
        borrowings = cur.fetchall()
else:
    # Admin/Staff: JOIN through CaNhan để lấy thông tin khách hàng
    cur.execute("""
        SELECT l.*, vp.TenVatPham, cn.Ho, cn.Ten
        FROM LanMuon l
        JOIN VatPham vp ON l.IDVatPham = vp.IDVatPham
        JOIN CaNhan cn ON l.CCCD_CMND = cn.CCCD_CMND
        ORDER BY l.NgayMuon DESC
    """)
    borrowings = cur.fetchall()
```

### 3. **Sửa Backend Query - Stats (auth_app.py)**
**Vấn đề:** Tính số lần mượn dùng `IDKhachHang` không tồn tại

**Sửa - Sau:**
```python
elif request.user['role'] == 'KhachHang':
    customer_id = request.user['reference_id']
    
    # Lấy CCCD để query LanMuon
    cur.execute("SELECT CCCD_CMND FROM CaNhan WHERE IDKhachHang = %s", (customer_id,))
    ca_nhan = cur.fetchone()
    if ca_nhan:
        cccd = ca_nhan['CCCD_CMND']
        cur.execute("SELECT COUNT(*) as count FROM LanMuon WHERE CCCD_CMND=%s", (cccd,))
        stats['my_borrowing'] = cur.fetchone()['count']
    else:
        stats['my_borrowing'] = 0
    
    # Rental vẫn dùng IDKhachHang (cột này tồn tại trong LanThue)
    cur.execute("SELECT COUNT(*) as count FROM LanThue WHERE IDKhachHang=%s", (customer_id,))
    stats['my_rentals'] = cur.fetchone()['count']
```

### 4. **Thêm Hàm Convert Decimal/Date (auth_app.py)**
**Vấn đề:** Python trả về Decimal object từ DB, nhưng Flask's jsonify() không thể serialize được

**Sửa:**
```python
def convert_decimal_and_dates(rows):
    """Convert Decimal và Date objects thành strings/floats để JSON có thể serialize"""
    from decimal import Decimal
    if not rows:
        return rows
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict):
                for key, value in row.items():
                    if isinstance(value, Decimal):
                        row[key] = float(value)  # Decimal → float
                    elif isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
                        row[key] = str(value)    # Date → "YYYY-MM-DD"
                    elif isinstance(value, datetime.datetime):
                        row[key] = value.isoformat()  # DateTime → ISO format
    return rows
```

**Áp dụng trong get_borrowing():**
```python
borrowings = convert_decimal_and_dates(borrowings)
return jsonify(borrowings), 200
```

**Áp dụng trong get_rentals():**
```python
rentals = convert_decimal_and_dates(rentals)
return jsonify(rentals), 200
```

### 5. **Update Seed Data (03_sample_data.sql)**
**Vấn đề:** INSERT LanMuon dùng `MaSoBanCopy` nhưng schema đã sửa thành `MaBanCopy`

**Sửa - Sau:**
```sql
INSERT INTO LanMuon (IDVatPham, MaBanCopy, CCCD_CMND, MaThe, MaDonMuon, TinhTrangSauKhiTra, NgayMuon, HanTra) VALUES
(1, 'BC001', '001111111111', 1, 'MUO001', 'Tốt', '2024-02-20', '2024-03-20'),
(4, 'BC004', '002222222222', 2, 'MUO002', 'Tốt', '2024-02-22', '2024-03-22'),
(2, 'BC003', '003333333333', 3, 'MUO003', 'Tốt', '2024-02-25', '2024-03-25');
```

## 📋 Tóm Tắt Cấu Trúc Dữ Liệu Borrowing

```
Khách Hàng → CaNhan → TheThanhVien → LanMuon
KhachHang.IDKhachHang
    ↓
CaNhan.CCCD_CMND (link via IDKhachHang)
    ↓
TheThanhVien (CCCD_CMND, MaThe)
    ↓
LanMuon (CCCD_CMND, MaThe) + BanCopy.MaBanCopy
```

**So sánh với Rental:**
```
Khách Hàng → LanThue
KhachHang.IDKhachHang
    ↓
LanThue.IDKhachHang (direct link)
```

## 🧪 Cách Test

1. **Chạy setup lại:**
```bash
cd python
python setup_db.py
```

2. **Chạy backend:**
```bash
python auth_app.py
```

3. **Đăng nhập và test:**
- Customer: đăng nhập & xem "My Borrowing"
- Admin: đăng nhập & xem toàn bộ borrowing
- Check stats: số lần mượn của customer

4. **Expected Result:**
- ✅ Không có lỗi 500
- ✅ Hiển thị danh sách mượn đúng
- ✅ Stats hiển thị số mượn chính xác
- ✅ Các giá tiền hiển thị dạng số (float), không phải Decimal object

## 📝 Files Được Sửa

1. ✅ `sql/01_create_tables.sql` - Thay `MaSoBanCopy` → `MaBanCopy` trong LanMuon
2. ✅ `sql/03_sample_data.sql` - Cập nhật INSERT LanMuon dùng `MaBanCopy`
3. ✅ `python/auth_app.py` - Sửa query borrowing, stats, thêm convert_decimal_and_dates()
4. ✅ `sql/07_init_users.sql` - Đã tạo trước (hash password bằng SQL)

## 🎯 Kết Quả

Sau những sửa lỗi này, hệ thống sẽ:
- ✅ Borrowing (Mươn) hoạt động bình thường
- ✅ Rental (Thuê) tiếp tục hoạt động
- ✅ Admin & Staff xem được đầy đủ dữ liệu
- ✅ Customer xem được chỉ dữ liệu của mình
- ✅ Stats hiển thị đúng
- ✅ JSON response không lỗi Decimal serialization
