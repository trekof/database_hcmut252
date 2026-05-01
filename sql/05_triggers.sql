-- Tạo TRIGGER để tự động xử lý logic hệ thống

-- Trigger: Kiểm tra số lượng khi thêm chi tiết đơn hàng
CREATE TRIGGER tr_check_so_luong_don_hang
BEFORE INSERT ON DonHangChiTiet
FOR EACH ROW
BEGIN
    DECLARE v_soLuongTon INT;
    
    SELECT SoLuongKhaDung INTO v_soLuongTon FROM VatPham WHERE IDVatPham = NEW.IDVatPham;
    
    IF v_soLuongTon IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vật phẩm không tồn tại';
    END IF;
    
    IF NEW.SoLuong > v_soLuongTon THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Số lượng trong kho không đủ';
    END IF;
END;

-- Trigger: Cập nhật số lượng vật phẩm khi thêm đơn hàng
CREATE TRIGGER tr_update_so_luong_sau_don_hang
AFTER INSERT ON DonHangChiTiet
FOR EACH ROW
BEGIN
    UPDATE VatPham SET SoLuongKhaDung = SoLuongKhaDung - NEW.SoLuong WHERE IDVatPham = NEW.IDVatPham;
END;

-- Trigger: Hoàn lại số lượng khi xóa chi tiết đơn hàng
CREATE TRIGGER tr_restore_so_luong_khi_huy_don
AFTER DELETE ON DonHangChiTiet
FOR EACH ROW
BEGIN
    UPDATE VatPham SET SoLuongKhaDung = SoLuongKhaDung + OLD.SoLuong WHERE IDVatPham = OLD.IDVatPham;
END;

-- Trigger: Xác nhận CMND/CCCD không trùng lặp
CREATE TRIGGER tr_check_cmnd_nhan_vien
BEFORE INSERT ON NhanVien
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM NhanVien WHERE CMND_CCCD = NEW.CMND_CCCD AND IDNhanVien != NEW.IDNhanVien) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'CMND/CCCD đã tồn tại';
    END IF;
END;

-- Trigger: Kiểm tra trùng lặp đợt giảm giá
CREATE TRIGGER tg_CheckDiscountOverlap
BEFORE INSERT ON DotGiamGia
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM DotGiamGia
        WHERE IDVatPham = NEW.IDVatPham
          AND NEW.NgayBatDau <= NgayKetThuc
          AND NEW.NgayKetThuc >= NgayBatDau
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Lỗi: Thời gian giảm giá bị chồng chéo với một đợt đã tồn tại!';
    END IF;
END;

-- Trigger: Khi cập nhật LanMuon (trả), nếu bị hư/mất thì tạo bồi thường
CREATE TRIGGER tr_on_lanmuon_after_update
AFTER UPDATE ON LanMuon
FOR EACH ROW
BEGIN
    DECLARE v_price DECIMAL(15,2);
    DECLARE v_multiplier DECIMAL(4,2);
    -- If status changed to Hư or Mất
    IF NEW.TinhTrangSauKhiTra IN ('Hư', 'Mất') AND OLD.TinhTrangSauKhiTra NOT IN ('Hư','Mất') THEN
        -- Get price
        SELECT GiaNiemYet INTO v_price FROM VatPham WHERE IDVatPham = NEW.IDVatPham;
        IF v_price IS NULL THEN
            SET v_price = 0;
        END IF;
        -- Simple rule: Hư = 120% , Mất = 150%
        IF NEW.TinhTrangSauKhiTra = 'Hư' THEN
            SET v_multiplier = 1.2;
        ELSE
            SET v_multiplier = 1.5;
        END IF;
        INSERT INTO BoiThuong (IDVatPham, MaSoBanCopy, CCCD_CMND, MaDonMuon, SoTien, LyDo)
        VALUES (NEW.IDVatPham, NEW.MaSoBanCopy, NEW.CCCD_CMND, NEW.MaDonMuon, v_price * v_multiplier, CONCAT('Bồi thường do trả: ', NEW.TinhTrangSauKhiTra));
    END IF;
END;

