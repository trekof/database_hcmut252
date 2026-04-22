#!/usr/bin/env python3
"""
Database User Initialization Script
Creates demo users for testing the role-based system
Run this after setting up the database schema
"""

import mysql.connector
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_USER = os.getenv('MYSQL_USER', 'root')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
DB_NAME = os.getenv('MYSQL_DB', 'btl2_db')

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_users():
    """Create demo users in the Users table"""
    
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cur = conn.cursor()
        
        print("📝 Creating demo users...")
        
        # First, ensure Users table exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                IDUser INT AUTO_INCREMENT PRIMARY KEY,
                Username VARCHAR(50) UNIQUE NOT NULL,
                Password VARCHAR(255) NOT NULL,
                Role ENUM('Admin', 'NhanVienDungQuay', 'KhachHang') NOT NULL,
                ReferenceID VARCHAR(20),
                IsActive BOOLEAN DEFAULT TRUE,
                CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # Clear existing demo users (optional)
        cur.execute("DELETE FROM Users WHERE Username IN ('admin', 'cashier', 'customer')")
        
        demo_users = [
            {
                'username': 'admin',
                'password': 'admin123',
                'role': 'Admin',
                'reference_id': 'NV001'  # Admin employee
            },
            {
                'username': 'cashier',
                'password': 'cashier123',
                'role': 'NhanVienDungQuay',
                'reference_id': 'NV002'  # Staff employee
            },
            {
                'username': 'customer',
                'password': 'customer123',
                'role': 'KhachHang',
                'reference_id': 'KH001'  # Customer
            }
        ]
        
        for user in demo_users:
            hashed_pwd = hash_password(user['password'])
            
            try:
                cur.execute("""
                    INSERT INTO Users (Username, Password, Role, ReferenceID, IsActive)
                    VALUES (%s, %s, %s, %s, TRUE)
                """, (
                    user['username'],
                    hashed_pwd,
                    user['role'],
                    user['reference_id']
                ))
                print(f"  ✅ Created {user['role']:20} | Username: {user['username']:10} | Pass: {user['password']}")
            except mysql.connector.Error as e:
                if "Duplicate entry" in str(e):
                    print(f"  ⚠️  {user['username']} already exists, skipping")
                else:
                    raise
        
        conn.commit()
        print("\n✨ Users created successfully!")
        print("\n📝 Demo Accounts:")
        print("┌─────────────────────────────────────────────────────┐")
        print("│ Role              │ Username  │ Password     │ Token │")
        print("├─────────────────────────────────────────────────────┤")
        print("│ Admin             │ admin     │ admin123     │ Bearer... │")
        print("│ Cashier/Staff     │ cashier   │ cashier123   │ Bearer... │")
        print("│ Customer          │ customer  │ customer123  │ Bearer... │")
        print("└─────────────────────────────────────────────────────┘")
        print("\n🔐 Security Note:")
        print("  - These are demo credentials only")
        print("  - Change them in production!")
        print("  - Passwords are hashed with SHA256")
        
        # Verify the employees/customers exist
        print("\n🔍 Verifying referenced entities...")
        
        cur.execute("SELECT COUNT(*) FROM NhanVien WHERE IDNhanVien IN ('NV001', 'NV002')")
        emp_count = cur.fetchone()[0]
        if emp_count < 2:
            print("  ⚠️  Warning: Only found {} employees (need 2: NV001, NV002)".format(emp_count))
            print("     Create employees first or update reference IDs in Users table")
        else:
            print("  ✅ Found required employees: NV001, NV002")
        
        cur.execute("SELECT COUNT(*) FROM KhachHang WHERE IDKhachHang = 'KH001'")
        cust_count = cur.fetchone()[0]
        if cust_count < 1:
            print("  ⚠️  Warning: Customer KH001 not found")
            print("     Create customer first or update reference IDs in Users table")
        else:
            print("  ✅ Found required customer: KH001")
        
        conn.close()
        
    except mysql.connector.Error as e:
        print(f"❌ Database Error: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

if __name__ == '__main__':
    print("🚀 Library Management System - User Initialization\n")
    print(f"Database: {DB_NAME} @ {DB_HOST}")
    create_users()
    print("\n✅ Setup complete! Start auth_app.py and login with demo credentials.")
