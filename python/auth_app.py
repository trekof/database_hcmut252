"""
Flask Backend with Role-Based Access Control (RBAC)
Supports 3 roles: Admin, NhanVienDungQuay (Cashier/Staff), KhachHang (Customer)
Uses JWT tokens for session management
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, date
import re
import jwt
import json
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
CORS(app)

# MySQL Configuration
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "database": os.getenv("MYSQL_DB"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "autocommit": False
}

def get_db_connection():
    """Get MySQL connection"""
    return mysql.connector.connect(**MYSQL_CONFIG)

# ==================== AUTH HELPERS ====================

def create_users_table():
    """Create Users table if it doesn't exist"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                IDUser INT AUTO_INCREMENT PRIMARY KEY,
                Username VARCHAR(50) UNIQUE NOT NULL,
                Password VARCHAR(255) NOT NULL,
                Role ENUM('Admin', 'NhanVienDungQuay', 'KhachHang') NOT NULL,
                ReferenceID VARCHAR(20),
                IsActive BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX (Username),
                INDEX (ReferenceID)
            )
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("Users table created successfully")
    except Exception as e:
        print(f"Error creating users table: {e}")

# Create users table on startup
create_users_table()

def generate_token(user_id, username, role, reference_id):
    """Generate JWT token"""
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'reference_id': reference_id,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Missing authorization token"}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Store payload in request for use in the route
        request.user = payload
        return f(*args, **kwargs)
    
    return decorated_function

