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

# Note: Users table and demo users are created via SQL files in /sql.
# The application no longer creates schema objects at runtime.

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


@app.route('/api/employees/<id>/dependents', methods=['GET'])
@require_role('Admin')
def get_employee_dependents(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM NguoiPhuThuoc WHERE IDNhanVien=%s", (id,))
        deps = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(deps), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/employees/<id>/dependents', methods=['POST'])
@require_role('Admin')
def add_employee_dependent(id):
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO NguoiPhuThuoc (IDNhanVien, CMND_CCCD, Quan_He, Ho, Ten) VALUES (%s,%s,%s,%s,%s)", (
            id,
            data['CMND_CCCD'],
            data.get('Quan_He'),
            data.get('Ho'),
            data.get('Ten')
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Dependent added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/employees/<id>/dependents/<cmnd>', methods=['DELETE'])
@require_role('Admin')
def delete_employee_dependent(id, cmnd):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM NguoiPhuThuoc WHERE IDNhanVien=%s AND CMND_CCCD=%s", (id, cmnd))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Dependent removed"}), 200
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
        # If an IDQuanLy (manager) is provided, fetch their CongViec to set BoPhanQuanLy
        bo_phan = data.get('BoPhanQuanLy')
        id_quan_ly = data.get('IDQuanLy')
        gioi_tinh = data.get('GioiTinh')
        ngay_sinh = data.get('NgaySinh')

        if id_quan_ly:
            cur.execute("SELECT CongViec FROM NhanVien WHERE IDNhanVien=%s", (id_quan_ly,))
            mgr = cur.fetchone()
            if mgr:
                bo_phan = mgr[0]

        query = """
            INSERT INTO NhanVien 
            (IDNhanVien, CMND_CCCD, Ho, Ten, NgaySinh, SDT, CongViec, GioiTinh, BoPhanQuanLy, IDQuanLy)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cur.execute(query, (
            emp_id,
            data['CMND_CCCD'],
            data.get('Ho'),
            data.get('Ten'),
            ngay_sinh,
            data.get('SDT'),
            data.get('CongViec'),
            gioi_tinh,
            bo_phan,
            id_quan_ly
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

@app.route('/api/employees/<emp_id>', methods=['PUT'])
@require_role('Admin')
def update_employee(emp_id):
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        fields = []
        params = []
        for key in ['CMND_CCCD', 'Ho', 'Ten', 'NgaySinh', 'SDT', 'CongViec', 'GioiTinh', 'BoPhanQuanLy', 'IDQuanLy']:
            if key in data:
                fields.append(f"{key}=%s")
                params.append(data[key])
        if not fields:
            return jsonify({"error": "No fields to update"}), 400
        params.append(emp_id)
        query = f"UPDATE NhanVien SET {', '.join(fields)} WHERE IDNhanVien=%s"
        cur.execute(query, tuple(params))
        conn.commit() # QUAN TRỌNG: Phải có dòng này thì DB mới thay đổi
        cur.close()
        conn.close()
        return jsonify({"message": "Updated successfully"}), 200
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
        cur.execute("SELECT k.*, c.CCCD_CMND, c.Ho, c.Ten, d.DiaChi, t.MaSoThue, t.TenCongTy FROM KhachHang k LEFT JOIN CaNhan c ON k.IDKhachHang=c.IDKhachHang LEFT JOIN DiaChiCaNhan d ON c.CCCD_CMND=d.CCCD_CMND LEFT JOIN TapTheCongTy t ON k.IDKhachHang=t.IDKhachHang ORDER BY k.IDKhachHang")
        rows = cur.fetchall()
        customers = []
        for r in rows:
            cust = dict(r)
            # determine type
            if r.get('CCCD_CMND'):
                cust['type'] = 'CaNhan'
                cust['Ho'] = r.get('Ho')
                cust['Ten'] = r.get('Ten')
                cust['CCCD_CMND'] = r.get('CCCD_CMND')
                cust['DiaChi'] = r.get('DiaChi')
            elif r.get('MaSoThue'):
                cust['type'] = 'TapTheCongTy'
                cust['MaSoThue'] = r.get('MaSoThue')
                cust['TenCongTy'] = r.get('TenCongTy')
            else:
                cust['type'] = 'Unknown'

            # Mask SDT for staff role
            if request.user['role'] == 'NhanVienDungQuay' and cust.get('SDT'):
                s = cust.get('SDT')
                if len(s) > 3:
                    cust['SDT'] = '*' * (len(s) - 3) + s[-3:]

            customers.append(cust)
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
        cur.execute("SELECT k.*, c.CCCD_CMND, c.Ho, c.Ten, d.DiaChi FROM KhachHang k LEFT JOIN CaNhan c ON k.IDKhachHang=c.IDKhachHang LEFT JOIN DiaChiCaNhan d ON c.CCCD_CMND=d.CCCD_CMND WHERE k.IDKhachHang=%s", (customer_id,))
        customer = cur.fetchone()
        cur.close()
        conn.close()
        
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        # annotate type
        if customer.get('CCCD_CMND'):
            customer['type'] = 'CaNhan'
        else:
            # check for company
            # need separate connection to check TapTheCongTy
            conn2 = get_db_connection()
            cur2 = conn2.cursor()
            cur2.execute("SELECT MaSoThue, TenCongTy FROM TapTheCongTy WHERE IDKhachHang=%s", (customer_id,))
            t = cur2.fetchone()
            cur2.close(); conn2.close()
            if t:
                customer['type'] = 'TapTheCongTy'
                customer['MaSoThue'] = t[0]
                customer['TenCongTy'] = t[1]
            else:
                customer['type'] = 'Unknown'

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
        cur.execute("SELECT k.*, c.CCCD_CMND, c.Ho, c.Ten, d.DiaChi, t.MaSoThue, t.TenCongTy FROM KhachHang k LEFT JOIN CaNhan c ON k.IDKhachHang=c.IDKhachHang LEFT JOIN DiaChiCaNhan d ON c.CCCD_CMND=d.CCCD_CMND LEFT JOIN TapTheCongTy t ON k.IDKhachHang=t.IDKhachHang WHERE k.IDKhachHang = %s", (id,))
        customer = cur.fetchone()
        cur.close()
        conn.close()
        
        if not customer:
            return jsonify({"error": "Customer not found"}), 404
        cust = dict(customer)
        if customer.get('CCCD_CMND'):
            cust['type'] = 'CaNhan'
        elif customer.get('MaSoThue'):
            cust['type'] = 'TapTheCongTy'
        else:
            cust['type'] = 'Unknown'

        # Mask SDT for staff role
        if request.user['role'] == 'NhanVienDungQuay' and cust.get('SDT'):
            s = cust.get('SDT')
            if len(s) > 3:
                cust['SDT'] = '*' * (len(s) - 3) + s[-3:]

        return jsonify(cust), 200
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

        # If personal info provided, insert into CaNhan and DiaChiCaNhan
        cccd = data.get('CCCD_CMND') or data.get('CCCD')
        ho = data.get('Ho')
        ten = data.get('Ten')
        diachi = data.get('DiaChi') or data.get('DiaChiCaNhan')

        if cccd and (ho or ten):
            try:
                cur.execute("""
                    INSERT INTO CaNhan (CCCD_CMND, IDKhachHang, Ho, Ten)
                    VALUES (%s, %s, %s, %s)
                """, (cccd, customer_id, ho, ten))
            except Exception:
                # ignore duplicates or issues here; caller can re-run updates
                pass

        if cccd and diachi:
            try:
                cur.execute("""
                    INSERT INTO DiaChiCaNhan (CCCD_CMND, DiaChi)
                    VALUES (%s, %s)
                """, (cccd, diachi))
            except Exception:
                pass
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "message": "Customer created successfully",
            "IDKhachHang": customer_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/customers/me', methods=['PATCH'])
@require_role('KhachHang')
def update_my_profile():
    """Allow customers to update their own profile (SDT, name, CCCD, address)"""
    try:
        data = request.json
        customer_id = request.user['reference_id']
        conn = get_db_connection()
        cur = conn.cursor()

        # Update KhachHang.SDT or DiemTichLuy if provided
        if 'SDT' in data or 'DiemTichLuy' in data:
            fields = []
            params = []
            if 'SDT' in data:
                fields.append('SDT=%s')
                params.append(data.get('SDT'))
            if 'DiemTichLuy' in data:
                fields.append('DiemTichLuy=%s')
                params.append(data.get('DiemTichLuy'))
            params.append(customer_id)
            cur.execute(f"UPDATE KhachHang SET {', '.join(fields)} WHERE IDKhachHang=%s", tuple(params))

        # Handle CaNhan (personal info)
        # Find existing CCCD for this customer if any
        cur.execute("SELECT CCCD_CMND FROM CaNhan WHERE IDKhachHang=%s", (customer_id,))
        existing = cur.fetchone()
        existing_cccd = existing[0] if existing else None

        new_cccd = data.get('CCCD_CMND') or data.get('CCCD')
        ho = data.get('Ho')
        ten = data.get('Ten')
        diachi = data.get('DiaChi') or data.get('DiaChiCaNhan')

        if existing_cccd and (ho or ten):
            # update existing personal record
            fields = []
            params = []
            if ho is not None:
                fields.append('Ho=%s'); params.append(ho)
            if ten is not None:
                fields.append('Ten=%s'); params.append(ten)
            params.append(existing_cccd)
            cur.execute(f"UPDATE CaNhan SET {', '.join(fields)} WHERE CCCD_CMND=%s", tuple(params))
        elif new_cccd and (ho or ten):
            # insert new personal record
            try:
                cur.execute("INSERT INTO CaNhan (CCCD_CMND, IDKhachHang, Ho, Ten) VALUES (%s, %s, %s, %s)", (new_cccd, customer_id, ho, ten))
            except Exception:
                pass

        # Address handling
        target_cccd = new_cccd or existing_cccd
        if target_cccd and diachi is not None:
            # upsert DiaChiCaNhan
            cur.execute("SELECT CCCD_CMND FROM DiaChiCaNhan WHERE CCCD_CMND=%s", (target_cccd,))
            if cur.fetchone():
                cur.execute("UPDATE DiaChiCaNhan SET DiaChi=%s WHERE CCCD_CMND=%s", (diachi, target_cccd))
            else:
                try:
                    cur.execute("INSERT INTO DiaChiCaNhan (CCCD_CMND, DiaChi) VALUES (%s, %s)", (target_cccd, diachi))
                except Exception:
                    pass

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Profile updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/orders', methods=['GET'])
@require_auth
def list_orders():
    """List orders (customers see their own, staff/admin see all)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        if request.user['role'] == 'KhachHang':
            customer_id = request.user['reference_id']
            cur.execute("SELECT * FROM DonMuaHang WHERE IDKhachHang=%s ORDER BY NgayMua DESC", (customer_id,))
        else:
            cur.execute("SELECT * FROM DonMuaHang ORDER BY NgayMua DESC")

        orders = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/orders/<int:order_id>', methods=['PATCH'])
