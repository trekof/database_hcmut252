-- 03_sample_data.sql
-- Thêm dữ liệu mẫu cho hệ thống
-- Note: IDs like NV, KH, MUO, THU, BC được generate từ Backend

-- Thêm Nhân Viên (Backend sẽ generate IDNhanVien: NV001, NV002, ...)
INSERT INTO NhanVien (IDNhanVien, CMND_CCCD, Ho, Ten, NgaySinh, SDT, CongViec, BoPhanQuanLy) VALUES
('NV001', '001234567890', 'Nguyễn', 'Văn A', '1995-05-15', '0912345678', 'Quản lý bán hàng', 'Bộ phận bán hàng'),
('NV002', '002234567890', 'Trần', 'Thị B', '1998-08-20', '0913245678', 'Tài xế', 'Bộ phận giao hàng'),
('NV003', '003234567890', 'Lê', 'Văn C', '1992-03-10', '0914345678', 'Nhân viên đứng quầy', 'Bộ phận bán hàng'),
('NV004', '004234567890', 'Phạm', 'Thị D', '1996-11-25', '0915345678', 'Tài xế', 'Bộ phận giao hàng'),
('NV005', '005234567890', 'Hoàng', 'Văn E', '1991-07-30', '0916345678', 'Quản trị viên', 'Bộ phận quản lý'),
('NV006', '006234567890', 'Võ', 'Văn F', '1997-02-14', '0917345678', 'Tài xế', 'Bộ phận giao hàng');

-- Thêm Quản Trị Viên
INSERT INTO QuanTriVien (IDNhanVien, CapBac) VALUES
('NV005', 1);

-- Thêm Tài Xế Chuyên Hàng
INSERT INTO TaiXeChuyenHang (IDNhanVien, IDBangLaiXe) VALUES
('NV002', 'BLX001'),
('NV004', 'BLX002'),
('NV006', 'BLX003');

-- Thêm Nhân Viên Đứng Quầy
INSERT INTO NhanVienDungQuay (IDNhanVien, NamKinhNghiep) VALUES
('NV001', 2015),
('NV003', 2018);

-- Thêm Khách Hàng (Backend sẽ generate IDKhachHang: KH001, KH002, ...)
INSERT INTO KhachHang (IDKhachHang, SDT, DiemTichLuy) VALUES
('KH001', '0901111111', 150),
('KH002', '0902222222', 250),
('KH003', '0903333333', 100),
('KH004', '0904444444', 320),
('KH005', '0905555555', 0),
('KH006', '0906666666', 180);

-- Thêm Cá Nhân
INSERT INTO CaNhan (CCCD_CMND, IDKhachHang, Ho, Ten) VALUES
('001111111111', 'KH001', 'Nguyễn', 'Văn Nam'),
('002222222222', 'KH002', 'Trần', 'Thị Mai'),
('003333333333', 'KH003', 'Lê', 'Văn Hùng');

-- Thêm Địa chỉ Cá Nhân
INSERT INTO DiaChiCaNhan (CCCD_CMND, DiaChi) VALUES
('001111111111', '123 Đường Lê Lợi, Hà Nội'),
('002222222222', '456 Đường Nguyễn Huệ, TPHCM'),
('003333333333', '789 Đường Trần Hưng Đạo, Đà Nẵng');

-- Thêm Thẻ Thành Viên (MaThe là INT, Backend sẽ tính toán số tiếp theo)
INSERT INTO TheThanhVien (CCCD_CMND, MaThe, NgayLapThe, NgayHetHan) VALUES
('001111111111', 1, '2020-01-15', '2025-01-15'),
('002222222222', 2, '2021-03-20', '2026-03-20'),
('003333333333', 3, '2020-06-10', '2025-06-10');

-- Thêm Tập Thể Công Ty
INSERT INTO TapTheCongTy (MaSoThue, IDKhachHang, TenCongTy) VALUES
('0105123456', 'KH002', 'Công ty ABC'),
('0105234567', 'KH004', 'Công ty XYZ'),
('0105345678', 'KH006', 'Công ty DEF');

-- Thêm Vật Phẩm (IDVatPham là AUTO_INCREMENT)
INSERT INTO VatPham (TenVatPham, SoLuongKhaDung, GiaNiemYet) VALUES
('Lập trình Python cơ bản', 50, 100000),
('Java cho người mới bắt đầu', 35, 110000),
('Database MySQL nâng cao', 25, 150000),
('Web Development with React', 40, 130000),
('Lập trình C++ căn bản', 30, 120000);

-- Thêm Sách
INSERT INTO Sach (IDVatPham, NamXB, TacGia, NXB) VALUES
(1, 2022, 'Nguyễn Văn Tú', 'NXB Thời đại'),
(2, 2021, 'Trần Quốc Anh', 'NXB Giáo dục'),
(3, 2023, 'Lê Văn Hùng', 'NXB Lao động'),
(4, 2023, 'Phạm Quỳnh Trang', 'NXB FPT'),
(5, 2022, 'Hoàng Minh Châu', 'NXB Khoa học');

-- Thêm Vật Phẩm (Báo - Tạp chí)
INSERT INTO VatPham (TenVatPham, SoLuongKhaDung, GiaNiemYet) VALUES
('Tạp chí Tuổi Trẻ - Số tháng 4', 100, 18000),
('Báo Công Thương ngày 15/4', 120, 10000),
('Tạp chí PC World - Số 5', 60, 30000);

-- Thêm Báo
INSERT INTO Bao (IDVatPham, TapChi, So, ToaSoan) VALUES
(6, 'Tuổi Trẻ', 4, 'Tuổi Trẻ'),
(7, 'Công Thương', 15, 'Công Thương'),
(8, 'PC World', 5, 'PC World');