def require_role(*roles):
    """Decorator to require specific roles"""
    def decorator(f):
        @wraps(f)
        @require_auth
        def decorated_function(*args, **kwargs):
            if request.user['role'] not in roles:
                return jsonify({"error": "Access denied for this role"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
def convert_decimal_and_dates(rows):
    """Convert Decimal and Date objects to strings/floats for JSON serialization"""
    from decimal import Decimal
    if not rows:
        return rows
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict):
                for key, value in row.items():
                    if isinstance(value, Decimal):
                        row[key] = float(value)
                    elif isinstance(value, date) and not isinstance(value, datetime):
                        row[key] = str(value)
                    elif isinstance(value, datetime):
                        row[key] = value.isoformat()
    elif isinstance(rows, dict):
        for key, value in rows.items():
            if isinstance(value, Decimal):
                rows[key] = float(value)
            elif isinstance(value, date) and not isinstance(value, datetime):
                rows[key] = str(value)
            elif isinstance(value, datetime):
                rows[key] = value.isoformat()
    return rows
# ==================== ID GENERATION HELPERS ====================

def generate_next_id(prefix, table_name, id_column):
    """Generate next sequential ID with prefix (e.g., NV001, KH002)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(f"SELECT {id_column} FROM {table_name} WHERE {id_column} LIKE %s", (f"{prefix}%",))
        result = cur.fetchall()
        cur.close()
        conn.close()
        
        max_num = 0
        for row in result:
            id_val = row[0]
            match = re.search(r'\d+', id_val)
            if match:
                num = int(match.group())
                max_num = max(max_num, num)
        
        next_num = max_num + 1
        return f"{prefix}{next_num:03d}"
    except Exception as e:
        print(f"Error generating ID: {e}")
        return None

# ==================== STATIC FILES ====================

@app.route('/')
def serve_root():
    """Serve login page"""
    return send_from_directory('.', 'login.html')

@app.route('/login.html')
def serve_login():
    return send_from_directory('.', 'login.html')

@app.route('/admin.html')
def serve_admin():
    return send_from_directory('.', 'admin.html')

@app.route('/cashier.html')
def serve_cashier():
    return send_from_directory('.', 'cashier.html')

@app.route('/customer.html')
def serve_customer():
    return send_from_directory('.', 'customer.html')

@app.route('/index.html')
def serve_index():
    return send_from_directory('.', 'admin.html')  # Default to admin

# ==================== AUTHENTICATION ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user (Admin only)"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT * FROM Users WHERE Username=%s", (data['username'],))
        if cur.fetchone():
            return jsonify({"error": "User already exists"}), 400
        
        # Hash password (in production, use proper bcrypt)
        import hashlib
        hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
        
        # Insert user
        query = """
            INSERT INTO Users (Username, Password, Role, ReferenceID)
            VALUES (%s, %s, %s, %s)
        """
        
        cur.execute(query, (
            data['username'],
            hashed_password,
            data.get('role', 'KhachHang'),
            data.get('reference_id')
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        
        # Get user
        cur.execute("SELECT * FROM Users WHERE Username=%s AND IsActive=TRUE", (data['username'],))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Verify password
        import hashlib
        hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
        
        if user['Password'] != hashed_password:
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Generate token
        token = generate_token(user['IDUser'], user['Username'], user['Role'], user['ReferenceID'])
        
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user['IDUser'],
                "username": user['Username'],
                "role": user['Role'],
                "reference_id": user['ReferenceID']
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user (currently just client-side token removal)"""
    return jsonify({"message": "Logout successful"}), 200

@app.route('/api/auth/me', methods=['GET'])
@require_auth
def get_current_user():
    """Get current user info"""
    return jsonify(request.user), 200

@app.route('/api/auth/verify', methods=['GET'])
def verify_auth():
    """Verify if token is valid"""
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token[7:]
        payload = verify_token(token)
        if payload:
            return jsonify({"valid": True, "user": payload}), 200
    return jsonify({"valid": False}), 401

# ==================== EMPLOYEES (Admin & Staff Only) ====================

@app.route('/api/employees', methods=['GET'])
@require_role('Admin', 'NhanVienDungQuay')
def get_employees():
    """Get all employees (Admin & Staff only)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM NhanVien ORDER BY IDNhanVien")
        employees = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/employees', methods=['POST'])
@require_role('Admin')
def create_employee():
    """Create new employee (Admin only)"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        emp_id = generate_next_id('NV', 'NhanVien', 'IDNhanVien')
        if not emp_id:
            return jsonify({"error": "Failed to generate employee ID"}), 500
        
        query = """
            INSERT INTO NhanVien 
            (IDNhanVien, CMND_CCCD, Ho, Ten, NgaySinh, SDT, CongViec, BoPhanQuanLy)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cur.execute(query, (
            emp_id,
            data['CMND_CCCD'],
            data.get('Ho'),
            data.get('Ten'),
            data.get('NgaySinh'),
            data.get('SDT'),
            data.get('CongViec'),
            data.get('BoPhanQuanLy')
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "message": "Employee created successfully",
            "IDNhanVien": emp_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/employees/<id>', methods=['DELETE'])
@require_role('Admin')
def delete_employee(id):
    """Delete employee (Admin only)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM NhanVien WHERE IDNhanVien=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Employee deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== CUSTOMERS ====================

@app.route('/api/customers', methods=['GET'])
@require_role('Admin', 'NhanVienDungQuay')
def get_customers():
    """Get all customers (Admin & Staff)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM KhachHang ORDER BY IDKhachHang")
        customers = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(customers), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/customers/me', methods=['GET'])
@require_role('KhachHang')
def get_my_profile():
    """Get own customer profile"""
    try:
        customer_id = request.user['reference_id']
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM KhachHang WHERE IDKhachHang=%s", (customer_id,))
        customer = cur.fetchone()
        cur.close()
        conn.close()
        
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify(customer), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/customers/<id>', methods=['GET'])
@require_role('Admin', 'NhanVienDungQuay')
def get_customer(id):
    """Get single customer (Admin & Staff)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM KhachHang WHERE IDKhachHang = %s", (id,))
        customer = cur.fetchone()
        cur.close()
        conn.close()
        
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify(customer), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/customers', methods=['POST'])
@require_role('Admin', 'NhanVienDungQuay')
def create_customer():
    """Create new customer (Admin & Staff)"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        customer_id = generate_next_id('KH', 'KhachHang', 'IDKhachHang')
        if not customer_id:
            return jsonify({"error": "Failed to generate customer ID"}), 500
        
        query = """
            INSERT INTO KhachHang 
            (IDKhachHang, SDT, DiemTichLuy)
            VALUES (%s, %s, %s)
        """
        
        cur.execute(query, (
            customer_id,
            data.get('SDT'),
            data.get('DiemTichLuy', 0)
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "message": "Customer created successfully",
            "IDKhachHang": customer_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/customers/<id>', methods=['DELETE'])
@require_role('Admin')
def delete_customer(id):
    """Delete customer (Admin only)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM KhachHang WHERE IDKhachHang=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Customer deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== PRODUCTS ====================

@app.route('/api/products', methods=['GET'])
@require_auth
def get_products():
    """Get all products (all authenticated users)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM VatPham ORDER BY IDVatPham")
        products = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:id>', methods=['GET'])
@require_auth
def get_product(id):
    """Get single product (all authenticated users)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM VatPham WHERE IDVatPham = %s", (id,))
        product = cur.fetchone()
        cur.close()
        conn.close()
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['POST'])
@require_role('Admin')
def create_product():
    """Create new product (Admin only)"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            INSERT INTO VatPham 
            (TenVatPham, SoLuongKhaDung, GiaNiemYet)
            VALUES (%s, %s, %s)
        """
        
        cur.execute(query, (
            data['TenVatPham'],
            data.get('SoLuongKhaDung', 0),
            data.get('GiaNiemYet', 0)
        ))
        
        product_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "message": "Product created successfully",
            "IDVatPham": product_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:id>', methods=['PUT'])
