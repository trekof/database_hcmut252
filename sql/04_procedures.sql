-- 04_procedures.sql
-- Tạo PROCEDURE cho hệ thống quản lý bán hàng, giao hàng, cho thuê

-- ===== NHÂN VIÊN =====
-- Procedure: Thêm nhân viên mới
CREATE PROCEDURE sp_insert_nhan_vien(
    IN p_IDNhanVien VARCHAR(20),
    IN p_CMND_CCCD VARCHAR(12),
    IN p_Ho VARCHAR(50),
    IN p_Ten VARCHAR(50),
    IN p_NgaySinh DATE,
    IN p_SDT VARCHAR(15),
    IN p_CongViec VARCHAR(100),
    IN p_BoPhanQuanLy VARCHAR(50)
)
BEGIN
    IF EXISTS (SELECT 1 FROM NhanVien WHERE IDNhanVien = p_IDNhanVien) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Nhân viên đã tồn tại';
    END IF;
    
    INSERT INTO NhanVien (IDNhanVien, CMND_CCCD, Ho, Ten, NgaySinh, SDT, CongViec, BoPhanQuanLy)
    VALUES (p_IDNhanVien, p_CMND_CCCD, p_Ho, p_Ten, p_NgaySinh, p_SDT, p_CongViec, p_BoPhanQuanLy);
END;

-- Procedure: Lấy tất cả nhân viên
CREATE PROCEDURE sp_get_all_nhan_vien()
BEGIN
    SELECT IDNhanVien, Ho, Ten, NgaySinh, SDT, CongViec, BoPhanQuanLy FROM NhanVien ORDER BY IDNhanVien;
END;

-- Procedure: Tìm nhân viên theo ID
CREATE PROCEDURE sp_get_nhan_vien_by_id(IN p_IDNhanVien VARCHAR(20))
BEGIN
    SELECT IDNhanVien, Ho, Ten, NgaySinh, SDT, CongViec, BoPhanQuanLy FROM NhanVien WHERE IDNhanVien = p_IDNhanVien;
END;

-- ===== KHÁCH HÀNG =====
-- Procedure: Thêm khách hàng mới
CREATE PROCEDURE sp_insert_khach_hang(
    IN p_IDKhachHang VARCHAR(20),
    IN p_SDT VARCHAR(15)
)
BEGIN
    IF EXISTS (SELECT 1 FROM KhachHang WHERE IDKhachHang = p_IDKhachHang) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Khách hàng đã tồn tại';
    END IF;
    
    INSERT INTO KhachHang (IDKhachHang, SDT, DiemTichLuy)
    VALUES (p_IDKhachHang, p_SDT, 0);
END;

-- Procedure: Lấy tất cả khách hàng
CREATE PROCEDURE sp_get_all_khach_hang()
BEGIN
    SELECT IDKhachHang, SDT, DiemTichLuy FROM KhachHang ORDER BY IDKhachHang;
END;

-- Procedure: Cập nhật điểm tích lũy khách hàng
CREATE PROCEDURE sp_update_diem_tich_luy(
    IN p_IDKhachHang VARCHAR(20),
    IN p_DiemThem INT
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM KhachHang WHERE IDKhachHang = p_IDKhachHang) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Khách hàng không tồn tại';
    END IF;
    
    UPDATE KhachHang 
    SET DiemTichLuy = DiemTichLuy + p_DiemThem
    WHERE IDKhachHang = p_IDKhachHang;
END;

-- ===== VẬT PHẨM =====
-- Procedure: Thêm vật phẩm mới
CREATE PROCEDURE sp_insert_vat_pham(
    IN p_TenVatPham VARCHAR(100),
    IN p_SoLuongKhaDung INT,
    IN p_GiaNiemYet DECIMAL(10, 2)
)
BEGIN
    INSERT INTO VatPham (TenVatPham, SoLuongKhaDung, GiaNiemYet)
    VALUES (p_TenVatPham, p_SoLuongKhaDung, p_GiaNiemYet);
END;

-- Procedure: Lấy tất cả vật phẩm
CREATE PROCEDURE sp_get_all_vat_pham()
BEGIN
    SELECT IDVatPham, TenVatPham, SoLuongKhaDung, GiaNiemYet FROM VatPham ORDER BY IDVatPham;
END;

