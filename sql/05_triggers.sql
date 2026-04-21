-- 05_triggers.sql
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