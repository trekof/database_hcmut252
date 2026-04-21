# 🚀 Frontend & Backend Setup Guide

## 📋 Before Starting

Make sure your database is set up:
```powershell
cd c:\Users\Admin\Desktop\db2\python
python setup_db.py
```

---

## 1️⃣ Install Dependencies

```powershell
cd c:\Users\Admin\Desktop\db2
pip install -r requirements.txt
```

This installs:
- `Flask` - Backend API framework
- `Flask-CORS` - Enable cross-origin requests
- `mysql-connector-python` - MySQL connection
- `python-dotenv` - Environment variables

---

## 2️⃣ Start the Backend Server

```powershell
cd c:\Users\Admin\Desktop\db2\python
python app.py
```

**Expected output:**
```
🚀 Starting Flask API server...
📍 http://localhost:5000
📊 Open http://localhost:5000/index.html
```

The backend runs on: **http://localhost:5000**

---

## 3️⃣ Open the Frontend

Two ways:

### Option A: Direct URL
Open your browser and go to:
```
http://localhost:5000/index.html
```

### Option B: Find the file locally
Navigate to: `c:\Users\Admin\Desktop\db2\python\index.html`
And drag it to your browser.

---

## 📊 What You Can Do

### Dashboard Features:
✅ **View Statistics** - Total employees, customers, orders, products  
✅ **Employees Tab** - Add, view, delete employees  
✅ **Customers Tab** - Add, view, delete customers  
✅ **Real-time Updates** - Data refreshes automatically  
✅ **Beautiful UI** - Modern gradient design  

### Forms:
- **Add Employee** - Enter ID, name, phone, job title, etc.
- **Add Customer** - Enter ID, phone, loyalty points, etc.

### Actions:
- **Delete** - Remove records with confirmation
- **View** - See all records in real-time

---

## 🔌 API Endpoints

The backend provides these endpoints:

### Employees
- `GET /api/employees` - Get all employees
- `GET /api/employees/<id>` - Get single employee
- `POST /api/employees` - Create employee
- `PUT /api/employees/<id>` - Update employee
- `DELETE /api/employees/<id>` - Delete employee

### Customers
- `GET /api/customers` - Get all customers
- `GET /api/customers/<id>` - Get single customer
- `POST /api/customers` - Create customer
- `PUT /api/customers/<id>` - Update customer
- `DELETE /api/customers/<id>` - Delete customer

### Statistics
- `GET /api/stats` - Get overview stats
- `GET /api/health` - Health check

---

## 🐛 Troubleshooting

### Error: "Connection refused"
```
Error: Cannot connect to localhost:5000
```
**Fix:** Make sure backend is running:
```powershell
cd c:\Users\Admin\Desktop\db2\python
python app.py
```

### Error: "Module not found: flask"
```
ModuleNotFoundError: No module named 'flask'
```
**Fix:** Install dependencies:
```powershell
pip install -r requirements.txt
```

### Error: "CORS error"
```
Access to XMLHttpRequest blocked by CORS policy
```
**Fix:** This is normal during development. The backend has CORS enabled.

### Database connection error
```
Can't connect to MySQL server
```
**Fix:** Check `.env` credentials and make sure MySQL is running.

---

## 📁 File Structure

```
db2/
├── python/
│   ├── app.py                # Backend Flask API
│   ├── index.html            # Frontend Dashboard
│   ├── setup_db.py           # Database setup
│   ├── demo_crud.py          # CRUD demo
│   ├── demo_query.py         # Query demo
│   └── db.py                 # Database connection
├── sql/                      # SQL files
├── requirements.txt          # Dependencies
├── .env                      # Configuration
└── README.md                 # Documentation
```

---

## 🎯 Quick Start (One Command)

Start everything at once:

```powershell
# Terminal 1 - Setup database
cd c:\Users\Admin\Desktop\db2\python
python setup_db.py

# Terminal 2 - Start backend
cd c:\Users\Admin\Desktop\db2\python
python app.py

# Then open browser
# http://localhost:5000/index.html
```

---

## 💡 Tips

1. **Keep backend running** - Leave the `python app.py` terminal open while using the dashboard

2. **Reload browser** - If data doesn't update, press F5

3. **Check console** - Press F12 in browser to see any errors

4. **Test with cURL**:
```powershell
# Get all employees
curl http://localhost:5000/api/employees

# Get stats
curl http://localhost:5000/api/stats
```

---

## 🚀 Next Steps

✅ Add more tables (Products, Orders, etc.)  
✅ Implement edit functionality  
✅ Add authentication/login  
✅ Add data export (CSV, Excel)  
✅ Deploy to cloud (Heroku, Azure, AWS)  

---

**Enjoy your Dashboard! 📊**
