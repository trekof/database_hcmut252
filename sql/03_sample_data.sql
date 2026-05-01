-- 03_sample_data.sql
-- Thêm dữ liệu mẫu có ý nghĩa cho tất cả các bảng chính (mỗi dữ liêu có ít nhất 5 bản ghi)

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
('KH001','0987000001',120),
('KH002','0987000002',50),
('KH003','0987000003',300),
('KH004','0987000004',0),
('KH005','0987000005',20);

-- CÁ NHÂN (>=5)
INSERT INTO CaNhan (CCCD_CMND, IDKhachHang, Ho, Ten) VALUES
('111111111111','KH001','Ly','An'),
('222222222222','KH002','Do','Binh'),
('333333333333','KH003','Vu','Cuong'),
('444444444444','KH004','Ngo','Dung'),
('555555555555','KH005','Dao','Mai');

-- ĐỊA CHỈ CÁ NHÂN
INSERT INTO DiaChiCaNhan (CCCD_CMND, DiaChi) VALUES
('111111111111','123 Le Loi, District 1'),
('222222222222','45 Tran Hung Dao, District 5'),
('333333333333','78 Nguyen Trai, District 3'),
('444444444444','9 Le Duan, District 1'),
('555555555555','12 Pham Ngu Lao, District 1');

-- THẺ THÀNH VIÊN (>=5)
INSERT INTO TheThanhVien (CCCD_CMND, MaThe, NgayLapThe, NgayHetHan) VALUES
('111111111111',1,'2023-01-01','2024-01-01'),
('222222222222',1,'2023-06-01','2024-06-01'),
('333333333333',1,'2022-12-15','2023-12-15'),
('444444444444',1,'2024-01-10','2025-01-10'),
('555555555555',1,'2024-02-01','2025-02-01');

-- TẬP THỂ CÔNG TY (example rows)
INSERT INTO TapTheCongTy (MaSoThue, IDKhachHang, TenCongTy) VALUES
('TAX001','KH002','ABC Trading'),
('TAX002','KH004','XYZ Supplies'),
('TAX003','KH005','Tech Solutions'),
('TAX004','KH001','Global Books'),
('TAX005','KH003','Innovatech');

-- VẬT PHẨM (>=5)
INSERT INTO VatPham (TenVatPham, SoLuongKhaDung, GiaNiemYet) VALUES
('Clean Code',10,250000.00),
('Design Patterns',5,300000.00),
('Nhan Dan Newspaper',20,5000.00),
('A4 Paper Pad',50,45000.00),
('Javascript Handbook',7,180000.00);

-- SÁCH / BÁO / VPP
INSERT INTO Sach (IDVatPham, NamXB, TacGia, NXB) VALUES
(1,2010,'Robert C. Martin','Prentice Hall'),
(2,1994,'Erich Gamma et al.','Addison-Wesley'),
(5,2018,'Florian','TechBooks'),
(3,2024,'Nhan Dan','Nhan Dan Publishing'),
(4,2020,'XBrand','XBrand Corp');

INSERT INTO Bao (IDVatPham, TapChi, So, ToaSoan) VALUES
(3,'Nhan Dan',12,'Editorial'),
(6,'Tech Today',5,'Tech Editorial'),
(7,'Office Weekly',20,'Office Editorial'),
(8,'Global News',30,'Global Editorial'),
(9,'Business Daily',15,'Business Editorial');

INSERT INTO VanPhongPham (IDVatPham, LoaiHang, HSX) VALUES
(4,'Office','XBrand'),
(10,'Stationery','OfficeSupplies'),
(11,'Writing','WriteWell'),
(12,'Paper','PaperCo'),
(13,'Desk Accessory','DeskMates');

-- BẢN COPY
INSERT INTO BanCopy (IDVatPham, MaSoBanCopy, TinhTrang) VALUES
(1,'BC001','Good'),
(1,'BC002','Good'),
(1,'BC003','Fair'),
(2,'BC001','Good'),
(2,'BC002','Damaged');

-- ĐỢT GIẢM GIÁ
INSERT INTO DotGiamGia (IDVatPham, NgayBatDau, NgayKetThuc, PhanTramGiamGia) VALUES
(1,'2024-04-01','2024-04-30',10),
(2,'2024-05-01','2024-05-10',15),
(5,'2024-06-01','2024-06-15',5),
(3,'2024-04-15','2024-04-25',20),
(4,'2024-05-05','2024-05-20',25);

-- ĐƠN MUA HÀNG + CHI TIẾT
INSERT INTO DonMuaHang (LoaiHoaDon, NgayMua, IDKhachHang) VALUES
('Online','2024-04-10','KH001'),
('Direct','2024-04-11','KH002'),
('Online','2024-04-12','KH003'),
('Direct','2024-04-13','KH004'),
('Online','2024-04-14','KH005');

