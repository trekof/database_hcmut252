# BTL CSDL - Bookstore / Library Project

This repository contains SQL (DDL, constraints, procedures, triggers, functions) and a lightweight Flask backend + static frontend used for the course project.

**Layout (important files)**

- sql/: schema and routines (01_create_tables.sql ... 07_init_users.sql)
- python/: backend and helper scripts (see below)
- tools/extract_docx.py: DOCX -> plain text extractor
- requirements.txt
- README.md (this file)

Relevant files:
- [python/setup_db.py](python/setup_db.py)
- [python/init_users.py](python/init_users.py)
- [python/auth_app.py](python/auth_app.py)
- [python/customer.html](python/customer.html)
- [python/admin.html](python/admin.html)
- [tools/extract_docx.py](tools/extract_docx.py)

**Quick summary:** run `setup_db.py` to execute the SQL files in `sql/`, seed demo users with `init_users.py`, run the Flask API with `auth_app.py`, and open the static HTML pages in `python/` for admin/cashier/customer views.

---

**Prerequisites**

- Python 3.8+
- MySQL 5.7+ (or compatible)
- Create a database in MySQL for the project (example: `btl2_db`)

Install Python dependencies:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1   # PowerShell on Windows
python -m pip install -r requirements.txt
python -m pip install python-docx
```

Create the database in MySQL (example):

```sql
CREATE DATABASE btl2_db;
```

Create a `.env` file in the repo root with your DB credentials (example):

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=btl2_db
MYSQL_USER=root
MYSQL_PASSWORD=your_password
```

---

**Database setup (run once or to reset)**

From the repository root:

```bash
python python/setup_db.py
python python/init_users.py
```

- `setup_db.py` runs the ordered SQL files under `sql/` and correctly handles routines (procedures/functions/triggers). Check output for any SQL errors.
- `init_users.py` inserts demo users (Admin/Cashier/Customer) using `sql/07_init_users.sql`.

---

**Run the backend API**

```bash
python python/auth_app.py
```

The API listens on http://localhost:5000 by default. Key endpoints used by the frontends:

- `POST /api/auth/login` — login (returns token and user info)
- `GET /api/customers/me` — get current customer profile
- `PATCH /api/customers/me` — update customer profile (customers only)
- `GET /api/products` — list products
- `POST /api/products` — create product (Admin only)
- `PUT /api/products/<id>` — update product (Admin only)
- `POST /api/orders` — create an order (Customer)

---

**Frontend (static pages)**

Files are under `python/` and are simple static HTML + JS that call the API:

- [python/login.html](python/login.html) — login page (demo buttons provided)
- [python/admin.html](python/admin.html) — Admin dashboard (add/update products, manage users)
- [python/customer.html](python/customer.html) — Customer view (view/edit profile, cart & checkout)

Open these files in a browser (or serve them via a static file server). Use the demo credentials seeded by `init_users.py`.

Admin behavior added:
- Per-product `Qty` input + `Add` button to increment stock (uses existing `PUT /api/products/<id>` endpoint). You can also add products using the Add Product form.

Customer behavior added:
- Profile is shown read-only with an `Edit Profile` button that enables fields. `Save` calls `PATCH /api/customers/me`.

---

**Extract DOCX (for BTL description)**

If you have `Mô tả BTL2-2.docx` or similar, extract plain text for review before adding to SQL/rules:

```bash
python tools/extract_docx.py "Mô tả BTL2-2.docx" docs/btl2.txt
```

The extractor uses `python-docx` and writes paragraphs/tables to the output text file.

---

**Basic manual tests**

1. Start backend: `python python/auth_app.py`
2. Login via `python/login.html` using demo accounts.
3. As Admin: open `python/admin.html` → Products tab → create product → use per-product Add to increase stock.
4. As Customer: open `python/customer.html` → Edit profile → Save → verify values persisted.

Optional: use `curl` or HTTP client to exercise endpoints. Example to create a product (Admin token required):

```bash
curl -X POST http://localhost:5000/api/products \
  -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '{"TenVatPham":"New Book","SoLuongKhaDung":10,"GiaNiemYet":120000}'
```

---

**Troubleshooting**

- "No module named mysql.connector": `pip install mysql-connector-python`
- DB connection issues: verify `.env`, MySQL running, database exists
- SQL errors during `setup_db.py`: inspect the failing SQL file (path printed in output) and check syntax/compatibility with your MySQL version.

---

If you want, I can:
- update this README with more examples and screenshots, or
- add a small smoke-test script that runs setup + a few API calls and reports results.

Made for BTL CSDL — updated README to reflect frontend/backend workflows.

**Made for BTL CSDL** ✨
