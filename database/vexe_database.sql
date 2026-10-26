-- ==============================================================================
-- CƠ SỞ DỮ LIỆU QUẢN LÝ & ĐẶT VÉ XE KHÁCH (VeXeApp)
-- Hỗ trợ: MySQL, MariaDB, PostgreSQL
-- ==============================================================================

-- 1. BẢNG LOẠI XE (LOAIXE)
CREATE TABLE IF NOT EXISTS loaixe (
    LoaixeID VARCHAR(20) PRIMARY KEY,
    tenLoai VARCHAR(50) NOT NULL,
    soCho INT NOT NULL,
    giaChuan BIGINT DEFAULT 0
);

-- 2. BẢNG NHÀ XE (NHAXE)
CREATE TABLE IF NOT EXISTS nhaxe (
    NhaxeID VARCHAR(20) PRIMARY KEY,
    tenNhaXe VARCHAR(100) NOT NULL,
    diaChi VARCHAR(255),
    soDienThoai VARCHAR(20),
    email VARCHAR(100),
    nguoiDaiDien VARCHAR(100),
    giayPhepKinhDoanh VARCHAR(50),
    logo TEXT
);

-- 3. BẢNG KHÁCH HÀNG (KHACHHANG)
CREATE TABLE IF NOT EXISTS khachhang (
    KhachHangID VARCHAR(20) PRIMARY KEY,
    hoTen VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    Ngaysinh VARCHAR(20),
    soDienThoai VARCHAR(20),
    AnhDaiDienURL LONGTEXT
);

-- 4. BẢNG NGƯỜI DÙNG & TÀI KHOẢN (NGUOIDUNG / USER_AUTH)
CREATE TABLE IF NOT EXISTS nguoidung (
    UserID VARCHAR(20) PRIMARY KEY,
    TenDangNhap VARCHAR(50) UNIQUE,
    MatKhau VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    SoDienThoai VARCHAR(20),
    Vaitro VARCHAR(20) NOT NULL, -- 'KhachHang', 'Nhaxe', 'TaiXe'
    Hovaten VARCHAR(100),
    KhachHangID VARCHAR(20),
    NhaxeID VARCHAR(20),
    FOREIGN KEY (KhachHangID) REFERENCES khachhang(KhachHangID) ON DELETE SET NULL,
    FOREIGN KEY (NhaxeID) REFERENCES nhaxe(NhaxeID) ON DELETE SET NULL
);

-- 5. BẢNG TÀI XẾ (TAIXE)
CREATE TABLE IF NOT EXISTS taixe (
    TaiXeID VARCHAR(20) PRIMARY KEY,
    HoTen VARCHAR(100) NOT NULL,
    SoDienThoai VARCHAR(20),
    SoBangLai VARCHAR(50),
    Nhaxe VARCHAR(20),
    AnhDaiDien LONGTEXT,
    FOREIGN KEY (Nhaxe) REFERENCES nhaxe(NhaxeID) ON DELETE CASCADE
);

-- 6. BẢNG CHI TIẾT TÀI XẾ (CHITIETTAIXE)
CREATE TABLE IF NOT EXISTS chitiettaixe (
    ChiTietID VARCHAR(20) PRIMARY KEY,
    TaiXe VARCHAR(20),
    HoTen VARCHAR(100),
    SoDienThoai VARCHAR(20),
    SoBangLai VARCHAR(50),
    Nhaxe VARCHAR(20),
    AnhDaiDien LONGTEXT,
    FOREIGN KEY (TaiXe) REFERENCES taixe(TaiXeID) ON DELETE CASCADE,
    FOREIGN KEY (Nhaxe) REFERENCES nhaxe(NhaxeID) ON DELETE CASCADE
);

-- 7. BẢNG XE / PHƯƠNG TIỆN (XE)
CREATE TABLE IF NOT EXISTS xe (
    XeID VARCHAR(20) PRIMARY KEY,
    bienSo VARCHAR(20) NOT NULL,
    Loaixe VARCHAR(20),
    Nhaxe VARCHAR(20),
    trangThai VARCHAR(50) DEFAULT 'Hoạt động',
    FOREIGN KEY (Loaixe) REFERENCES loaixe(LoaixeID) ON DELETE SET NULL,
    FOREIGN KEY (Nhaxe) REFERENCES nhaxe(NhaxeID) ON DELETE CASCADE
);

