#!/usr/bin/env python3
"""
QUICK START GUIDE - Copy & Paste Commands
Run these commands in order to get the system up and running
"""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║         📚 LIBRARY MANAGEMENT SYSTEM - QUICK START GUIDE 📚                ║
╚════════════════════════════════════════════════════════════════════════════╝

🚀 STEP 1: Install Dependencies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cd C:\\Users\\Admin\\Desktop\\db2\\bookstore
pip install -r requirements.txt

✅ Expected: Successfully installed mysql-connector-python, Flask, PyJWT, etc.


🔧 STEP 2: Configure Environment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
copy .env.example .env
# Edit .env and update:
# - DB_USER (your MySQL username)
# - DB_PASSWORD (your MySQL password)
# - JWT_SECRET_KEY (change to something secure)

✅ Expected: .env file exists with your credentials


🗄️  STEP 3: Setup Database
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
mysql -u root -p < sql\\01_create_tables.sql
mysql -u root -p < sql\\02_constraints.sql
mysql -u root -p < sql\\03_sample_data.sql
mysql -u root -p < sql\\04_procedures.sql
mysql -u root -p < sql\\05_triggers.sql
mysql -u root -p < sql\\06_functions.sql

✅ Expected: All tables created without errors


👥 STEP 4: Initialize Demo Users
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cd python
python init_users.py

✅ Expected: "✨ Users created successfully!" message


🚀 STEP 5: Start Backend API (Terminal 1)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cd python
python auth_app.py

✅ Expected: "Running on http://127.0.0.1:5000" message
   Keep this terminal open!


🌐 STEP 6: Start Frontend Server (Terminal 2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
cd python
python -m http.server 8000

✅ Expected: "Serving HTTP on 0.0.0.0 port 8000" message
   Keep this terminal open!


🔐 STEP 7: Open Browser & Login
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Visit: http://localhost:8000/login.html

Demo Credentials (click the role buttons):
  👨‍💼 Admin:    admin / admin123
  💼 Cashier:   cashier / cashier123
  👥 Customer:  customer / customer123


📊 What You Can Do
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💼 ADMIN DASHBOARD
   ✅ Manage Employees (Create, Read, Delete)
   ✅ Manage Customers (Create, Read, Delete)
   ✅ Manage Products (Create, Read, Delete)
   ✅ View All Borrowing Records
   ✅ View All Rental Records
   ✅ See Full System Statistics

💼 CASHIER DASHBOARD
   ✅ Create & Manage Customers
   ✅ View Products (Read-Only)
   ✅ View All Borrowing Records
   ✅ View All Rental Records
   ❌ Cannot delete or modify anything

👥 CUSTOMER PORTAL
   ✅ View Own Profile
   ✅ View Own Borrowing History
   ✅ View Own Rental History
   ✅ Browse Product Catalog
   ❌ Cannot access admin features


🆔 Auto-Generated IDs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
When you create records, IDs are auto-generated:
  • NV001, NV002, NV003...  (Employees - Nhân Viên)
  • KH001, KH002, KH003...  (Customers - Khách Hàng)
  • 1, 2, 3...               (Products - Vật Phẩm)
  • MUO001, MUO002...        (Borrowing - Mượn)
  • THU001, THU002...        (Rental - Thuê)


🔍 Files You Should Know About
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 SETUP_GUIDE.md              Full detailed setup & architecture
📄 COMPLETION_SUMMARY.md       What's been completed
📄 auth_app.py                 Backend API (do NOT edit unless you know Python)
🌐 login.html                  Login page for all roles
🎨 admin.html                  Admin dashboard
🎨 cashier.html                Staff/Cashier dashboard
🎨 customer.html               Customer self-service portal
⚙️  .env                       Your configuration (KEEP SECURE!)
⚙️  requirements.txt            Python dependencies


🐛 Troubleshooting
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ "Cannot find module PyJWT"
   Run: pip install PyJWT>=2.8.0

❌ "Connection refused on localhost:5000"
   Make sure auth_app.py is running in Terminal 1

❌ "404 Not Found on http://localhost:8000"
   Make sure HTTP server is running in Terminal 2 and you're in the python/ folder

❌ "Database connection error"
   Check .env file has correct DB_USER and DB_PASSWORD

❌ "Token expired" errors
   Tokens expire after 24 hours. Just login again.

❌ "Redirect to login after every click"
   Check browser localStorage has the token. Try clearing cache.


✨ Pro Tips
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Keep auth_app.py running in the background
• Change JWT_SECRET_KEY in .env for production
• Don't share .env file (it has your database password!)
• Use Ctrl+Shift+Delete to clear browser cache if issues persist
• Each role only sees data they're allowed to see


🆘 Need Help?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Read SETUP_GUIDE.md for detailed explanations
2. Check COMPLETION_SUMMARY.md for feature list
3. Review API endpoints in SETUP_GUIDE.md
4. Check browser console (F12) for error messages


🎉 Ready to Go!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your system is now fully set up with:
  ✅ Role-based access control (Admin, Cashier, Customer)
  ✅ JWT authentication
  ✅ 3 separate dashboards
  ✅ Auto-generated IDs
  ✅ Demo accounts for testing

Happy managing! 📚

═══════════════════════════════════════════════════════════════════════════════
""")