-- Procedure: Cập nhật số lượng vật phẩm
CREATE PROCEDURE sp_update_so_luong_vat_pham(
    IN p_IDVatPham INT,
    IN p_SoLuongKhaDung INT
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM VatPham WHERE IDVatPham = p_IDVatPham) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vật phẩm không tồn tại';
    END IF;
    
    UPDATE VatPham SET SoLuongKhaDung = p_SoLuongKhaDung WHERE IDVatPham = p_IDVatPham;
END;

-- ===== ĐƠN HÀNG =====
-- Procedure: Tạo đơn hàng mới
CREATE PROCEDURE sp_insert_don_mua_hang(
    IN p_LoaiHoaDon VARCHAR(50),
    IN p_NgayMua DATE,
    IN p_IDKhachHang VARCHAR(20),
    OUT p_IDDonMuaHang INT
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM KhachHang WHERE IDKhachHang = p_IDKhachHang) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Khách hàng không tồn tại';
    END IF;
    
    INSERT INTO DonMuaHang (LoaiHoaDon, NgayMua, IDKhachHang)
    VALUES (p_LoaiHoaDon, p_NgayMua, p_IDKhachHang);
    
    SET p_IDDonMuaHang = LAST_INSERT_ID();
END;

-- Procedure: Lấy tất cả đơn hàng
CREATE PROCEDURE sp_get_all_don_hang()
BEGIN
    SELECT d.IDDonMuaHang, d.LoaiHoaDon, d.NgayMua, d.IDKhachHang, COUNT(ct.IDVatPham) as SoMatHang
    FROM DonMuaHang d
    LEFT JOIN DonHangChiTiet ct ON d.IDDonMuaHang = ct.IDDonMuaHang
    GROUP BY d.IDDonMuaHang, d.LoaiHoaDon, d.NgayMua, d.IDKhachHang
    ORDER BY d.NgayMua DESC;
END;

-- Procedure: Lấy chi tiết đơn hàng
CREATE PROCEDURE sp_get_chi_tiet_don_hang(IN p_IDDonMuaHang INT)
BEGIN
    SELECT ct.IDDonMuaHang, ct.IDVatPham, vp.TenVatPham, ct.SoLuong, ct.GiaLucMua, 
           (ct.SoLuong * ct.GiaLucMua) as ThanhTien
    FROM DonHangChiTiet ct
    JOIN VatPham vp ON ct.IDVatPham = vp.IDVatPham
    WHERE ct.IDDonMuaHang = p_IDDonMuaHang;
END;

-- ===== GIAO HÀNG =====
-- Procedure: Ghi nhận giao hàng
CREATE PROCEDURE sp_insert_giao_hang(
    IN p_IDDonMuaHang INT,
    IN p_DiaChiNhanHang VARCHAR(100),
    IN p_TrangThai VARCHAR(50),
    IN p_PhiVanChuyen DECIMAL(10, 2),
    IN p_IDNhanVien VARCHAR(20)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM TaiXeChuyenHang WHERE IDNhanVien = p_IDNhanVien) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Tài xế không tồn tại';
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM DonMuaHang WHERE IDDonMuaHang = p_IDDonMuaHang) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Đơn hàng không tồn tại';
    END IF;
    
    INSERT INTO GiaoTanNha (IDDonMuaHang, DiaChiNhanHang, TrangThai, PhiVanChuyen, IDNhanVien)
    VALUES (p_IDDonMuaHang, p_DiaChiNhanHang, p_TrangThai, p_PhiVanChuyen, p_IDNhanVien);
END;

-- Procedure: Lấy danh sách giao hàng theo tài xế
CREATE PROCEDURE sp_get_giao_hang_by_taxi(IN p_IDNhanVien VARCHAR(20))
BEGIN
    SELECT g.IDDonMuaHang, d.NgayMua, d.LoaiHoaDon, d.IDKhachHang, g.PhiVanChuyen
    FROM GiaoTanNha g
    JOIN DonMuaHang d ON g.IDDonMuaHang = d.IDDonMuaHang
    WHERE g.IDNhanVien = p_IDNhanVien
    ORDER BY d.NgayMua DESC;
END;