-- Thêm Vật Phẩm (Văn Phòng Phẩm)
INSERT INTO VatPham (TenVatPham, SoLuongKhaDung, GiaNiemYet) VALUES
('Bút bi Pentel BK77', 500, 4000),
('Vở kẻ ngang 80 trang', 200, 15000),
('Giấy A4 80gsm ream', 150, 80000),
('Bìa hồ sơ bìa cứng', 300, 20000);

-- Thêm Văn Phòng Phẩm
INSERT INTO VanPhongPham (IDVatPham, LoaiHang, HSX) VALUES
(9, 'Bút viết', 'Pentel'),
(10, 'Vở ghi chép', 'Hồng Hà'),
(11, 'Giấy in', 'Sao Thái'),
(12, 'Bìa hồ sơ', 'Hàng Việt');

-- Thêm Bản Copy (Backend generate MaBanCopy: BC001, BC002, ...)
INSERT INTO BanCopy (IDVatPham, MaBanCopy, TinhTrang) VALUES
(1, 'BC001', 'Tốt'),
(1, 'BC002', 'Tốt'),
(2, 'BC003', 'Tốt'),
(4, 'BC004', 'Tốt');

-- Thêm Đợt Giảm Giá
INSERT INTO DotGiamGia (IDVatPham, NgayBatDau, NgayKetThuc, PhanTramGiamGia) VALUES
(1, '2024-02-01', '2024-02-15', 10),
(2, '2024-02-05', '2024-02-20', 15),
(3, '2024-02-10', '2024-02-25', 20);

-- Thêm Đơn Mua Hàng (IDDonMuaHang là AUTO_INCREMENT)
INSERT INTO DonMuaHang (LoaiHoaDon, NgayMua, IDKhachHang) VALUES
('Hóa đơn', '2024-01-15', 'KH001'),
('Hóa đơn', '2024-01-18', 'KH002'),
('Hóa đơn', '2024-01-20', 'KH003'),
('Hóa đơn', '2024-02-05', 'KH004'),
('Hóa đơn', '2024-02-10', 'KH005'),
('Hóa đơn', '2024-02-15', 'KH006');

-- Thêm Chi Tiết Đơn Hàng
INSERT INTO DonHangChiTiet (IDDonMuaHang, IDVatPham, SoLuong, GiaLucMua) VALUES
(1, 1, 2, 85000),
(1, 2, 3, 90000),
(2, 3, 1, 120000),
(2, 4, 2, 110000),
(3, 5, 2, 95000),
(4, 6, 3, 15000),
(4, 7, 1, 8000),
(5, 9, 5, 3000),
(6, 11, 6, 65000);

-- Thêm Giao Tận Nhà
INSERT INTO GiaoTanNha (IDDonMuaHang, DiaChiNhanHang, TrangThai, PhiVanChuyen, IDNhanVien) VALUES
(1, '123 Đường Lê Lợi, Hà Nội', 'Đã giao', 20000, 'NV002'),
(2, '456 Đường Nguyễn Huệ, TPHCM', 'Đã giao', 25000, 'NV004'),
(3, '789 Đường Trần Hưng Đạo, Đà Nẵng', 'Đã giao', 15000, 'NV002'),
(4, 'Công ty XYZ, Hà Nội', 'Đang giao', 30000, 'NV006'),
(5, '123 Đường Lê Lợi, Hà Nội', 'Chờ giao', 20000, 'NV004'),
(6, 'Công ty DEF, TPHCM', 'Đã giao', 35000, 'NV002');

-- Thêm Mua Trực Tiếp
INSERT INTO MuaTrucTiep (IDDonMuaHang, IDNhanVien) VALUES
(1, 'NV003'),
(3, 'NV001');

-- Thêm Lần Mượn (Backend generate MaDonMuon: MUO001, MUO002, ...)
INSERT INTO LanMuon (IDVatPham, MaSoBanCopy, CCCD_CMND, MaThe, MaDonMuon, TinhTrangSauKhiTra, NgayMuon, HanTra) VALUES
(1, 'BC001', '001111111111', 1, 'MUO001', 'Tốt', '2024-02-20', '2024-03-20'),
(4, 'BC004', '002222222222', 2, 'MUO002', 'Tốt', '2024-02-22', '2024-03-22'),
(2, 'BC003', '003333333333', 3, 'MUO003', 'Tốt', '2024-02-25', '2024-03-25');

-- Thêm Lần Thuê (Backend generate MaDonThue: THU001, THU002, ...)
INSERT INTO LanThue (IDKhachHang, IDVatPham, MaDonThue, ThoiHanTra, GiaThue, NgayThue, NgayTra, SoLuong) VALUES
('KH001', 2, 'THU001', '2024-03-01', 20000, '2024-02-10', '2024-03-01', 2),
('KH003', 5, 'THU002', '2024-03-05', 15000, '2024-02-20', '2024-03-05', 1),
('KH005', 1, 'THU003', '2024-03-10', 25000, '2024-02-28', '2024-03-10', 3);

-- Thêm Cập Nhật
INSERT INTO CapNhat (IDNhanVien, IDVatPham, NgayCapNhat, SoLuong) VALUES
('NV005', 9, '2024-01-10', 100),
('NV005', 10, '2024-01-10', 50),
('NV005', 11, '2024-01-15', 80),
('NV005', 12, '2024-01-15', 60);

-- Thêm Gia Hạn Thẻ
INSERT INTO GiaHanThe (CCCD_CMND, MaThe, IDNhanVien, NgayGiaHan) VALUES
('001111111111', 1, 'NV005', '2025-01-10'),
('002222222222', 2, 'NV005', '2026-03-15');
