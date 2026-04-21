# python/demo_crud.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from db import get_mysql_conn


def demo_insert_nhan_vien():
    """Demo: Gọi PROCEDURE để INSERT nhân viên"""
    print("\n=== Demo: Thêm nhân viên mới ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor()
    
    try:
        cur.callproc("sp_insert_nhan_vien", (
            "NV007", "007234567890", "Trịnh", "Văn G", 
            "1999-09-05", "0918345678", "Nhân viên kho", "Khu công nghiệp"
        ))
        conn.commit()
        print("✓ Thêm nhân viên thành công")
    except Exception as e:
        conn.rollback()
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


def demo_insert_khach_hang():
    """Demo: Gọi PROCEDURE để INSERT khách hàng"""
    print("\n=== Demo: Thêm khách hàng mới ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor()
    
    try:
        cur.callproc("sp_insert_khach_hang", ("KH007", "0907777777", "NV001"))
        conn.commit()
        print("✓ Thêm khách hàng thành công")
    except Exception as e:
        conn.rollback()
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


def demo_insert_vat_pham():
    """Demo: Gọi PROCEDURE để INSERT vật phẩm"""
    print("\n=== Demo: Thêm vật phẩm mới ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor()
    
    try:
        cur.callproc("sp_insert_vat_pham", (
            "Sách Python 3 Nâng Cao", 45, 105000, 130000, "Sách"
        ))
        conn.commit()
        print("✓ Thêm vật phẩm thành công")
    except Exception as e:
        conn.rollback()
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


def demo_update_diem_tich_luy():
    """Demo: Cập nhật điểm tích lũy khách hàng"""
    print("\n=== Demo: Cập nhật điểm tích lũy ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor()
    
    try:
        cur.callproc("sp_update_diem_tich_luy", ("KH001", 50))
        conn.commit()
        print("✓ Cập nhật điểm tích lũy thành công")
    except Exception as e:
        conn.rollback()
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


def demo_insert_don_mua_hang():
    """Demo: Tạo đơn hàng mới"""
    print("\n=== Demo: Tạo đơn hàng mới ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor()
    
    try:
        # Gọi procedure với parameter OUT
        cur.callproc("sp_insert_don_mua_hang", (
            "2024-04-08", "DM007", 3, "KH007", 0
        ))
        
        # Lấy giá trị OUTPUT
        result = cur.fetchone()
        if result:
            print(f"✓ Tạo đơn hàng thành công - ID: {result[0]}")
        else:
            print("✓ Tạo đơn hàng thành công")
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    print("=" * 50)
    print("DEMO CRUD OPS (Gọi PROCEDURE từ Python)")
    print("=" * 50)
    
    demo_insert_nhan_vien()
    demo_insert_khach_hang()
    demo_insert_vat_pham()
    demo_update_diem_tich_luy()
    demo_insert_don_mua_hang()
    
    print("\n" + "=" * 50)
    print("✓ Demo CRUD completed!")
    print("=" * 50)