-- ===== MƯỢN / THUÊ =====
-- Procedure: Thêm lần mượn với các ràng buộc nghiệp vụ
CREATE PROCEDURE sp_insert_lan_muon(
    IN p_IDVatPham INT,
    IN p_MaSoBanCopy VARCHAR(20),
    IN p_CCCD_CMND VARCHAR(20),
    IN p_MaThe INT,
    IN p_MaDonMuon VARCHAR(20),
    IN p_NgayMuon DATE
)
BEGIN
    DECLARE v_soLuong INT;
    DECLARE v_ngayLapThe DATE;
    DECLARE v_count_active INT;
    DECLARE v_idKhach VARCHAR(20);

    -- Check existence of copy and stock
    SELECT SoLuongKhaDung INTO v_soLuong FROM VatPham WHERE IDVatPham = p_IDVatPham;
    IF v_soLuong IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vật phẩm không tồn tại';
    END IF;

    IF v_soLuong <= 3 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vật phẩm tồn kho thấp, không cho phép mượn';
    END IF;

    -- Check thẻ thành viên validity
    SELECT NgayLapThe, NgayHetHan INTO v_ngayLapThe, @v_ngayHetHan FROM TheThanhVien WHERE CCCD_CMND = p_CCCD_CMND AND MaThe = p_MaThe;
    IF @v_ngayHetHan IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Thẻ thành viên không tồn tại';
    END IF;

    IF @v_ngayHetHan < p_NgayMuon THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Thẻ thành viên đã hết hạn';
    END IF;

    -- Limit: if within 30 days of card creation, max 2 active borrows
    IF DATEDIFF(p_NgayMuon, v_ngayLapThe) <= 30 THEN
        SELECT COUNT(*) INTO v_count_active FROM LanMuon WHERE CCCD_CMND = p_CCCD_CMND AND HanTra >= p_NgayMuon;
        IF v_count_active >= 2 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Giới hạn mượn trong 30 ngày đầu: tối đa 2 giao dịch';
        END IF;
    END IF;

    -- Borrow limits by customer type (simple policy)
    SELECT IDKhachHang INTO v_idKhach FROM CaNhan WHERE CCCD_CMND = p_CCCD_CMND;
    IF v_idKhach IS NULL THEN
        SELECT IDKhachHang INTO v_idKhach FROM TapTheCongTy WHERE MaSoThue = p_CCCD_CMND; -- try company mapping (if used)
    END IF;

    IF v_idKhach IS NOT NULL THEN
        -- assume CaNhan limit 5, TapTheCongTy limit 10
        IF EXISTS (SELECT 1 FROM CaNhan WHERE CCCD_CMND = p_CCCD_CMND) THEN
            SELECT COUNT(*) INTO v_count_active FROM LanMuon WHERE CCCD_CMND = p_CCCD_CMND AND HanTra >= p_NgayMuon;
            IF v_count_active >= 5 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Giới hạn mượn cho cá nhân đã đạt tối đa';
            END IF;
        ELSE
            SELECT COUNT(*) INTO v_count_active FROM LanMuon WHERE CCCD_CMND = p_CCCD_CMND AND HanTra >= p_NgayMuon;
            IF v_count_active >= 10 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Giới hạn mượn cho tổ chức đã đạt tối đa';
            END IF;
        END IF;
    END IF;

    -- Insert borrow record
    INSERT INTO LanMuon (IDVatPham, MaSoBanCopy, CCCD_CMND, MaThe, MaDonMuon, TinhTrangSauKhiTra, NgayMuon, HanTra)
    VALUES (p_IDVatPham, p_MaSoBanCopy, p_CCCD_CMND, p_MaThe, p_MaDonMuon, 'Tốt', p_NgayMuon, DATE_ADD(p_NgayMuon, INTERVAL 30 DAY));
END;