-- 8. BẢNG TUYẾN XE (TUYENXE)
CREATE TABLE IF NOT EXISTS tuyenxe (
    TuyenxeID VARCHAR(20) PRIMARY KEY,
    tenTuyen VARCHAR(100) NOT NULL,
    diemDi VARCHAR(100) NOT NULL,
    diemDen VARCHAR(100) NOT NULL,
    diemDung TEXT,
    khoangCach FLOAT DEFAULT 0,
    thoiGianUocTinh VARCHAR(50),
    giaCoBan BIGINT DEFAULT 0,
    Nhaxe VARCHAR(20),
    FOREIGN KEY (Nhaxe) REFERENCES nhaxe(NhaxeID) ON DELETE CASCADE
);

-- 9. BẢNG CHUYẾN XE (CHUYENXE)
CREATE TABLE IF NOT EXISTS chuyenxe (
    ChuyenxeID VARCHAR(20) PRIMARY KEY,
    Tuyenxe VARCHAR(20),
    Xe VARCHAR(20),
    TaiXe VARCHAR(20),
    ngayKhoiHanh VARCHAR(20) NOT NULL,
    gioDi VARCHAR(10) NOT NULL,
    gioDen VARCHAR(10),
    giaVe BIGINT NOT NULL,
    trangThai VARCHAR(50) DEFAULT 'Sắp chạy',
    FOREIGN KEY (Tuyenxe) REFERENCES tuyenxe(TuyenxeID) ON DELETE CASCADE,
    FOREIGN KEY (Xe) REFERENCES xe(XeID) ON DELETE SET NULL,
    FOREIGN KEY (TaiXe) REFERENCES taixe(TaiXeID) ON DELETE SET NULL
);

-- 10. BẢNG GHẾ NGỒI (GHENGOI)
CREATE TABLE IF NOT EXISTS ghengoi (
    GheID VARCHAR(50) PRIMARY KEY,
    Chuyenxe VARCHAR(20),
    soGhe VARCHAR(10) NOT NULL,
    trangThai VARCHAR(20) DEFAULT 'Trống',
    FOREIGN KEY (Chuyenxe) REFERENCES chuyenxe(ChuyenxeID) ON DELETE CASCADE
);

-- 11. BẢNG VÉ XE (VE)
CREATE TABLE IF NOT EXISTS ve (
    VeID VARCHAR(50) PRIMARY KEY,
    Chuyenxe VARCHAR(20),
    KhachHang VARCHAR(20),
    soLuongGhe INT NOT NULL,
    danhSachGhe TEXT NOT NULL,
    tongTien BIGINT NOT NULL,
    diemDon TEXT,
    diemTra TEXT,
    ngayDat VARCHAR(30),
    trangThai VARCHAR(30) DEFAULT 'Đã đặt',
    trangThaiThanhToan VARCHAR(30) DEFAULT 'Chưa thanh toán',
    FOREIGN KEY (Chuyenxe) REFERENCES chuyenxe(ChuyenxeID) ON DELETE CASCADE,
    FOREIGN KEY (KhachHang) REFERENCES khachhang(KhachHangID) ON DELETE CASCADE
);

-- 12. BẢNG VÉ HỦY (VEHUY)
CREATE TABLE IF NOT EXISTS vehuy (
    HuyID INT AUTO_INCREMENT PRIMARY KEY,
    Ve VARCHAR(50),
    KhachHang VARCHAR(20),
    lyDoHuy TEXT,
    ngayHuy VARCHAR(30),
    FOREIGN KEY (Ve) REFERENCES ve(VeID) ON DELETE CASCADE
);

-- 13. BẢNG ĐÁNH GIÁ (DANHGIA)
CREATE TABLE IF NOT EXISTS danhgia (
    DanhgiaID INT AUTO_INCREMENT PRIMARY KEY,
    Ve VARCHAR(50),
    KhachHang VARCHAR(20),
    soSao INT DEFAULT 5,
    noiDung TEXT,
    ngayDanhGia VARCHAR(30),
    FOREIGN KEY (Ve) REFERENCES ve(VeID) ON DELETE CASCADE,
    FOREIGN KEY (KhachHang) REFERENCES khachhang(KhachHangID) ON DELETE CASCADE
);

-- ==============================================================================
-- DỮ LIỆU KHỞI TẠO ĐA DẠNG (RICH SEED DATA)
-- ==============================================================================

