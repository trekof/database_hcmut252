CREATE DATABASE IF NOT EXISTS btl2_db;
USE btl2_db;

-- =====================================================
-- PHẦN 1: NHÂN VIÊN VÀ NGƯỜI PHỤ THUỘC
-- =====================================================

-- 1. Nhân Viên
-- Backend sẽ tính toán mã: NV + số thứ tự (ví dụ: NV001)
CREATE TABLE IF NOT EXISTS NhanVien (
    IDNhanVien VARCHAR(20) PRIMARY KEY, 
    CMND_CCCD VARCHAR(12) UNIQUE NOT NULL,
    CongViec VARCHAR(100),
    GioiTinh VARCHAR(20),
    NgaySinh DATE NOT NULL,
    SDT VARCHAR(15) UNIQUE,
    Ho VARCHAR(50),
    Ten VARCHAR(50),
    BoPhanQuanLy VARCHAR(50),
    IDQuanLy VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (IDQuanLy) REFERENCES NhanVien(IDNhanVien) ON DELETE SET NULL,
    INDEX (IDNhanVien) -- Tối ưu cho việc Backend tìm kiếm mã
);

-- 2. Người Phụ Thuộc
CREATE TABLE IF NOT EXISTS NguoiPhuThuoc (
    IDNhanVien VARCHAR(20) NOT NULL,
    CMND_CCCD VARCHAR(12),
    Quan_He VARCHAR(50),
    Ho VARCHAR(50),
    Ten VARCHAR(50),
    PRIMARY KEY (IDNhanVien, CMND_CCCD),
    FOREIGN KEY (IDNhanVien) REFERENCES NhanVien(IDNhanVien) ON DELETE CASCADE
);

-- 3. Quản Trị Viên
CREATE TABLE IF NOT EXISTS QuanTriVien (
    IDNhanVien VARCHAR(20) PRIMARY KEY,
    CapBac INT,
    FOREIGN KEY (IDNhanVien) REFERENCES NhanVien(IDNhanVien) ON DELETE CASCADE
);

-- =====================================================
-- PHẦN 2: CHUYÊN MÔN NHÂN VIÊN
-- =====================================================

-- 4. Tài Xế Chuyên Hàng
CREATE TABLE IF NOT EXISTS TaiXeChuyenHang (
    IDNhanVien VARCHAR(20) PRIMARY KEY,
    IDBangLaiXe VARCHAR(20),
    FOREIGN KEY (IDNhanVien) REFERENCES NhanVien(IDNhanVien) ON DELETE CASCADE
);

-- 5. Nhân Viên Đứng Quầy
CREATE TABLE IF NOT EXISTS NhanVienDungQuay (
    IDNhanVien VARCHAR(20) PRIMARY KEY,
    NamKinhNghiep INT,
    FOREIGN KEY (IDNhanVien) REFERENCES NhanVien(IDNhanVien) ON DELETE CASCADE
);

-- =====================================================
-- PHẦN 3: KHÁCH HÀNG & THÀNH VIÊN
-- =====================================================

-- 6. Khách Hàng
-- Backend tính mã: KH + số (ví dụ: KH001)
CREATE TABLE IF NOT EXISTS KhachHang (
    IDKhachHang VARCHAR(20) PRIMARY KEY,
    SDT VARCHAR(15),
    DiemTichLuy INT DEFAULT 0,
    INDEX (IDKhachHang)
);

-- 7. Cá Nhân
CREATE TABLE IF NOT EXISTS CaNhan (
    CCCD_CMND VARCHAR(20),
    IDKhachHang VARCHAR(20),
    Ho VARCHAR(50),
    Ten VARCHAR(50),
    PRIMARY KEY (CCCD_CMND, IDKhachHang),
    FOREIGN KEY (IDKhachHang) REFERENCES KhachHang(IDKhachHang) ON DELETE CASCADE
);

-- 8. Địa chỉ cá nhân
CREATE TABLE IF NOT EXISTS DiaChiCaNhan (
    CCCD_CMND VARCHAR(20) PRIMARY KEY,
    DiaChi VARCHAR(200),
    FOREIGN KEY (CCCD_CMND) REFERENCES CaNhan(CCCD_CMND) ON DELETE CASCADE
);

-- 9. Tập Thể Công Ty
CREATE TABLE IF NOT EXISTS TapTheCongTy (
    MaSoThue VARCHAR(20) PRIMARY KEY,
    IDKhachHang VARCHAR(20),
    TenCongTy VARCHAR(100),
    FOREIGN KEY (IDKhachHang) REFERENCES KhachHang(IDKhachHang) ON DELETE CASCADE
);

