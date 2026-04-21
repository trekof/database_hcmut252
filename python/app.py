# python/app.py
"""
Flask Backend API for Database Management System
Connects to MySQL and provides REST API endpoints
ID Generation Strategy: Backend generates formatted IDs (NV, KH, MUO, THU, BC)
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)
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

# ==================== ID GENERATION HELPERS ====================

def generate_next_id(prefix, table_name, id_column):
    """Generate next sequential ID with prefix (e.g., NV001, KH002)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get all IDs and extract numbers
        cur.execute(f"SELECT {id_column} FROM {table_name} WHERE {id_column} LIKE %s", (f"{prefix}%",))
        result = cur.fetchall()
        cur.close()
        conn.close()
        
        max_num = 0
        for row in result:
            id_val = row[0]
            # Extract number from ID (e.g., 'NV001' -> 001)
            match = re.search(r'\d+', id_val)
            if match:
                num = int(match.group())
                max_num = max(max_num, num)
        
        next_num = max_num + 1
        return f"{prefix}{next_num:03d}"
    except Exception as e:
        print(f"Error generating ID: {e}")
        return None

# ==================== FRONTEND ====================

@app.route('/')
def serve_root():
    """Serve index.html at root"""
    return send_from_directory('.', 'index.html')

@app.route('/index.html')
def serve_index():
    """Serve index.html"""
    return send_from_directory('.', 'index.html')

# ==================== EMPLOYEES ====================

@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Get all employees"""
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

@app.route('/api/employees/<id>', methods=['GET'])
def get_employee(id):
    """Get single employee by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM NhanVien WHERE IDNhanVien = %s", (id,))
        employee = cur.fetchone()
        cur.close()
        conn.close()
        
        if not employee:
            return jsonify({"error": "Employee not found"}), 404
        return jsonify(employee), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/employees', methods=['POST'])
def create_employee():
    """Create new employee - Backend generates IDNhanVien"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Generate next employee ID (NV001, NV002, etc.)
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

@app.route('/api/employees/<id>', methods=['PUT'])
def update_employee(id):
    """Update employee"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            UPDATE NhanVien 
            SET Ho=%s, Ten=%s, NgaySinh=%s, SDT=%s, CongViec=%s, BoPhanQuanLy=%s
            WHERE IDNhanVien=%s
        """
        
        cur.execute(query, (
            data.get('Ho'),
            data.get('Ten'),
            data.get('NgaySinh'),
            data.get('SDT'),
            data.get('CongViec'),
            data.get('BoPhanQuanLy'),
            id
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Employee updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/employees/<id>', methods=['DELETE'])
def delete_employee(id):
    """Delete employee"""
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
def get_customers():
    """Get all customers"""
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

@app.route('/api/customers/<id>', methods=['GET'])
def get_customer(id):
    """Get single customer by ID"""
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
def create_customer():
    """Create new customer - Backend generates IDKhachHang"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Generate next customer ID (KH001, KH002, etc.)
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