-- 1. Loại xe
INSERT INTO loaixe (LoaixeID, tenLoai, soCho, giaChuan) VALUES 
('LX01', 'Limousine VIP 34 chỗ', 34, 180000),
('LX02', 'Xe Giường Nằm 40 chỗ', 40, 150000),
('LX03', 'Xe Ghế Ngồi 29 chỗ', 29, 120000),
('LX04', 'Limousine Cung Điện 22 phòng', 22, 250000);

-- 2. Nhà xe
INSERT INTO nhaxe (NhaxeID, tenNhaXe, diaChi, soDienThoai, email, nguoiDaiDien, giayPhepKinhDoanh, logo) VALUES 
('NX00001', 'Hải Vân Limousine', '233 Nguyễn Tri Phương, Thanh Khê, Đà Nẵng', '0905123456', 'haivan@vexeapp.com', 'Nguyễn Văn Hải', 'GP-2024-HV', ''),
('NX00002', 'Phương Trang Bus Lines', '201 Tôn Đức Thắng, Liên Chiểu, Đà Nẵng', '0905888999', 'phuongtrang@vexeapp.com', 'Trần Văn Trang', 'GP-2023-PT', '');

-- 3. Tài xế
INSERT INTO taixe (TaiXeID, HoTen, SoDienThoai, SoBangLai, Nhaxe, AnhDaiDien) VALUES 
('TX00001', 'Nguyễn Văn Bình', '0905111222', 'B2-998877', 'NX00001', ''),
('TX00002', 'Trần Đình Trọng', '0905333444', 'E-556677', 'NX00001', ''),
('TX00003', 'Lê Văn Hùng', '0905555666', 'E-667788', 'NX00001', ''),
('TX00004', 'Phạm Quốc Tuấn', '0905777888', 'D-334455', 'NX00001', ''),
('TX00005', 'Hoàng Đức Anh', '0905999000', 'E-112233', 'NX00001', ''),
('TX00006', 'Đỗ Minh Quân', '0905222333', 'D-445566', 'NX00001', '');

INSERT INTO chitiettaixe (ChiTietID, TaiXe, HoTen, SoDienThoai, SoBangLai, Nhaxe, AnhDaiDien) VALUES 
('TX00001', 'TX00001', 'Nguyễn Văn Bình', '0905111222', 'B2-998877', 'NX00001', ''),
('TX00002', 'TX00002', 'Trần Đình Trọng', '0905333444', 'E-556677', 'NX00001', ''),
('TX00003', 'TX00003', 'Lê Văn Hùng', '0905555666', 'E-667788', 'NX00001', ''),
('TX00004', 'TX00004', 'Phạm Quốc Tuấn', '0905777888', 'D-334455', 'NX00001', ''),
('TX00005', 'TX00005', 'Hoàng Đức Anh', '0905999000', 'E-112233', 'NX00001', ''),
('TX00006', 'TX00006', 'Đỗ Minh Quân', '0905222333', 'D-445566', 'NX00001', '');

-- 4. Xe
INSERT INTO xe (XeID, bienSo, Loaixe, Nhaxe, trangThai) VALUES 
('XE00001', '43B-012.34', 'LX01', 'NX00001', 'Hoạt động'),
('XE00002', '43B-056.78', 'LX02', 'NX00001', 'Hoạt động'),
('XE00003', '43B-088.88', 'LX01', 'NX00001', 'Hoạt động'),
('XE00004', '43B-099.99', 'LX02', 'NX00001', 'Hoạt động'),
('XE00005', '43B-034.56', 'LX03', 'NX00001', 'Hoạt động'),
('XE00006', '43B-077.77', 'LX04', 'NX00001', 'Hoạt động'),
('XE00007', '43B-023.45', 'LX01', 'NX00002', 'Hoạt động'),
('XE00008', '43B-067.89', 'LX02', 'NX00002', 'Hoạt động');

-- 5. Khách hàng
INSERT INTO khachhang (KhachHangID, hoTen, Email, Ngaysinh, soDienThoai, AnhDaiDienURL) VALUES 
('KH00001', 'Lê Hoàng Nam', 'nam.le@vexeapp.com', '2001-05-15', '0912345678', ''),
('KH00002', 'Nguyễn Thu Hà', 'ha.nguyen@vexeapp.com', '2002-08-20', '0987654321', ''),
('KH00003', 'Trần Quốc Bảo', 'bao.tran@vexeapp.com', '1998-11-10', '0905123987', '');