-- 10. Thẻ Thành Viên
CREATE TABLE IF NOT EXISTS TheThanhVien (
    CCCD_CMND VARCHAR(20),
    MaThe INT, -- MaThe để INT để Backend dễ tăng tự động bằng số
    NgayLapThe DATE,
    NgayHetHan DATE,
    PRIMARY KEY (CCCD_CMND, MaThe),
    FOREIGN KEY (CCCD_CMND) REFERENCES CaNhan(CCCD_CMND) ON DELETE CASCADE,
    CONSTRAINT chk_han_su_dung CHECK (NgayHetHan > NgayLapThe)
);

-- =====================================================
-- PHẦN 4: VẬT PHẨM & LOẠI HÀNG
-- =====================================================

-- 11. Vật Phẩm
CREATE TABLE IF NOT EXISTS VatPham (
    IDVatPham INT AUTO_INCREMENT PRIMARY KEY, -- Riêng Vật phẩm vẫn nên dùng AUTO_INCREMENT cho hiệu năng
    TenVatPham VARCHAR(100),
    SoLuongKhaDung INT DEFAULT 0,
    GiaNiemYet DECIMAL(10, 2),
    CONSTRAINT chk_so_luong_kha_dung CHECK (SoLuongKhaDung >= 0)
);

-- 12. Sách
CREATE TABLE IF NOT EXISTS Sach (
    IDVatPham INT PRIMARY KEY,
    NamXB YEAR,
    TacGia VARCHAR(100),
    NXB VARCHAR(100),
    FOREIGN KEY (IDVatPham) REFERENCES VatPham(IDVatPham) ON DELETE CASCADE
);

-- 13. Báo
CREATE TABLE IF NOT EXISTS Bao (
    IDVatPham INT PRIMARY KEY,
    TapChi VARCHAR(50),
    So INT,
    ToaSoan VARCHAR(50),
    FOREIGN KEY (IDVatPham) REFERENCES VatPham(IDVatPham) ON DELETE CASCADE
);

-- 14. Văn Phòng Phẩm
CREATE TABLE IF NOT EXISTS VanPhongPham (
    IDVatPham INT PRIMARY KEY,
    LoaiHang VARCHAR(50),
    HSX VARCHAR(50),
    FOREIGN KEY (IDVatPham) REFERENCES VatPham(IDVatPham) ON DELETE CASCADE
);

-- 15. Bản Copy (Khóa hợp phần)
CREATE TABLE IF NOT EXISTS BanCopy (
    IDVatPham INT,
    MaSoBanCopy VARCHAR(20), -- Backend tính mã: BC001
    TinhTrang VARCHAR(50),
    PRIMARY KEY (IDVatPham, MaSoBanCopy),
    FOREIGN KEY (IDVatPham) REFERENCES Sach(IDVatPham) ON DELETE CASCADE
);

-- 16. Đợt Giảm Giá
CREATE TABLE IF NOT EXISTS DotGiamGia (
    IDDotGiamGia INT PRIMARY KEY AUTO_INCREMENT,
    IDVatPham INT,
    NgayBatDau DATE,
    NgayKetThuc DATE,
    PhanTramGiamGia INT,
    FOREIGN KEY (IDVatPham) REFERENCES VatPham(IDVatPham) ON DELETE CASCADE,
    CONSTRAINT chk_phan_tram CHECK (PhanTramGiamGia BETWEEN 0 AND 100),
    CONSTRAINT chk_ngay_giam_gia CHECK (NgayKetThuc > NgayBatDau),
    UNIQUE (IDVatPham, NgayBatDau)
);

-- =====================================================
-- PHẦN 5: ĐƠN HÀNG & GIAO HÀNG
-- =====================================================

-- 17. Đơn Mua Hàng
CREATE TABLE IF NOT EXISTS DonMuaHang (
    IDDonMuaHang INT AUTO_INCREMENT PRIMARY KEY,
    LoaiHoaDon VARCHAR(50),
    NgayMua DATE,
    IDKhachHang VARCHAR(20),
    FOREIGN KEY (IDKhachHang) REFERENCES KhachHang(IDKhachHang) ON DELETE CASCADE
);

-- 18. Chi Tiết Đơn Hàng
CREATE TABLE IF NOT EXISTS DonHangChiTiet (
    IDDonMuaHang INT,
    IDVatPham INT,
    SoLuong INT,
    GiaLucMua DECIMAL(10, 2),
    PRIMARY KEY (IDDonMuaHang, IDVatPham),
    FOREIGN KEY (IDDonMuaHang) REFERENCES DonMuaHang(IDDonMuaHang) ON DELETE CASCADE,
    FOREIGN KEY (IDVatPham) REFERENCES VatPham(IDVatPham) ON DELETE RESTRICT,
    CONSTRAINT chk_so_luong_don CHECK (SoLuong > 0)
);