-- Procedure: Thêm lần thuê (yêu cầu xử lý đặt cọc nếu vật phẩm đắt)
CREATE PROCEDURE sp_insert_lan_thue(
    IN p_IDKhachHang VARCHAR(20),
    IN p_IDVatPham INT,
    IN p_MaDonThue VARCHAR(20),
    IN p_ThoiHanTra DATE,
    IN p_GiaThue DECIMAL(10,2),
    IN p_NgayThue DATE,
    IN p_SoLuong INT,
    IN p_PaymentDeposit DECIMAL(15,2)
)
BEGIN
    DECLARE v_gia DECIMAL(15,2);

    SELECT GiaNiemYet INTO v_gia FROM VatPham WHERE IDVatPham = p_IDVatPham;
    IF v_gia IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vật phẩm không tồn tại';
    END IF;

    IF v_gia > 2000000 THEN
        IF p_PaymentDeposit < (v_gia * 0.5) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Yêu cầu đặt cọc tối thiểu 50% cho vật phẩm giá cao';
        END IF;
    END IF;

    -- Check stock
    IF (SELECT SoLuongKhaDung FROM VatPham WHERE IDVatPham = p_IDVatPham) <= 3 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vật phẩm tồn kho thấp, không cho phép thuê';
    END IF;

    INSERT INTO LanThue (IDKhachHang, IDVatPham, MaDonThue, ThoiHanTra, GiaThue, NgayThue, NgayTra, SoLuong)
    VALUES (p_IDKhachHang, p_IDVatPham, p_MaDonThue, p_ThoiHanTra, p_GiaThue, p_NgayThue, NULL, p_SoLuong);
END;

-- ===== THỐNG KÊ =====
-- Procedure: Tính tổng doanh thu theo khách hàng
CREATE PROCEDURE sp_get_doanh_thu_khach_hang(IN p_IDKhachHang VARCHAR(20))
BEGIN
    SELECT d.IDKhachHang, k.SDT, 
           COUNT(DISTINCT d.IDDonMuaHang) as SoHoaDon,
           SUM(ct.SoLuong * ct.GiaLucMua) as TongDoanh,
           SUM(g.PhiVanChuyen) as TongPhiVanChuyen,
           (SUM(ct.SoLuong * ct.GiaLucMua) + SUM(COALESCE(g.PhiVanChuyen, 0))) as TongTT
    FROM DonMuaHang d
    LEFT JOIN DonHangChiTiet ct ON d.IDDonMuaHang = ct.IDDonMuaHang
    LEFT JOIN GiaoTanNha g ON d.IDDonMuaHang = g.IDDonMuaHang
    LEFT JOIN KhachHang k ON d.IDKhachHang = k.IDKhachHang
    WHERE d.IDKhachHang = p_IDKhachHang
    GROUP BY d.IDKhachHang;
END;

CREATE PROCEDURE sp_btl21_vat_pham_insert(
    IN p_TenVatPham VARCHAR(100),
    IN p_SoLuongKhaDung INT,
    IN p_GiaNiemYet DECIMAL(10, 2)
)
BEGIN
    IF p_TenVatPham IS NULL OR CHAR_LENGTH(TRIM(p_TenVatPham)) = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Tên vật phẩm không được để trống';
    END IF;

    IF CHAR_LENGTH(TRIM(p_TenVatPham)) > 100 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Tên vật phẩm vượt quá 100 ký tự';
    END IF;

    IF p_SoLuongKhaDung IS NULL OR p_SoLuongKhaDung < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Số lượng khả dụng không được âm và phải được nhập';
    END IF;

    IF p_GiaNiemYet IS NULL OR p_GiaNiemYet <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Giá niêm yết phải là số dương (lớn hơn 0)';
    END IF;

    IF EXISTS (SELECT 1 FROM VatPham WHERE TenVatPham = TRIM(p_TenVatPham)) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Trùng tên vật phẩm (ràng buộc duy nhất TenVatPham)';
    END IF;

    INSERT INTO VatPham (TenVatPham, SoLuongKhaDung, GiaNiemYet)
    VALUES (TRIM(p_TenVatPham), p_SoLuongKhaDung, p_GiaNiemYet);

    SELECT LAST_INSERT_ID() AS IDVatPham;
END;