-- 6. Tài khoản người dùng (Mật khẩu: '123456')
INSERT INTO nguoidung (UserID, TenDangNhap, MatKhau, Email, SoDienThoai, Vaitro, Hovaten, KhachHangID, NhaxeID) VALUES 
('US00001', 'haivan', '123456', 'haivan@vexeapp.com', '0905123456', 'Nhaxe', 'Hải Vân Limousine', NULL, 'NX00001'),
('US00002', 'phuongtrang', '123456', 'phuongtrang@vexeapp.com', '0905888999', 'Nhaxe', 'Phương Trang Bus Lines', NULL, 'NX00002'),
('US00003', '0912345678', '123456', 'nam.le@vexeapp.com', '0912345678', 'KhachHang', 'Lê Hoàng Nam', 'KH00001', NULL),
('US00004', '0987654321', '123456', 'ha.nguyen@vexeapp.com', '0987654321', 'KhachHang', 'Nguyễn Thu Hà', 'KH00002', NULL),
('US00005', '0905123987', '123456', 'bao.tran@vexeapp.com', '0905123987', 'KhachHang', 'Trần Quốc Bảo', 'KH00003', NULL);

-- 7. Tuyến xe
INSERT INTO tuyenxe (TuyenxeID, tenTuyen, diemDi, diemDen, diemDung, khoangCach, thoiGianUocTinh, giaCoBan, Nhaxe) VALUES 
('TXE00001', 'Đà Nẵng - Huế', 'Đà Nẵng', 'Huế', 'Lăng Cô, Phú Lộc', 100.5, '2 giờ 15 phút', 160000, 'NX00001'),
('TXE00002', 'Đà Nẵng - Hội An', 'Đà Nẵng', 'Hội An', 'Ngũ Hành Sơn', 30.0, '45 phút', 70000, 'NX00001'),
('TXE00003', 'Đà Nẵng - Quy Nhơn', 'Đà Nẵng', 'Quy Nhơn', 'Tam Kỳ, Quảng Ngãi', 315.0, '6 giờ', 260000, 'NX00001'),
('TXE00004', 'Đà Nẵng - Nha Trang', 'Đà Nẵng', 'Nha Trang', 'Bình Định, Phú Yên', 530.0, '10 giờ', 380000, 'NX00001'),
('TXE00005', 'Huế - Đà Nẵng', 'Huế', 'Đà Nẵng', 'Phú Lộc, Hải Vân', 100.5, '2 giờ 15 phút', 160000, 'NX00001');

-- 8. Chuyến xe
INSERT INTO chuyenxe (ChuyenxeID, Tuyenxe, Xe, TaiXe, ngayKhoiHanh, gioDi, gioDen, giaVe, trangThai) VALUES 
('CX00001', 'TXE00001', 'XE00001', 'TX00001', CURDATE(), '06:30', '08:45', 160000, 'Sắp chạy'),
('CX00002', 'TXE00001', 'XE00003', 'TX00002', CURDATE(), '09:00', '11:15', 160000, 'Sắp chạy'),
('CX00003', 'TXE00001', 'XE00001', 'TX00003', CURDATE(), '13:30', '15:45', 160000, 'Sắp chạy'),
('CX00004', 'TXE00001', 'XE00003', 'TX00001', CURDATE(), '16:30', '18:45', 160000, 'Sắp chạy'),
('CX00005', 'TXE00002', 'XE00005', 'TX00004', CURDATE(), '08:00', '08:45', 70000, 'Sắp chạy'),
('CX00006', 'TXE00002', 'XE00005', 'TX00004', CURDATE(), '14:00', '14:45', 70000, 'Sắp chạy'),
('CX00007', 'TXE00003', 'XE00002', 'TX00005', CURDATE(), '07:00', '13:00', 260000, 'Sắp chạy'),
('CX00008', 'TXE00003', 'XE00004', 'TX00006', CURDATE(), '19:30', '01:30', 260000, 'Sắp chạy'),
('CX00009', 'TXE00004', 'XE00006', 'TX00005', CURDATE(), '18:00', '04:00', 380000, 'Sắp chạy'),
('CX00010', 'TXE00005', 'XE00001', 'TX00002', CURDATE(), '07:30', '09:45', 160000, 'Sắp chạy');
