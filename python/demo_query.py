# python/demo_query.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from db import get_mysql_conn


def demo_get_all_nhan_vien():
    """Demo: Gọi PROCEDURE để lấy tất cả nhân viên"""
    print("\n=== Demo: Danh sách tất cả nhân viên ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor(dictionary=True)
    
    try:
        cur.callproc("sp_get_all_nhan_vien")
        
        print("\n📊 Kết quả:")
        for result in cur.stored_results():
            rows = result.fetchall()
            if rows:
                for r in rows:
                    print(f"  {r['IDNhanVien']:6} | {r['Ho']:10} {r['Ten']:10} | {r['SDT']:12} | {r['CongViec']}")
            else:
                print("  (Không có dữ liệu)")
    except Exception as e:
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


def demo_get_all_khach_hang():
    """Demo: Lấy danh sách khách hàng"""
    print("\n=== Demo: Danh sách khách hàng ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor(dictionary=True)
    
    try:
        cur.callproc("sp_get_all_khach_hang")
        
        print("\n📊 Kết quả:")
        for result in cur.stored_results():
            rows = result.fetchall()
            if rows:
                for r in rows:
                    print(f"  {r['IDKhachHang']:6} | {r['SDT']:12} | Điểm: {r['DiemTichLuy']:4} | NV: {r['IDNhanVienDamTrach']}")
            else:
                print("  (Không có dữ liệu)")
    except Exception as e:
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


def demo_get_all_vat_pham():
    """Demo: Lấy danh sách vật phẩm"""
    print("\n=== Demo: Danh sách vật phẩm ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor(dictionary=True)
    
    try:
        cur.callproc("sp_get_all_vat_pham")
        
        print("\n📊 Kết quả:")
        for result in cur.stored_results():
            rows = result.fetchall()
            if rows:
                for r in rows:
                    print(f"  {r['IDVatPham']:2} | {r['TenVatPham']:40} | SL: {r['SoLuong']:3} | Giá: {r['GiaLuong']:,} | Loại: {r['NhomVatPham']}")
            else:
                print("  (Không có dữ liệu)")
    except Exception as e:
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


def demo_get_all_don_hang():
    """Demo: Lấy danh sách đơn hàng"""
    print("\n=== Demo: Danh sách đơn hàng ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor(dictionary=True)
    
    try:
        cur.callproc("sp_get_all_don_hang")
        
        print("\n📊 Kết quả:")
        for result in cur.stored_results():
            rows = result.fetchall()
            if rows:
                for r in rows:
                    print(f"  {r['IDDonMua']:2} | {r['NgayMua']} | Mã: {r['MaDonMuon']} | KH: {r['IDKhachHang']} | Mặt hàng: {r['SoMatHang']}")
            else:
                print("  (Không có dữ liệu)")
    except Exception as e:
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


def demo_get_chi_tiet_don_hang():
    """Demo: Lấy chi tiết một đơn hàng"""
    print("\n=== Demo: Chi tiết đơn hàng (ID=1) ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor(dictionary=True)
    
    try:
        cur.callproc("sp_get_chi_tiet_don_hang", (1,))
        
        print("\n📊 Kết quả:")
        for result in cur.stored_results():
            rows = result.fetchall()
            if rows:
                tong = 0
                for r in rows:
                    print(f"  {r['TenVatPham']:40} | SL: {r['SoLuong']:2} | Giá: {r['GiaLuong']:,} | Thành tiền: {r['ThanhTien']:,}")
                    tong += r['ThanhTien']
                print(f"  {'Tổng cộng':40} | {' ':30} | {tong:,}")
            else:
                print("  (Không có dữ liệu)")
    except Exception as e:
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


def demo_get_giao_hang_by_taxi():
    """Demo: Lấy danh sách giao hàng của tài xế"""
    print("\n=== Demo: Danh sách giao hàng (Tài xế NV002) ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor(dictionary=True)
    
    try:
        cur.callproc("sp_get_giao_hang_by_taxi", ("NV002",))
        
        print("\n📊 Kết quả:")
        for result in cur.stored_results():
            rows = result.fetchall()
            if rows:
                for r in rows:
                    print(f"  {r['IDGiao']:2} | {r['NgayMua']} | Mã: {r['MaDonMuon']} | KH: {r['IDKhachHang']} | Phí: {r['PhiVanChuyen']:,}đ")
            else:
                print("  (Không có dữ liệu)")
    except Exception as e:
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


def demo_get_doanh_thu_khach_hang():
    """Demo: Thống kê doanh thu khách hàng"""
    print("\n=== Demo: Doanh thu khách hàng (KH001) ===")
    
    conn = get_mysql_conn()
    cur = conn.cursor(dictionary=True)
    
    try:
        cur.callproc("sp_get_doanh_thu_khach_hang", ("KH001",))
        
        print("\n📊 Kết quả:")
        for result in cur.stored_results():
            rows = result.fetchall()
            if rows:
                for r in rows:
                    print(f"  Khách hàng: {r['IDKhachHang']}")
                    print(f"  Số hóa đơn: {r['SoHoaDon']}")
                    print(f"  Tổng doanh số: {r['TongDoanh']:,}đ")
                    print(f"  Tổng phí vận chuyển: {r['TongPhiVanChuyen']:,}đ")
                    print(f"  Tổng thanh toán: {r['TongTT']:,}đ")
            else:
                print("  (Không có dữ liệu)")
    except Exception as e:
        print(f"✗ Lỗi: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    print("=" * 80)
    print("DEMO QUERY (Gọi PROCEDURE từ Python)")
    print("=" * 80)
    
    demo_get_all_nhan_vien()
    demo_get_all_khach_hang()
    demo_get_all_vat_pham()
    demo_get_all_don_hang()
    demo_get_chi_tiet_don_hang()
    demo_get_giao_hang_by_taxi()
    demo_get_doanh_thu_khach_hang()
    
    print("\n" + "=" * 80)
    print("✓ Demo Query completed!")
    print("=" * 80)
