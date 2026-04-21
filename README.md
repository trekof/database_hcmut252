# BTL CSDL - Database Project

## 📁 Cấu trúc thư mục

```
BTL2/
├── sql/
│   ├── 01_create_tables.sql       # Tạo bảng
│   ├── 02_constraints.sql         # Ràng buộc + khóa ngoài
│   ├── 03_sample_data.sql         # Dữ liệu mẫu
│   ├── 04_procedures.sql          # PROCEDURE
│   ├── 05_triggers.sql            # TRIGGER
│   └── 06_functions.sql           # FUNCTION
│
├── python/
│   ├── db.py                       # Kết nối MySQL
│   ├── setup_db.py                 # Chạy SQL từ file
│   ├── demo_crud.py                # Demo INSERT/UPDATE/DELETE
│   └── demo_query.py               # Demo SELECT qua PROCEDURE
│
├── .env                            # Cấu hình (KHÔNG commit)
├── requirements.txt                # Dependencies
└── README.md                        # Hướng dẫn này
```

---

## 🚀 Hướng dẫn cài đặt

### 1️⃣ Clone/Download project

```bash
cd c:\Users\Admin\Desktop\db2
```

### 2️⃣ Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Cấu hình .env

Mở file `.env` và sửa thông tin MySQL của bạn:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=btl2_db
MYSQL_USER=root
MYSQL_PASSWORD=your_password
```

⚠️ **CHÚ Ý**: Tạo database trước trên MySQL:
```sql
CREATE DATABASE btl2_db;
```

### 4️⃣ Chạy SQL setup

```bash
cd python
python setup_db.py
```

✓ Nếu thấy:
```
✓ Executed ../sql/01_create_tables.sql
✓ Executed ../sql/02_constraints.sql
...
✓ Database setup completed!
```

→ Setup thành công! 🎉

---

## 📝 Cách sử dụng

### Demo CRUD (INSERT/UPDATE/DELETE)

```bash
cd python
python demo_crud.py
```

Output:
```
==== Demo: Gọi PROCEDURE INSERT ===
✓ Insert thành công
```

### Demo Query (SELECT)

```bash
cd python
python demo_query.py
```

Output:
```
=== Demo: Lấy danh sách toàn bộ nhân viên ===
📊 Kết quả:
  {'id': 1, 'name': 'Nguyễn Văn A', 'age': 28, ...}
  {'id': 2, 'name': 'Trần Thị B', 'age': 26, ...}
```

---

## 🎯 Ưu điểm của cấu trúc này

| Tiêu chí | Mô tả |
|---------|-------|
| **Sạch** | SQL riêng, Python riêng → dễ quản lý |
| **Chuyên nghiệp** | Dùng PROCEDURE → không SQL inline |
| **GV yêu thích** | Có thể chạy từ đầu đến cuối 1 lệnh |
| **Scalable** | Thêm PROCEDURE/TRIGGER mà không sửa code Python |
| **Reusable** | File SQL có thể import vào phần mềm khác |

---

## 📌 Lưu ý quan trọng

### ✔️ DO (Làm)

- ✓ Gọi PROCEDURE từ Python (như trong `demo_crud.py`)
- ✓ Viết SQL không có DELIMITER (file SQL)
- ✓ Sử dụng `.env` cho config
- ✓ Commit code nhưng KHÔNG commit `.env`

### ❌ DON'T (Không làm)

- ✗ Viết SQL inline trong Python (vd: `"INSERT INTO ..."`)
- ✗ Hardcode mật khẩu trong code
- ✗ Dùng `DELIMITER` trong file SQL khi chạy từ Python
- ✗ Commit `.env` file

---

## 🔧 Lỗi thường gặp

### Lỗi: "No module named 'mysql.connector'"

```bash
pip install mysql-connector-python
```

### Lỗi: "Can't connect to MySQL server"

- Kiểm tra MySQL đang chạy
- Kiểm tra thông tin trong `.env` (host, user, password)
- Kiểm tra database `btl2_db` tồn tại

### Lỗi: "Tuổi phải >= 18" (Procedure)

→ Đó là ràng buộc business logic, sửa lại `p_age` để >= 18

---

## 📚 Mở rộng

Để thêm **PROCEDURE/TRIGGER/FUNCTION** mới:

1. Tạo file SQL (vd: `07_advanced_procedures.sql`)
2. Chạy: `run_routine_file("../sql/07_advanced_procedures.sql")`
3. Gọi từ Python như bình thường

---

## 👨‍💻 Contact

Nếu có lỗi, kiểm tra:
- Python version >= 3.7
- MySQL >= 5.7
- mysql-connector-python được install đúng

---

**Made for BTL CSDL** ✨
