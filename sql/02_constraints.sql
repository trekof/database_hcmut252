-- 02_constraints.sql
-- Thêm UNIQUE constraints và Indexes

-- Thêm unique index để đảm bảo dữ liệu không trùng lặp
ALTER TABLE VatPham
ADD CONSTRAINT ui_vp_ten UNIQUE (TenVatPham);

-- Index để tối ưu hóa truy vấn
CREATE INDEX idx_nhanvien_cmnd ON NhanVien(CMND_CCCD);
CREATE INDEX idx_khachhang_sdt ON KhachHang(SDT);
CREATE INDEX idx_donmuahang_khachhang ON DonMuaHang(IDKhachHang);
CREATE INDEX idx_donmuahang_ngaymua ON DonMuaHang(NgayMua);
CREATE INDEX idx_giaotaneha_nhanvien ON GiaoTanNha(IDNhanVien);
CREATE INDEX idx_giaotaneha_donmua ON GiaoTanNha(IDDonMuaHang);
CREATE INDEX idx_donhangchitiet_donmua ON DonHangChiTiet(IDDonMuaHang);
CREATE INDEX idx_donhangchitiet_vatpham ON DonHangChiTiet(IDVatPham);
CREATE INDEX idx_lanthue_khachhang ON LanThue(IDKhachHang);
CREATE INDEX idx_lanthue_vatpham ON LanThue(IDVatPham);
CREATE INDEX idx_lanmuon_vatpham ON LanMuon(IDVatPham);
CREATE INDEX idx_capnhat_nhanvien ON CapNhat(IDNhanVien);
CREATE INDEX idx_capnhat_vatpham ON CapNhat(IDVatPham);

-- Table: BoiThuong (bồi thường khi trả hư/mất)
CREATE TABLE IF NOT EXISTS BoiThuong (
	IDBoiThuong INT AUTO_INCREMENT PRIMARY KEY,
	IDVatPham INT,
	MaSoBanCopy VARCHAR(20),
	CCCD_CMND VARCHAR(20),
	MaDonMuon VARCHAR(20),
	SoTien DECIMAL(15,2),
	LyDo VARCHAR(255),
	CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (IDVatPham) REFERENCES VatPham(IDVatPham) ON DELETE SET NULL
);

-- Table: KhachHangKhoa (tạm khóa quyền mượn/thue)
CREATE TABLE IF NOT EXISTS KhachHangKhoa (
	IDKhachHang VARCHAR(20) PRIMARY KEY,
	LockedUntil DATETIME,
	Reason VARCHAR(255),
	INDEX (LockedUntil)
);