-- Trigger: Khi thêm LanMuon hoặc LanThue (đã phần lớn xử lý trong procedure), nhưng kiểm tra khóa khách hàng
CREATE TRIGGER tr_check_khachhang_locked_before_lanmuon
BEFORE INSERT ON LanMuon
FOR EACH ROW
BEGIN
    DECLARE v_locked DATETIME;
    SELECT LockedUntil INTO v_locked FROM KhachHangKhoa WHERE IDKhachHang = (SELECT IDKhachHang FROM CaNhan WHERE CCCD_CMND = NEW.CCCD_CMND);
    IF v_locked IS NOT NULL AND v_locked >= NEW.NgayMuon THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Khách hàng đang bị khóa, không thể mượn';
    END IF;
END;

-- Trigger: Khi insert DonMuaHang, cập nhật điểm tích lũy nếu đủ doanh thu 5,000,000 trong năm
CREATE TRIGGER tr_after_insert_donmuahang
AFTER INSERT ON DonMuaHang
FOR EACH ROW
BEGIN
    DECLARE v_total_year DECIMAL(15,2);
    -- Tính tổng doanh thu của khách hàng trong năm hiện tại
    SELECT SUM(COALESCE(ct.SoLuong * ct.GiaLucMua,0)) INTO v_total_year
    FROM DonMuaHang d
    LEFT JOIN DonHangChiTiet ct ON d.IDDonMuaHang = ct.IDDonMuaHang
    WHERE d.IDKhachHang = NEW.IDKhachHang
      AND YEAR(d.NgayMua) = YEAR(NEW.NgayMua);

    -- Nếu có doanh thu >= 5,000,000 thì cộng điểm tích lũy (100 điểm) - chính sách placeholder
    IF v_total_year >= 5000000 THEN
        UPDATE KhachHang 
        SET DiemTichLuy = DiemTichLuy + 100 
        WHERE IDKhachHang = NEW.IDKhachHang;
    END IF;
END;

-- Trigger: Khi update LanMuon, xét trả trễ để khóa nếu 3 lần trễ trong 6 tháng theo ràng buộc 10
-- Ràng buộc 10: Nếu một khách hàng có từ 3 lần trả trễ hạn trở lên trong vòng 6 tháng, hệ thống phải tự động tạm khóa quyền tạo mới giao dịch mượn hoặc thuê trong thời hạn 30 ngày.
CREATE TRIGGER tr_check_late_returns_after_update
AFTER UPDATE ON LanMuon
FOR EACH ROW
BEGIN
    DECLARE v_late_count INT;
    DECLARE v_idKhach VARCHAR(20);
    
    -- Chỉ xem xét khi cột NgayTra được cập nhật (từ NULL thành có giá trị)
    IF NEW.NgayTra IS NOT NULL AND OLD.NgayTra IS NULL THEN
        -- Kiểm tra nếu ngày trả muộn hơn hạn trả
        IF NEW.NgayTra > NEW.HanTra THEN
            -- Lấy IDKhachHang từ bảng Cá Nhân dựa trên CCCD
            SELECT IDKhachHang INTO v_idKhach FROM CaNhan WHERE CCCD_CMND = NEW.CCCD_CMND;
            
            IF v_idKhach IS NOT NULL THEN
                -- Đếm số lần trả trễ hạn trong vòng 6 tháng qua
                SELECT COUNT(*) INTO v_late_count FROM LanMuon
                WHERE CCCD_CMND = NEW.CCCD_CMND
                  AND NgayTra > HanTra
                  AND NgayTra >= DATE_SUB(NEW.NgayTra, INTERVAL 6 MONTH);

                -- Nếu số lần vi phạm >= 3, thực hiện khóa
                IF v_late_count >= 3 THEN
                    INSERT INTO KhachHangKhoa (IDKhachHang, LockedUntil, Reason)
                    VALUES (v_idKhach, DATE_ADD(NEW.NgayTra, INTERVAL 30 DAY), '3 trả trễ trong 6 tháng')
                    ON DUPLICATE KEY UPDATE 
                        LockedUntil = DATE_ADD(NEW.NgayTra, INTERVAL 30 DAY), 
                        Reason = '3 trả trễ trong 6 tháng';
                END IF;
            END IF;
        END IF;
    END IF;
END;