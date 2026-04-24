-- 06_functions.sql
-- Tạo FUNCTION để tính toán hoặc xử lý dữ liệu

-- Function: Tính tổng tiền một đơn hàng (không tính phí vận chuyển)
CREATE FUNCTION fn_tong_tien_don_hang(p_IDDonMuaHang INT)
RETURNS DECIMAL(15, 2)
READS SQL DATA
BEGIN
    DECLARE total DECIMAL(15, 2);
    SELECT SUM(SoLuong * GiaLucMua) INTO total
    FROM DonHangChiTiet
    WHERE IDDonMuaHang = p_IDDonMuaHang;
    RETURN COALESCE(total, 0);
END;

-- Function: Tính tổng doanh thu khách hàng (có tính phí vận chuyển)
CREATE FUNCTION fn_doanh_thu_khach_hang(p_IDKhachHang VARCHAR(20))
RETURNS DECIMAL(15, 2)
READS SQL DATA
BEGIN
    DECLARE total DECIMAL(15, 2);
    SELECT SUM(COALESCE(ct.SoLuong * ct.GiaLucMua, 0)) + SUM(COALESCE(g.PhiVanChuyen, 0)) INTO total
    FROM DonMuaHang d
    LEFT JOIN DonHangChiTiet ct ON d.IDDonMuaHang = ct.IDDonMuaHang
    LEFT JOIN GiaoTanNha g ON d.IDDonMuaHang = g.IDDonMuaHang
    WHERE d.IDKhachHang = p_IDKhachHang;
    RETURN COALESCE(total, 0);
END;

-- Function: Đếm số hóa đơn của khách hàng
CREATE FUNCTION fn_count_don_hang_khach_hang(p_IDKhachHang VARCHAR(20))
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE cnt INT;
    SELECT COUNT(*) INTO cnt
    FROM DonMuaHang
    WHERE IDKhachHang = p_IDKhachHang;
    RETURN cnt;
END;

-- Function: Tính tổng số lượng vật phẩm bán được
CREATE FUNCTION fn_tong_so_luong_ban_duoc(p_IDVatPham INT)
RETURNS INT
READS SQL DATA
BEGIN
    DECLARE cnt INT;
    SELECT SUM(SoLuong) INTO cnt
    FROM DonHangChiTiet
    WHERE IDVatPham = p_IDVatPham;
    RETURN COALESCE(cnt, 0);
END;

-- Function: Lấy chữ cái đầu và chuỗi tên nhân viên
CREATE FUNCTION fn_ho_ten_nhan_vien(p_IDNhanVien VARCHAR(20))
RETURNS VARCHAR(100)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE fullname VARCHAR(100);
    SELECT CONCAT(COALESCE(Ho, ''), ' ', COALESCE(Ten, '')) INTO fullname
    FROM NhanVien
    WHERE IDNhanVien = p_IDNhanVien;
    RETURN TRIM(fullname);
END;

-- Function: Lệnh để kiểm tra khách hàng VIP (có điểm tích lũy >= 300)
CREATE FUNCTION fn_la_khach_hang_vip(p_IDKhachHang VARCHAR(20))
RETURNS BOOLEAN
READS SQL DATA
BEGIN
    DECLARE diem INT;
    SELECT DiemTichLuy INTO diem
    FROM KhachHang
    WHERE IDKhachHang = p_IDKhachHang;
    RETURN diem >= 300;
END;

-- Function: Mask phone number for staff (show only last 3 digits)
CREATE FUNCTION fn_mask_sdt(p_SDT VARCHAR(20), p_role VARCHAR(50))
RETURNS VARCHAR(50)
DETERMINISTIC
READS SQL DATA
BEGIN
    IF p_role = 'NhanVienDungQuay' THEN
        IF p_SDT IS NULL THEN
            RETURN NULL;
        END IF;
        RETURN CONCAT(REPEAT('*', GREATEST(0, CHAR_LENGTH(p_SDT) - 3)), SUBSTRING(p_SDT, -3));
    ELSE
        RETURN p_SDT;
    END IF;
END;

-- Function: Compute compensation amount (percentage rule)
CREATE FUNCTION fn_compute_compensation(p_IDVatPham INT, p_status VARCHAR(20))
RETURNS DECIMAL(15,2)
READS SQL DATA
BEGIN
    DECLARE v_price DECIMAL(15,2);
    DECLARE v_multiplier DECIMAL(4,2);
    SELECT GiaNiemYet INTO v_price FROM VatPham WHERE IDVatPham = p_IDVatPham;
    IF v_price IS NULL THEN
        RETURN 0;
    END IF;
    IF p_status = 'Hư' THEN
        SET v_multiplier = 1.2;
    ELSEIF p_status = 'Mất' THEN
        SET v_multiplier = 1.5;
    ELSE
        SET v_multiplier = 0;
    END IF;
    RETURN v_price * v_multiplier;
END;

-- Function: Tính giá trị trung bình mỗi hóa đơn của khách hàng
CREATE FUNCTION fn_gia_tri_tb_don_hang(p_IDKhachHang VARCHAR(20))
RETURNS DECIMAL(15, 2)
READS SQL DATA
BEGIN
    DECLARE avg_value DECIMAL(15, 2);
    SELECT AVG(COALESCE(ct.SoLuong * ct.GiaLucMua, 0) + COALESCE(g.PhiVanChuyen, 0)) INTO avg_value
    FROM DonMuaHang d
    LEFT JOIN DonHangChiTiet ct ON d.IDDonMuaHang = ct.IDDonMuaHang
    LEFT JOIN GiaoTanNha g ON d.IDDonMuaHang = g.IDDonMuaHang
    WHERE d.IDKhachHang = p_IDKhachHang;
    RETURN COALESCE(avg_value, 0);
END;