@require_role('Admin', 'NhanVienDungQuay')
def update_order(order_id):
    """Allow staff/admin to update order delivery status and assign staff"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()

        # Update GiaoTanNha if exists
        if 'TrangThai' in data or 'PhiVanChuyen' in data or 'IDNhanVien' in data:
            # Ensure a GiaoTanNha row exists for this order
            cur.execute("SELECT IDDonMuaHang FROM GiaoTanNha WHERE IDDonMuaHang=%s", (order_id,))
            if not cur.fetchone():
                # create a minimal record
                cur.execute("INSERT INTO GiaoTanNha (IDDonMuaHang, TrangThai) VALUES (%s, %s)", (order_id, data.get('TrangThai', 'Pending')))

            fields = []
            params = []
            if 'TrangThai' in data:
                fields.append('TrangThai=%s'); params.append(data.get('TrangThai'))
            if 'PhiVanChuyen' in data:
                fields.append('PhiVanChuyen=%s'); params.append(data.get('PhiVanChuyen'))
            if 'IDNhanVien' in data:
                fields.append('IDNhanVien=%s'); params.append(data.get('IDNhanVien'))
            params.append(order_id)
            cur.execute(f"UPDATE GiaoTanNha SET {', '.join(fields)} WHERE IDDonMuaHang=%s", tuple(params))

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Order updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/orders', methods=['POST'])
@require_auth
def create_order():
    """Create a new order. Customers create their own orders; Admin/Staff can create for any customer."""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()

        # Determine customer
        if request.user['role'] == 'KhachHang':
            id_khach = request.user['reference_id']
        else:
            id_khach = data.get('IDKhachHang')
            if not id_khach:
                return jsonify({"error": "IDKhachHang required for admin/staff orders"}), 400

        loai = data.get('LoaiHoaDon', 'Hóa đơn')
        ngay = data.get('NgayMua')
        if not ngay:
            from datetime import date
            ngay = date.today().isoformat()

        # Start transaction
        cur.execute("INSERT INTO DonMuaHang (LoaiHoaDon, NgayMua, IDKhachHang) VALUES (%s, %s, %s)", (loai, ngay, id_khach))
        order_id = cur.lastrowid

        items = data.get('items', [])
        if not items:
            conn.rollback()
            return jsonify({"error": "Order must include items"}), 400

        for it in items:
            cur.execute("INSERT INTO DonHangChiTiet (IDDonMuaHang, IDVatPham, SoLuong, GiaLucMua) VALUES (%s, %s, %s, %s)", (order_id, it['IDVatPham'], it['SoLuong'], it.get('GiaLucMua', 0)))

        # If delivery requested
        if data.get('isDelivery'):
            diachi = data.get('DiaChiNhanHang')
            trangthai = data.get('TrangThai', 'Chờ giao')
            phivc = data.get('PhiVanChuyen', 0)
            idnv = data.get('IDNhanVien')
            cur.execute("INSERT INTO GiaoTanNha (IDDonMuaHang, DiaChiNhanHang, TrangThai, PhiVanChuyen, IDNhanVien) VALUES (%s, %s, %s, %s, %s)", (order_id, diachi, trangthai, phivc, idnv))

        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Order created", "IDDonMuaHang": order_id}), 201
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
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
