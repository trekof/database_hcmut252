-- 03_sample_data.sql
-- Thêm dữ liệu mẫu có ý nghĩa cho tất cả các bảng chính

-- NHÂN VIÊN (>=5)
INSERT INTO NhanVien (IDNhanVien, CMND_CCCD, CongViec, GioiTinh, NgaySinh, SDT, Ho, Ten, BoPhanQuanLy, IDQuanLy) VALUES
('NV001','001234567890','QuanTriVien','Male','1980-03-20','0912000001','Nguyen','An','Management',NULL),
('NV002','001234567891','NhanVienDungQuay','Female','1990-06-15','0912000002','Tran','Binh','Sales','NV001'),
('NV003','001234567892','TaiXeChuyenHang','Male','1985-01-10','0912000003','Le','Cuong','Logistics','NV001'),
('NV004','001234567893','NhanVienDungQuay','Female','1992-11-05','0912000004','Pham','Dung','Sales','NV002'),
('NV005','001234567894','QuanTriVien','Male','1978-08-30','0912000005','Hoang','Minh','Management','NV001');

-- PHỤ LỤC CHUYÊN MÔN
INSERT INTO QuanTriVien (IDNhanVien, CapBac) VALUES
('NV001', 1),('NV005', 2);

INSERT INTO NhanVienDungQuay (IDNhanVien, NamKinhNghiep) VALUES
('NV002', 5),('NV004', 3);

INSERT INTO TaiXeChuyenHang (IDNhanVien, IDBangLaiXe) VALUES
('NV003','BLX001');

-- NGƯỜI PHỤ THUỘC (>=5)
INSERT INTO NguoiPhuThuoc (IDNhanVien, CMND_CCCD, Quan_He, Ho, Ten) VALUES
('NV001','900000000001','Con','Nguyen','Linh'),
('NV001','900000000002','Vo','Nguyen','Mai'),
('NV002','900000000003','Con','Tran','Khang'),
('NV003','900000000004','Bo','Le','Hung'),
('NV004','900000000005','Vo','Pham','Lan');

-- KHÁCH HÀNG (>=5)
INSERT INTO KhachHang (IDKhachHang, SDT, DiemTichLuy) VALUES
('KH001','0987000001',120),('KH002','0987000002',50),('KH003','0987000003',300),('KH004','0987000004',0),('KH005','0987000005',20);

-- CÁ NHÂN (>=5)
INSERT INTO CaNhan (CCCD_CMND, IDKhachHang, Ho, Ten) VALUES
('111111111111','KH001','Ly','An'),('222222222222','KH002','Do','Binh'),('333333333333','KH003','Vu','Cuong'),('444444444444','KH004','Ngo','Dung'),('555555555555','KH005','Dao','Mai');

-- ĐỊA CHỈ CÁ NHÂN
INSERT INTO DiaChiCaNhan (CCCD_CMND, DiaChi) VALUES
('111111111111','123 Le Loi, District 1'),('222222222222','45 Tran Hung Dao, District 5'),('333333333333','78 Nguyen Trai, District 3'),('444444444444','9 Le Duan, District 1'),('555555555555','12 Pham Ngu Lao, District 1');

-- THẺ THÀNH VIÊN (>=5)
INSERT INTO TheThanhVien (CCCD_CMND, MaThe, NgayLapThe, NgayHetHan) VALUES
('111111111111',1,'2023-01-01','2024-01-01'),('222222222222',1,'2023-06-01','2024-06-01'),('333333333333',1,'2022-12-15','2023-12-15'),('444444444444',1,'2024-01-10','2025-01-10'),('555555555555',1,'2024-02-01','2025-02-01');

-- TẬP THỂ CÔNG TY (example rows)
INSERT INTO TapTheCongTy (MaSoThue, IDKhachHang, TenCongTy) VALUES
('TAX001','KH002','ABC Trading'),('TAX002','KH004','XYZ Supplies');

-- VẬT PHẨM (>=5)
INSERT INTO VatPham (TenVatPham, SoLuongKhaDung, GiaNiemYet) VALUES
('Clean Code',10,250000.00),('Design Patterns',5,300000.00),('Nhan Dan Newspaper',20,5000.00),('A4 Paper Pad',50,45000.00),('Javascript Handbook',7,180000.00);

-- SÁCH / BÁO / VPP
INSERT INTO Sach (IDVatPham, NamXB, TacGia, NXB) VALUES
(1,2010,'Robert C. Martin','Prentice Hall'),(2,1994,'Erich Gamma et al.','Addison-Wesley'),(5,2018,'Florian','TechBooks');

INSERT INTO Bao (IDVatPham, TapChi, So, ToaSoan) VALUES
(3,'Nhan Dan',12,'Editorial');

INSERT INTO VanPhongPham (IDVatPham, LoaiHang, HSX) VALUES
(4,'Office','XBrand');

-- BẢN COPY
INSERT INTO BanCopy (IDVatPham, MaSoBanCopy, TinhTrang) VALUES
(1,'BC001','Good'),(1,'BC002','Good'),(1,'BC003','Fair'),(2,'BC001','Good'),(2,'BC002','Damaged');

-- ĐỢT GIẢM GIÁ
INSERT INTO DotGiamGia (IDVatPham, NgayBatDau, NgayKetThuc, PhanTramGiamGia) VALUES
(1,'2024-04-01','2024-04-30',10),(2,'2024-05-01','2024-05-10',15),(5,'2024-06-01','2024-06-15',5);

-- ĐƠN MUA HÀNG + CHI TIẾT
INSERT INTO DonMuaHang (LoaiHoaDon, NgayMua, IDKhachHang) VALUES
('Online','2024-04-10','KH001'),('Direct','2024-04-11','KH002'),('Online','2024-04-12','KH003');

INSERT INTO DonHangChiTiet (IDDonMuaHang, IDVatPham, SoLuong, GiaLucMua) VALUES
(1,1,1,250000.00),(1,4,2,45000.00),(2,2,1,300000.00),(3,5,1,180000.00);

INSERT INTO GiaoTanNha (IDDonMuaHang, DiaChiNhanHang, TrangThai, PhiVanChuyen, IDNhanVien) VALUES
(1,'123 Le Loi','Delivered',30000.00,'NV003');

INSERT INTO MuaTrucTiep (IDDonMuaHang, IDNhanVien) VALUES
(2,'NV002');

-- LẦN MƯỢN / THUÊ
INSERT INTO LanMuon (IDVatPham, MaSoBanCopy, CCCD_CMND, MaThe, MaDonMuon, TinhTrangSauKhiTra, NgayMuon, HanTra) VALUES
(1,'BC001','111111111111',1,'MUO001','Good','2024-03-01','2024-03-15'),(1,'BC002','222222222222',1,'MUO002','Good','2024-03-05','2024-03-20');

INSERT INTO LanThue (IDKhachHang, IDVatPham, MaDonThue, ThoiHanTra, GiaThue, NgayThue, NgayTra, SoLuong) VALUES
('KH001',5,'THU001','2024-05-01',50000.00,'2024-04-01','2024-04-15',1);

-- CẬP NHẬT
INSERT INTO CapNhat (IDNhanVien, IDVatPham, NgayCapNhat, SoLuong) VALUES
('NV001',1,'2024-01-10',10),('NV001',2,'2024-02-10',5);

-- GIA HẠN THẺ
INSERT INTO GiaHanThe (CCCD_CMND, MaThe, IDNhanVien, NgayGiaHan) VALUES
('111111111111',1,'NV001','2024-03-01');

-- End sample data