INSERT INTO DonHangChiTiet (IDDonMuaHang, IDVatPham, SoLuong, GiaLucMua) VALUES
(1,1,1,250000.00),
(1,4,2,45000.00),
(2,2,1,300000.00),
(3,5,1,180000.00),
(4,3,3,5000.00),
(5,1,2,250000.00);

INSERT INTO GiaoTanNha (IDDonMuaHang, DiaChiNhanHang, TrangThai, PhiVanChuyen, IDNhanVien) VALUES
(1,'123 Le Loi','Delivered',30000.00,'NV003'),
(2,'45 Tran Hung Dao','In Transit',20000.00,'NV003'),
(3,'78 Nguyen Trai','Delivered',25000.00,'NV003'),
(4,'9 Le Duan','Pending',0.00,'NV003'),
(5,'12 Pham Ngu Lao','Delivered',30000.00,'NV003');

INSERT INTO MuaTrucTiep (IDDonMuaHang, IDNhanVien) VALUES
(2,'NV002'),
(4,'NV004'),
(1,'NV002'),
(3,'NV004'),
(5,'NV002');

-- LẦN MƯỢN / THUÊ
INSERT INTO LanMuon (IDVatPham, MaSoBanCopy, CCCD_CMND, MaThe, MaDonMuon, TinhTrangSauKhiTra, NgayMuon, HanTra) VALUES
(1,'BC001','111111111111',1,'MUO001','Good','2024-03-01','2024-03-15'),
(1,'BC002','222222222222',1,'MUO002','Good','2024-03-05','2024-03-20'),
(2,'BC001','333333333333',1,'MUO003','Damaged','2024-03-10','2024-03-25'),
(5,'BC001','444444444444',1,'MUO004','Good','2024-03-15','2024-03-30'),
(5,'BC002','555555555555',1,'MUO005','Good','2024-03-20','2024-04-05');

INSERT INTO LanThue (IDKhachHang, IDVatPham, MaDonThue, ThoiHanTra, GiaThue, NgayThue, NgayTra, SoLuong) VALUES
('KH001',5,'THU001','2024-05-01',50000.00,'2024-04-01','2024-04-15',1),
('KH002',1,'THU002','2024-05-10',70000.00,'2024-04-05','2024-04-20',1),
('KH003',2,'THU003','2024-06-01',80000.00,'2024-04-10','2024-05-10',1),
('KH004',3,'THU004','2024-05-15',2000.00,'2024-04-15','2024-05-15',2),
('KH005',4,'THU005','2024-06-10',10000.00,'2024-04-20','2024-06-10',5);

-- CẬP NHẬT
INSERT INTO CapNhat (IDNhanVien, IDVatPham, NgayCapNhat, SoLuong) VALUES
('NV001',1,'2024-01-10',10),
('NV001',2,'2024-02-10',5),
('NV002',3,'2024-03-10',20),
('NV002',4,'2024-04-10',50),
('NV003',5,'2024-05-10',7);

-- GIA HẠN THẺ
INSERT INTO GiaHanThe (CCCD_CMND, MaThe, IDNhanVien, NgayGiaHan) VALUES
('111111111111',1,'NV001','2024-03-01'),
('222222222222',1,'NV001','2024-04-01'),
('333333333333',1,'NV001','2024-05-01'),
('444444444444',1,'NV001','2024-06-01'),
('555555555555',1,'NV001','2024-07-01');

-- TEST ĐIỂM TÍCH LŨY
INSERT INTO KhachHang (IDKhachHang, SDT, DiemTichLuy) 
VALUES ('KH_TEST01', '0919123456', 0);

INSERT INTO CaNhan (CCCD_CMND, IDKhachHang, Ho, Ten) 
VALUES ('777777777777', 'KH_TEST01', 'Le', 'Khang');

-- Thêm vật phẩm để bán
INSERT INTO VatPham (TenVatPham, SoLuongKhaDung, GiaNiemYet) 
VALUES ('May Tinh Xach Tay', 10, 25000000.00);

INSERT INTO DonMuaHang (LoaiHoaDon, NgayMua, IDKhachHang) 
VALUES ('Online', '2026-04-15', 'KH_TEST01');

INSERT INTO DonHangChiTiet (IDDonMuaHang, IDVatPham, SoLuong, GiaLucMua) 
VALUES (LAST_INSERT_ID(), 6, 1, 25000000.00);

-- Kiểm tra điểm tích lũy sau khi mua hàng
SELECT DiemTichLuy 
FROM KhachHang 
WHERE IDKhachHang = 'KH_TEST01';

-- End sample data