-- 19. Giao Tận Nhà
CREATE TABLE IF NOT EXISTS GiaoTanNha (
    IDDonMuaHang INT PRIMARY KEY,
    DiaChiNhanHang VARCHAR(100),
    TrangThai VARCHAR(50),
    PhiVanChuyen DECIMAL(10, 2),
    IDNhanVien VARCHAR(20),
    FOREIGN KEY (IDDonMuaHang) REFERENCES DonMuaHang(IDDonMuaHang) ON DELETE CASCADE,
    FOREIGN KEY (IDNhanVien) REFERENCES TaiXeChuyenHang(IDNhanVien) ON DELETE SET NULL
);

-- 20. Mua Trực Tiếp
CREATE TABLE IF NOT EXISTS MuaTrucTiep (
    IDDonMuaHang INT PRIMARY KEY,
    IDNhanVien VARCHAR(20),
    FOREIGN KEY (IDDonMuaHang) REFERENCES DonMuaHang(IDDonMuaHang) ON DELETE CASCADE,
    FOREIGN KEY (IDNhanVien) REFERENCES NhanVien(IDNhanVien) ON DELETE SET NULL
);

-- =====================================================
-- PHẦN 6: MƯỢN - THUÊ
-- =====================================================

-- 21. Lần Mượn
-- Backend tính mã: MUO001
CREATE TABLE IF NOT EXISTS LanMuon (
    IDVatPham INT,
    MaSoBanCopy VARCHAR(20),
    CCCD_CMND VARCHAR(20),
    MaThe INT,
    MaDonMuon VARCHAR(20), 
    TinhTrangSauKhiTra VARCHAR(50),
    NgayMuon DATE,
    HanTra DATE,
    PRIMARY KEY (IDVatPham, MaSoBanCopy, CCCD_CMND, MaThe, MaDonMuon),
    FOREIGN KEY (IDVatPham, MaSoBanCopy) REFERENCES BanCopy(IDVatPham, MaSoBanCopy) ON DELETE CASCADE,
    FOREIGN KEY (CCCD_CMND, MaThe) REFERENCES TheThanhVien(CCCD_CMND, MaThe) ON DELETE CASCADE,
    CONSTRAINT chk_han_tra CHECK (HanTra > NgayMuon)
);

-- 22. Lần Thuê
-- Backend tính mã: THU001
CREATE TABLE IF NOT EXISTS LanThue (
    IDKhachHang VARCHAR(20),
    IDVatPham INT,
    MaDonThue VARCHAR(20),
    ThoiHanTra DATE,
    GiaThue DECIMAL(10, 2),
    NgayThue DATE,
    NgayTra DATE,
    SoLuong INT,
    PRIMARY KEY (IDKhachHang, IDVatPham, MaDonThue),
    FOREIGN KEY (IDKhachHang) REFERENCES KhachHang(IDKhachHang) ON DELETE CASCADE,
    FOREIGN KEY (IDVatPham) REFERENCES VatPham(IDVatPham) ON DELETE CASCADE
);

-- =====================================================
-- PHẦN 7: CÔNG VIỆC CỦA ADMIN (TRỎ VỀ QuanTriVien)
-- =====================================================

-- 23. Cập nhật
CREATE TABLE IF NOT EXISTS CapNhat (
    IDNhanVien VARCHAR(20),
    IDVatPham INT,
    NgayCapNhat DATE,
    SoLuong INT,
    PRIMARY KEY (IDNhanVien, IDVatPham, NgayCapNhat),
    FOREIGN KEY (IDNhanVien) REFERENCES QuanTriVien(IDNhanVien) ON DELETE CASCADE,
    FOREIGN KEY (IDVatPham) REFERENCES VatPham(IDVatPham) ON DELETE CASCADE
);

-- 24. Gia Hạn Thẻ
CREATE TABLE IF NOT EXISTS GiaHanThe (
    CCCD_CMND VARCHAR(20),
    MaThe INT,
    IDNhanVien VARCHAR(20),
    NgayGiaHan DATE,
    PRIMARY KEY (CCCD_CMND, MaThe, IDNhanVien),
    FOREIGN KEY (CCCD_CMND, MaThe) REFERENCES TheThanhVien(CCCD_CMND, MaThe) ON DELETE CASCADE,
    FOREIGN KEY (IDNhanVien) REFERENCES QuanTriVien(IDNhanVien) ON DELETE CASCADE
);