@require_role('Admin')
def update_product(id):
    """Update product (Admin only)"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            UPDATE VatPham 
            SET TenVatPham=%s, SoLuongKhaDung=%s, GiaNiemYet=%s
            WHERE IDVatPham=%s
        """
        
        cur.execute(query, (
            data.get('TenVatPham'),
            data.get('SoLuongKhaDung'),
            data.get('GiaNiemYet'),
            id
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:id>', methods=['DELETE'])
@require_role('Admin')
def delete_product(id):
    """Delete product (Admin only)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("DELETE FROM VatPham WHERE IDVatPham=%s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== BORROWING (RENTAL for customers/staff) ====================

@app.route('/api/borrowing', methods=['GET'])
@require_auth
def get_borrowing():
    """Get borrowing records (filtered by role)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        
        if request.user['role'] == 'KhachHang':
            # Customer sees only their own borrowing
            # 1. Find customer's CCCD from CaNhan table
            customer_id = request.user['reference_id']
            cur.execute("SELECT CCCD_CMND FROM CaNhan WHERE IDKhachHang = %s", (customer_id,))
            ca_nhan = cur.fetchone()
            
            if not ca_nhan:
                borrowings = []
            else:
                cccd = ca_nhan['CCCD_CMND']
                # 2. Query LanMuon using CCCD_CMND
                cur.execute("""
                    SELECT l.*, vp.TenVatPham
                    FROM LanMuon l
                    JOIN VatPham vp ON l.IDVatPham = vp.IDVatPham
                    WHERE l.CCCD_CMND=%s
                    ORDER BY l.NgayMuon DESC
                """, (cccd,))
                borrowings = cur.fetchall()
        else:
            # Admin/Staff see all - JOIN through CaNhan to get customer info
            cur.execute("""
                SELECT l.*, vp.TenVatPham, cn.Ho, cn.Ten
                FROM LanMuon l
                JOIN VatPham vp ON l.IDVatPham = vp.IDVatPham
                JOIN CaNhan cn ON l.CCCD_CMND = cn.CCCD_CMND
                ORDER BY l.NgayMuon DESC
            """)
            borrowings = cur.fetchall()
        
        borrowings = convert_decimal_and_dates(borrowings)
        cur.close()
        conn.close()
        return jsonify(borrowings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/rentals', methods=['GET'])
@require_auth
def get_rentals():
    """Get rental records (filtered by role)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        
        if request.user['role'] == 'KhachHang':
            # Customer sees only their own rentals
            customer_id = request.user['reference_id']
            cur.execute("""
                SELECT l.*, vp.TenVatPham
                FROM LanThue l
                JOIN VatPham vp ON l.IDVatPham = vp.IDVatPham
                WHERE l.IDKhachHang=%s
                ORDER BY l.NgayThue DESC
            """, (customer_id,))
        else:
            # Admin/Staff see all
            cur.execute("""
                SELECT l.*, vp.TenVatPham, kh.SDT
                FROM LanThue l
                JOIN VatPham vp ON l.IDVatPham = vp.IDVatPham
                JOIN KhachHang kh ON l.IDKhachHang = kh.IDKhachHang
                ORDER BY l.NgayThue DESC
            """)
        
        rentals = cur.fetchall()
        rentals = convert_decimal_and_dates(rentals)
        cur.close()
        conn.close()
        return jsonify(rentals), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== STATS ====================

@app.route('/api/stats', methods=['GET'])
@require_auth
def get_stats():
    """Get statistics (role-based)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        
        stats = {}
        
        if request.user['role'] in ['Admin', 'NhanVienDungQuay']:
            # Full stats for Admin and Staff
            cur.execute("SELECT COUNT(*) as count FROM NhanVien")
            stats['employees'] = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM KhachHang")
            stats['customers'] = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM VatPham")
            stats['products'] = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM DonMuaHang")
            stats['orders'] = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM LanMuon")
            stats['borrowing'] = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(*) as count FROM LanThue")
            stats['rentals'] = cur.fetchone()['count']
        
        elif request.user['role'] == 'KhachHang':
            # Customer sees their own stats
            customer_id = request.user['reference_id']
            
            # Get CCCD from CaNhan to query LanMuon
            cur.execute("SELECT CCCD_CMND FROM CaNhan WHERE IDKhachHang = %s", (customer_id,))
            ca_nhan = cur.fetchone()
            if ca_nhan:
                cccd = ca_nhan['CCCD_CMND']
                cur.execute("SELECT COUNT(*) as count FROM LanMuon WHERE CCCD_CMND=%s", (cccd,))
                stats['my_borrowing'] = cur.fetchone()['count']
            else:
                stats['my_borrowing'] = 0
            
            cur.execute("SELECT COUNT(*) as count FROM LanThue WHERE IDKhachHang=%s", (customer_id,))
            stats['my_rentals'] = cur.fetchone()['count']
        
        cur.close()
        conn.close()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
