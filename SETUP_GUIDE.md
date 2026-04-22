# 🔐 Library Management System - Setup Guide

## Overview
This is a role-based library management system with three distinct user roles:
- **Admin** (💼): Full system control - manage employees, customers, products, borrowing & rental
- **Cashier/Staff** (NhanVienDungQuay): Transaction processing - manage customers, view inventory, process borrowing & rental
- **Customer** (KhachHang): Self-service portal - view profile, borrowing history, rental history, browse products

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment Variables
Copy the example file and configure:
```bash
cp .env.example .env
```

Edit `.env` and change:
```
JWT_SECRET_KEY=your-super-secret-key-change-this
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
```

### 3. Setup Database
```bash
mysql -u root -p < sql/01_create_tables.sql
mysql -u root -p < sql/02_constraints.sql
mysql -u root -p < sql/03_sample_data.sql
mysql -u root -p < sql/04_procedures.sql
mysql -u root -p < sql/05_triggers.sql
mysql -u root -p < sql/06_functions.sql
```

### 4. Start the Backend
```bash
cd python
python auth_app.py
```
The API will run on `http://localhost:5000`

### 5. Open in Browser
```
http://localhost:8000/login.html
```
(You'll need to serve the HTML files via a simple HTTP server)

---

## 🔑 Demo Accounts

### Pre-configured Login Credentials
The system comes with 3 demo accounts (all passwords are the login name + "123"):

| Role | Username | Password | Access |
|------|----------|----------|--------|
| Admin | admin | admin123 | Full system control |
| Cashier | cashier | cashier123 | Transaction processing |
| Customer | customer | customer123 | Self-service portal |

Click the role buttons on the login page to auto-fill these credentials.

---

## 📊 User Roles & Permissions

### 👨‍💼 Admin Role
**Dashboard**: `admin.html`  
**Permissions**:
- ✅ Create/Read/Delete Employees
- ✅ Create/Read/Delete Customers  
- ✅ Create/Read/Delete Products
- ✅ View All Borrowing Records
- ✅ View All Rental Records
- ✅ View System Statistics

**API Endpoints**:
- `POST/GET/DELETE /api/employees`
- `POST/GET/DELETE /api/customers`
- `POST/GET/DELETE /api/products`
- `GET /api/borrowing`
- `GET /api/rentals`
- `GET /api/stats`

---

### 👔 Cashier/Staff Role (NhanVienDungQuay)
**Dashboard**: `cashier.html`  
**Permissions**:
- ✅ Create/Read Customers
- ✅ Read Products (view only)
- ✅ View All Borrowing Records
- ✅ View All Rental Records
- ❌ Cannot manage employees
- ❌ Cannot delete customers
- ❌ Cannot modify products

**API Endpoints** (with role checking):
- `POST/GET /api/customers` (no delete)
- `GET /api/products`
- `GET /api/borrowing`
- `GET /api/rentals`
- `GET /api/stats`

---

### 👥 Customer Role (KhachHang)
**Dashboard**: `customer.html`  
**Permissions**:
- ✅ View Own Profile
- ✅ View Own Borrowing History
- ✅ View Own Rental History
- ✅ Browse Product Catalog
- ❌ Cannot view other customers
- ❌ Cannot manage anything

**API Endpoints** (with role checking):
- `GET /api/customers/me` (own profile only)
- `GET /api/borrowing` (filtered to own records)
- `GET /api/rentals` (filtered to own records)
- `GET /api/products` (public catalog)
- `GET /api/stats` (personal stats only)

---

## 🔧 Backend Architecture (auth_app.py)

### Authentication Flow
```
1. User logs in with username/password
2. Backend validates credentials against Users table
3. Generates JWT token with 24-hour expiry
4. Token contains: user_id, username, role, reference_id
5. Frontend stores token in localStorage
6. All API requests include Authorization: Bearer <token>
7. Backend verifies token and enforces role-based access
```

### Key Components

#### JWT Tokens
- **Expiry**: 24 hours
- **Secret Key**: From `.env` (JWT_SECRET_KEY)
- **Payload**:
  ```json
  {
    "user_id": 1,
    "username": "admin",
    "role": "Admin",
    "reference_id": "NV001",
    "exp": 1234567890
  }
  ```

#### Role-Based Decorators
```python
@require_auth  # Validates JWT token
@require_role('Admin', 'NhanVienDungQuay')  # Checks role
def protected_endpoint():
    pass
```

#### ID Generation
- **Format**: `{Prefix}{Number}` (e.g., NV001, KH001)
- **Prefix Examples**:
  - NV = Nhân Viên (Employee)
  - KH = Khách Hàng (Customer)
  - MUO = Mượn (Borrowing)
  - THU = Thuê (Rental)
  - BC = Bản Copy (Copy)
- **Auto-generated**: Backend extracts existing IDs, finds max number, increments

---

## 📁 File Structure

```
bookstore/
├── python/
│   ├── auth_app.py          # 🆕 Main Flask API with RBAC
│   ├── login.html           # 🆕 Authentication portal
│   ├── admin.html           # 🆕 Admin dashboard (5 tabs)
│   ├── cashier.html         # 🆕 Staff dashboard (4 tabs)
│   ├── customer.html        # 🆕 Customer portal (4 tabs)
│   ├── app.py               # Original app (deprecated)
│   ├── db.py                # Database utilities
│   └── index.html           # Original UI (deprecated)
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_constraints.sql
│   ├── 03_sample_data.sql
│   ├── 04_procedures.sql
│   ├── 05_triggers.sql
│   └── 06_functions.sql
│
├── requirements.txt         # 🆕 Updated with PyJWT
├── .env.example             # 🆕 Configuration template
├── .env                     # 🆕 Actual config (add to .gitignore!)
└── README.md
```

---

## 🎨 Frontend Architecture

### Authentication Flow (login.html)
```javascript
1. User enters credentials or clicks demo button
2. POST /api/auth/login with username/password
3. Backend returns: { token, user: {id, username, role, reference_id} }
4. Frontend stores token + user in localStorage
5. Auto-redirects based on role:
   - Admin → admin.html
   - NhanVienDungQuay → cashier.html
   - KhachHang → customer.html
```

### Protected Pages
All dashboards check:
```javascript
if (!token || currentUser.role !== 'ExpectedRole') {
    window.location.href = '/login.html';  // Redirect if not authorized
}
```

### API Calls with Auth
```javascript
const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};

const res = await fetch(`${API_URL}/endpoint`, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(data)
});
```

---

## 🔒 Security Considerations

### Current Implementation
- ✅ JWT token-based authentication (24-hour expiry)
- ✅ Password hashing with SHA256
- ✅ Role-based access control (RBAC)
- ✅ CORS enabled for localhost:8000
- ✅ Token stored in localStorage

### Production Recommendations
1. **Change JWT_SECRET_KEY**: Use a strong random key (min 32 chars)
2. **Use bcrypt**: Replace SHA256 with bcrypt for password hashing
3. **Enable HTTPS**: Use SSL/TLS in production
4. **Restrict CORS**: Only allow trusted origins
5. **Use httpOnly Cookies**: Instead of localStorage for token
6. **Add Rate Limiting**: Prevent brute-force attacks
7. **Implement Refresh Tokens**: For better UX without security loss
8. **Audit Logging**: Log all sensitive operations

---

## 🧪 Testing the System

### Test Admin Login
1. Go to login page
2. Click "👨‍💼 Admin" button
3. Should redirect to admin.html
4. Can see all 5 tabs and create entities

### Test Cashier Login
1. Go to login page
2. Click "💼 Cashier" button
3. Should redirect to cashier.html
4. Can only see 4 tabs (no employees)

### Test Customer Login
1. Go to login page
2. Click "👥 Customer" button
3. Should redirect to customer.html
4. Can only see personal data and catalog

### Test API Access Control
```bash
# Without token
curl http://localhost:5000/api/employees
# Result: 401 Unauthorized

# With admin token
curl -H "Authorization: Bearer <admin_token>" http://localhost:5000/api/employees
# Result: 200 OK - List of employees

# Customer trying to access admin endpoint
curl -H "Authorization: Bearer <customer_token>" http://localhost:5000/api/employees
# Result: 403 Forbidden - Not allowed
```

---

## 🐛 Troubleshooting

### Login page won't load
- Make sure auth_app.py is running: `python auth_app.py`
- Check CORS is enabled: Look for `@app.after_request` in auth_app.py
- Verify API_URL in login.html matches: `http://localhost:5000/api`

### "Cannot find module PyJWT"
```bash
pip install PyJWT>=2.8.0
```

### Database connection error
- Check MySQL is running
- Verify .env has correct DB credentials
- Try: `mysql -u root -p -e "SELECT 1"`

### JWT token expired errors
- Tokens expire after 24 hours
- User needs to login again
- Token refresh endpoint can be added for better UX

### Role-based redirect not working
- Check browser localStorage: `localStorage.getItem('user')`
- Verify role matches expected value (exact case-sensitive)
- Clear cache and try again

---

## 📞 API Endpoints Reference

### Authentication
```
POST   /api/auth/login          Login with credentials
POST   /api/auth/register       Create new user (admin only)
GET    /api/auth/verify         Verify token is valid
```

### Employees (Admin only)
```
GET    /api/employees            List all
POST   /api/employees            Create new
DELETE /api/employees/<id>       Delete by ID
```

### Customers (Admin/Staff view all, Customer see own)
```
GET    /api/customers            List all (Admin/Staff) or own (Customer)
POST   /api/customers            Create new
GET    /api/customers/me         Get own profile
DELETE /api/customers/<id>       Delete by ID (Admin only)
```

### Products (All roles can view, Admin can modify)
```
GET    /api/products             List all
POST   /api/products             Create new (Admin only)
DELETE /api/products/<id>        Delete (Admin only)
```

### Borrowing (Filtered by role)
```
GET    /api/borrowing            List all (Admin/Staff) or own (Customer)
```

### Rentals (Filtered by role)
```
GET    /api/rentals              List all (Admin/Staff) or own (Customer)
```

### Statistics (Filtered by role)
```
GET    /api/stats                Get stats (different data per role)
```

---

## 📝 Notes

- **Multiple dashboards**: Users access different UIs based on their role
- **No manual ID entry**: All IDs auto-generated by backend
- **Data filtering**: Customers see only their own data automatically
- **Real-time updates**: Tables refresh after create/delete operations
- **Search/Filter**: All tables support client-side search

---

## 🎯 Next Steps

1. ✅ Run `pip install -r requirements.txt`
2. ✅ Setup `.env` file
3. ✅ Start backend: `python auth_app.py`
4. ✅ Open login.html in browser
5. ✅ Login with demo credentials
6. ✅ Test role-based features

**Happy managing!** 📚