CREATE PROCEDURE sp_btl21_vat_pham_update(
    IN p_IDVatPham INT,
    IN p_TenVatPham VARCHAR(100),
    IN p_SoLuongKhaDung INT,
    IN p_GiaNiemYet DECIMAL(10, 2)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM VatPham WHERE IDVatPham = p_IDVatPham) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vật phẩm không tồn tại (ID không hợp lệ)';
    END IF;

    IF p_TenVatPham IS NULL OR CHAR_LENGTH(TRIM(p_TenVatPham)) = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Tên vật phẩm không được để trống';
    END IF;

    IF CHAR_LENGTH(TRIM(p_TenVatPham)) > 100 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Tên vật phẩm vượt quá 100 ký tự';
    END IF;

    IF p_SoLuongKhaDung IS NULL OR p_SoLuongKhaDung < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Số lượng khả dụng không được âm và phải được nhập';
    END IF;

    IF p_GiaNiemYet IS NULL OR p_GiaNiemYet <= 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Giá niêm yết phải là số dương (lớn hơn 0)';
    END IF;

    IF EXISTS (
        SELECT 1 FROM VatPham
        WHERE TenVatPham = TRIM(p_TenVatPham) AND IDVatPham <> p_IDVatPham
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Trùng tên vật phẩm với một mặt hàng khác';
    END IF;

    UPDATE VatPham
    SET TenVatPham = TRIM(p_TenVatPham),
        SoLuongKhaDung = p_SoLuongKhaDung,
        GiaNiemYet = p_GiaNiemYet
    WHERE IDVatPham = p_IDVatPham;
END;

CREATE PROCEDURE sp_btl21_vat_pham_delete(IN p_IDVatPham INT)
BEGIN
    DECLARE v_od INT DEFAULT 0;

    IF NOT EXISTS (SELECT 1 FROM VatPham WHERE IDVatPham = p_IDVatPham) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vật phẩm không tồn tại (không thể xóa)';
    END IF;

    SELECT COUNT(*) INTO v_od FROM DonHangChiTiet WHERE IDVatPham = p_IDVatPham;
    IF v_od > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Không thể xóa: vật phẩm đã xuất hiện trong đơn hàng (DonHangChiTiet)';
    END IF;

    DELETE FROM VatPham WHERE IDVatPham = p_IDVatPham;
END;

CREATE PROCEDURE sp_btl23_tim_sach(
    IN p_tu_khoa VARCHAR(100),
    IN p_nam_xb_min INT,
    IN p_nam_xb_max INT,
    IN p_gia_min DECIMAL(10, 2),
    IN p_gia_max DECIMAL(10, 2)
)
BEGIN
    SELECT
        vp.IDVatPham,
        vp.TenVatPham,
        vp.SoLuongKhaDung,
        vp.GiaNiemYet,
        s.NamXB,
        s.TacGia,
        s.NXB
    FROM VatPham vp
    INNER JOIN Sach s ON vp.IDVatPham = s.IDVatPham
    WHERE
        (p_tu_khoa IS NULL OR TRIM(p_tu_khoa) = '' OR
         vp.TenVatPham LIKE CONCAT('%', TRIM(p_tu_khoa), '%') OR
         s.TacGia LIKE CONCAT('%', TRIM(p_tu_khoa), '%'))
        AND (p_nam_xb_min IS NULL OR s.NamXB >= p_nam_xb_min)
        AND (p_nam_xb_max IS NULL OR s.NamXB <= p_nam_xb_max)
        AND (p_gia_min IS NULL OR vp.GiaNiemYet >= p_gia_min)
        AND (p_gia_max IS NULL OR vp.GiaNiemYet <= p_gia_max)
    ORDER BY vp.GiaNiemYet ASC, vp.TenVatPham ASC;
END;

CREATE PROCEDURE sp_btl23_thong_ke_ban_vat_pham(
    IN p_tu_ngay DATE,
    IN p_den_ngay DATE,
    IN p_doanh_toi_thieu DECIMAL(15, 2)
)
BEGIN
    SELECT
        vp.IDVatPham,
        vp.TenVatPham,
        SUM(ct.SoLuong * ct.GiaLucMua) AS TongDoanh,
        SUM(ct.SoLuong) AS TongSoLuongBan
    FROM VatPham vp
    INNER JOIN DonHangChiTiet ct ON vp.IDVatPham = ct.IDVatPham
    INNER JOIN DonMuaHang d ON ct.IDDonMuaHang = d.IDDonMuaHang
    WHERE
        (p_tu_ngay IS NULL OR d.NgayMua >= p_tu_ngay)
        AND (p_den_ngay IS NULL OR d.NgayMua <= p_den_ngay)
    GROUP BY vp.IDVatPham, vp.TenVatPham
    HAVING SUM(ct.SoLuong * ct.GiaLucMua) >= IFNULL(p_doanh_toi_thieu, 0)
    ORDER BY TongDoanh DESC;
END;