@app.route('/api/customers/<id>', methods=['PUT'])
def update_customer(id):
    """Update customer"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            UPDATE KhachHang 
            SET SDT=%s, DiemTichLuy=%s
            WHERE IDKhachHang=%s
        """
        
        cur.execute(query, (
            data.get('SDT'),
            data.get('DiemTichLuy'),
            id
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Customer updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/customers/<id>', methods=['DELETE'])
def delete_customer(id):
    """Delete customer"""
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

# ==================== ORDERS ====================

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM DonMuaHang ORDER BY IDDonMuaHang DESC")
        orders = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(orders), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders/<int:id>', methods=['GET'])
def get_order(id):
    """Get single order by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM DonMuaHang WHERE IDDonMuaHang = %s", (id,))
        order = cur.fetchone()
        cur.close()
        conn.close()
        
        if not order:
            return jsonify({"error": "Order not found"}), 404
        return jsonify(order), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create new order"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            INSERT INTO DonMuaHang 
            (LoaiHoaDon, NgayMua, IDKhachHang)
            VALUES (%s, %s, %s)
        """
        
        cur.execute(query, (
            data.get('LoaiHoaDon', 'Hóa đơn'),
            data.get('NgayMua', datetime.now().date()),
            data['IDKhachHang']
        ))
        
        order_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "message": "Order created successfully",
            "IDDonMuaHang": order_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== PRODUCTS ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
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
def get_product(id):
    """Get single product by ID"""
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
def create_product():
    """Create new product"""
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
def update_product(id):
    """Update product"""
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
def delete_product(id):
    """Delete product"""
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

# ==================== MEMBERSHIP CARDS ====================

@app.route('/api/membership/next-number', methods=['GET'])
def get_next_membership_number():
    """Get next membership card number (MaThe INT)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT MAX(CAST(MaThe AS UNSIGNED)) as max_num FROM TheThanhVien")
        result = cur.fetchone()
        max_num = result[0] if result[0] else 0
        
        cur.close()
        conn.close()
        
        return jsonify({"nextNumber": max_num + 1}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/membership', methods=['GET'])
def get_membership_cards():
    """Get all membership cards"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT t.*, c.Ho, c.Ten 
            FROM TheThanhVien t
            JOIN CaNhan c ON t.CCCD_CMND = c.CCCD_CMND
            ORDER BY t.MaThe
        """)
        cards = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(cards), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/membership', methods=['POST'])
def create_membership():
    """Create new membership card"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            INSERT INTO TheThanhVien 
            (CCCD_CMND, MaThe, NgayLapThe, NgayHetHan)
            VALUES (%s, %s, %s, %s)
        """
        
        cur.execute(query, (
            data['CCCD_CMND'],
            data['MaThe'],
            data.get('NgayLapThe', datetime.now().date()),
            data.get('NgayHetHan')
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Membership card created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== RENTALS ====================

@app.route('/api/rentals', methods=['GET'])
def get_rentals():
    """Get all rental records"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT l.*, vp.TenVatPham, kh.SDT
            FROM LanThue l
            JOIN VatPham vp ON l.IDVatPham = vp.IDVatPham
            JOIN KhachHang kh ON l.IDKhachHang = kh.IDKhachHang
            ORDER BY l.NgayThue DESC
        """)
        rentals = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rentals), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/rentals', methods=['POST'])
def create_rental():
    """Create new rental record - Backend generates MaDonThue"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Generate next rental ID (THU001, THU002, etc.)
        rental_id = generate_next_id('THU', 'LanThue', 'MaDonThue')
        if not rental_id:
            return jsonify({"error": "Failed to generate rental ID"}), 500
        
        query = """
            INSERT INTO LanThue 
            (IDKhachHang, IDVatPham, MaDonThue, NgayThue, NgayTra, ThoiHanTra, GiaThue, SoLuong)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cur.execute(query, (
            data['IDKhachHang'],
            data['IDVatPham'],
            rental_id,
            data.get('NgayThue', datetime.now().date()),
            data.get('NgayTra'),
            data.get('ThoiHanTra'),
            data.get('GiaThue'),
            data.get('SoLuong')
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "message": "Rental record created successfully",
            "MaDonThue": rental_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== BORROWING ====================

@app.route('/api/borrowing', methods=['GET'])
def get_borrowings():
    """Get all borrowing records"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT l.*, vp.TenVatPham, c.Ho, c.Ten
            FROM LanMuon l
            JOIN BanCopy bc ON l.IDVatPham = bc.IDVatPham AND l.MaSoBanCopy = bc.MaBanCopy
            JOIN VatPham vp ON bc.IDVatPham = vp.IDVatPham
            JOIN CaNhan c ON l.CCCD_CMND = c.CCCD_CMND
            ORDER BY l.NgayMuon DESC
        """)
        borrowings = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(borrowings), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/borrowing', methods=['POST'])
def create_borrowing():
    """Create new borrowing record - Backend generates MaDonMuon"""
    try:
        data = request.json
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Generate next borrowing ID (MUO001, MUO002, etc.)
        borrowing_id = generate_next_id('MUO', 'LanMuon', 'MaDonMuon')
        if not borrowing_id:
            return jsonify({"error": "Failed to generate borrowing ID"}), 500
        
        query = """
            INSERT INTO LanMuon 
            (IDVatPham, MaSoBanCopy, CCCD_CMND, MaThe, MaDonMuon, NgayMuon, HanTra, TinhTrangSauKhiTra)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cur.execute(query, (
            data['IDVatPham'],
            data['MaSoBanCopy'],
            data['CCCD_CMND'],
            data['MaThe'],
            borrowing_id,
            data.get('NgayMuon', datetime.now().date()),
            data.get('HanTra'),
            data.get('TinhTrangSauKhiTra', 'Chưa trả')
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "message": "Borrowing record created successfully",
            "MaDonMuon": borrowing_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== STATISTICS ====================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get basic statistics"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        
        # Count employees
        cur.execute("SELECT COUNT(*) as count FROM NhanVien")
        employee_count = cur.fetchone()['count']
        
        # Count customers
        cur.execute("SELECT COUNT(*) as count FROM KhachHang")
        customer_count = cur.fetchone()['count']
        
        # Count orders
        cur.execute("SELECT COUNT(*) as count FROM DonMuaHang")
        order_count = cur.fetchone()['count']
        
        # Count products
        cur.execute("SELECT COUNT(*) as count FROM VatPham")
        product_count = cur.fetchone()['count']
        
        cur.close()
        conn.close()
        
        return jsonify({
            "employees": employee_count,
            "customers": customer_count,
            "orders": order_count,
            "products": product_count
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    print("🚀 Starting Flask API server...")
    print("📍 http://localhost:5000")
    print("📊 Open http://localhost:5000/index.html")
    app.run(debug=True, host='0.0.0.0', port=5000)
