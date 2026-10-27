-- ==============================================================================
-- CƠ SỞ DỮ LIỆU QUẢN LÝ & ĐẶT VÉ XE KHÁCH (VeXeApp)
-- Tuyến trọng điểm: Hà Nội - Ninh Bình - Thanh Hóa
-- Hỗ trợ: MySQL, MariaDB, PostgreSQL, SQLite
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
    Tuyenxe VARCHAR(20) NOT NULL,
    Xe VARCHAR(20) NOT NULL,
    TaiXe VARCHAR(20),
    ngayKhoiHanh VARCHAR(20) NOT NULL,
    gioDi VARCHAR(20) NOT NULL,
    gioDen VARCHAR(20),
    giaVe BIGINT DEFAULT 0,
    trangThai VARCHAR(50) DEFAULT 'Chưa hoàn thành',
    FOREIGN KEY (Tuyenxe) REFERENCES tuyenxe(TuyenxeID) ON DELETE CASCADE,
    FOREIGN KEY (Xe) REFERENCES xe(XeID) ON DELETE CASCADE,
    FOREIGN KEY (TaiXe) REFERENCES taixe(TaiXeID) ON DELETE SET NULL
);

-- 10. BẢNG GHẾ NGỒI (GHENGOI)
CREATE TABLE IF NOT EXISTS ghengoi (
    GheID VARCHAR(50) PRIMARY KEY,
    Chuyenxe VARCHAR(20) NOT NULL,
    soGhe VARCHAR(10) NOT NULL,
    trangThai VARCHAR(30) DEFAULT 'Trống', -- 'Trống', 'Đang chọn', 'Đã đặt'
    FOREIGN KEY (Chuyenxe) REFERENCES chuyenxe(ChuyenxeID) ON DELETE CASCADE
);

-- 11. BẢNG VÉ XE (VE)
CREATE TABLE IF NOT EXISTS ve (
    VeID VARCHAR(20) PRIMARY KEY,
    Chuyenxe VARCHAR(20) NOT NULL,
    KhachHang VARCHAR(20) NOT NULL,
    soLuongGhe INT DEFAULT 1,
    danhSachGhe VARCHAR(100) NOT NULL,
    tongTien BIGINT NOT NULL,
    diemDon VARCHAR(255),
    diemTra VARCHAR(255),
    ngayDat VARCHAR(30) NOT NULL,
    trangThai VARCHAR(50) DEFAULT 'Đã đặt', -- 'Đã đặt', 'Đã đi', 'Đã hủy'
    trangThaiThanhToan VARCHAR(50) DEFAULT 'Chưa thanh toán', -- 'Đã thanh toán', 'Chưa thanh toán', 'Đã hoàn tiền'
    FOREIGN KEY (Chuyenxe) REFERENCES chuyenxe(ChuyenxeID) ON DELETE CASCADE,
    FOREIGN KEY (KhachHang) REFERENCES khachhang(KhachHangID) ON DELETE CASCADE
);

-- 12. BẢNG VÉ HỦY (VEHUY)
CREATE TABLE IF NOT EXISTS vehuy (
    HuyID INT PRIMARY KEY AUTO_INCREMENT,
    Ve VARCHAR(20) NOT NULL,
    KhachHang VARCHAR(20) NOT NULL,
    lyDoHuy TEXT,
    ngayHuy VARCHAR(30),
    FOREIGN KEY (Ve) REFERENCES ve(VeID) ON DELETE CASCADE,
    FOREIGN KEY (KhachHang) REFERENCES khachhang(KhachHangID) ON DELETE CASCADE
);

-- 13. BẢNG ĐÁNH GIÁ (DANHGIA)
CREATE TABLE IF NOT EXISTS danhgia (
    DanhgiaID INT PRIMARY KEY AUTO_INCREMENT,
    Ve VARCHAR(20),
    KhachHang VARCHAR(20),
    soSao INT DEFAULT 5,
    noiDung TEXT,
    ngayDanhGia VARCHAR(30),
    FOREIGN KEY (Ve) REFERENCES ve(VeID) ON DELETE CASCADE,
    FOREIGN KEY (KhachHang) REFERENCES khachhang(KhachHangID) ON DELETE SET NULL
);

-- ==============================================================================
-- DỮ LIỆU MẪU ĐẦY ĐỦ ĐỂ DEMO THUYẾT TRÌNH & KIỂM THỬ TẤT CẢ CHỨC NĂNG
-- ==============================================================================

-- 1. Loại xe
INSERT INTO loaixe (LoaixeID, tenLoai, soCho, giaChuan) VALUES 
('LX01', 'Limousine VIP 34 chỗ', 34, 180000),
('LX02', 'Xe Giường Nằm 40 chỗ', 40, 150000),
('LX03', 'Xe Ghế Ngồi 29 chỗ', 29, 120000),
('LX04', 'Limousine Cung Điện 22 phòng', 22, 250000);

-- 2. Nhà xe
INSERT INTO nhaxe (NhaxeID, tenNhaXe, diaChi, soDienThoai, email, nguoiDaiDien, giayPhepKinhDoanh, logo) VALUES 
('NX00001', 'Tràng An Limousine', '107 Bến xe Mỹ Đình, Nam Từ Liêm, Hà Nội', '0988123456', 'trangan@vexeapp.com', 'Nguyễn Văn Hải', 'GP-2024-HN', ''),
('NX00002', 'Vân Anh Limousine', '29 Lê Hoàn, Phường Điện Biên, TP. Thanh Hóa', '0905888999', 'vananh@vexeapp.com', 'Trần Văn Trang', 'GP-2023-TH', '');

-- 3. Tài xế
INSERT INTO taixe (TaiXeID, HoTen, SoDienThoai, SoBangLai, Nhaxe, AnhDaiDien) VALUES 
('TX00001', 'Nguyễn Văn Bình', '0988111222', 'B2-998877', 'NX00001', ''),
('TX00002', 'Trần Đình Trọng', '0988333444', 'E-556677', 'NX00001', ''),
('TX00003', 'Lê Văn Hùng', '0988555666', 'E-667788', 'NX00001', ''),
('TX00004', 'Phạm Quốc Tuấn', '0988777888', 'D-334455', 'NX00001', ''),
('TX00005', 'Hoàng Đức Anh', '0988999000', 'E-112233', 'NX00001', ''),
('TX00006', 'Đỗ Minh Quân', '0988222333', 'D-445566', 'NX00001', '');

INSERT INTO chitiettaixe (ChiTietID, TaiXe, HoTen, SoDienThoai, SoBangLai, Nhaxe, AnhDaiDien) VALUES 
('TX00001', 'TX00001', 'Nguyễn Văn Bình', '0988111222', 'B2-998877', 'NX00001', ''),
('TX00002', 'TX00002', 'Trần Đình Trọng', '0988333444', 'E-556677', 'NX00001', ''),
('TX00003', 'TX00003', 'Lê Văn Hùng', '0988555666', 'E-667788', 'NX00001', ''),
('TX00004', 'TX00004', 'Phạm Quốc Tuấn', '0988777888', 'D-334455', 'NX00001', ''),
('TX00005', 'TX00005', 'Hoàng Đức Anh', '0988999000', 'E-112233', 'NX00001', ''),
('TX00006', 'TX00006', 'Đỗ Minh Quân', '0988222333', 'D-445566', 'NX00001', '');

-- 4. Xe
INSERT INTO xe (XeID, bienSo, Loaixe, Nhaxe, trangThai) VALUES 
('XE00001', '29B-123.45', 'LX01', 'NX00001', 'Hoạt động'),
('XE00002', '29B-567.89', 'LX02', 'NX00001', 'Hoạt động'),
('XE00003', '35B-012.34', 'LX01', 'NX00001', 'Hoạt động'),
('XE00004', '36B-056.78', 'LX02', 'NX00001', 'Hoạt động'),
('XE00005', '29B-333.44', 'LX03', 'NX00001', 'Hoạt động'),
('XE00006', '29B-888.99', 'LX04', 'NX00001', 'Hoạt động'),
('XE00007', '36B-023.45', 'LX01', 'NX00002', 'Hoạt động'),
('XE00008', '36B-067.89', 'LX02', 'NX00002', 'Hoạt động');

-- 5. Khách hàng
INSERT INTO khachhang (KhachHangID, hoTen, Email, Ngaysinh, soDienThoai, AnhDaiDienURL) VALUES 
('KH00001', 'Lê Hoàng Nam', 'nam.le@vexeapp.com', '2001-05-15', '0912345678', ''),
('KH00002', 'Nguyễn Thu Hà', 'ha.nguyen@vexeapp.com', '2002-08-20', '0987654321', ''),
('KH00003', 'Trần Quốc Bảo', 'bao.tran@vexeapp.com', '1998-11-10', '0905123987', '');

-- 6. Tài khoản người dùng (Mật khẩu: '123456')
INSERT INTO nguoidung (UserID, TenDangNhap, MatKhau, Email, SoDienThoai, Vaitro, Hovaten, KhachHangID, NhaxeID) VALUES 
('US00001', 'haivan', '123456', 'trangan@vexeapp.com', '0988123456', 'Nhaxe', 'Tràng An Limousine', NULL, 'NX00001'),
('US00006', 'trangan', '123456', 'trangan@vexeapp.com', '0988123456', 'Nhaxe', 'Tràng An Limousine', NULL, 'NX00001'),
('US00002', 'phuongtrang', '123456', 'vananh@vexeapp.com', '0905888999', 'Nhaxe', 'Vân Anh Limousine', NULL, 'NX00002'),
('US00007', 'vananh', '123456', 'vananh@vexeapp.com', '0905888999', 'Nhaxe', 'Vân Anh Limousine', NULL, 'NX00002'),
('US00003', '0912345678', '123456', 'nam.le@vexeapp.com', '0912345678', 'KhachHang', 'Lê Hoàng Nam', 'KH00001', NULL),
('US00004', '0987654321', '123456', 'ha.nguyen@vexeapp.com', '0987654321', 'KhachHang', 'Nguyễn Thu Hà', 'KH00002', NULL),
('US00005', '0905123987', '123456', 'bao.tran@vexeapp.com', '0905123987', 'KhachHang', 'Trần Quốc Bảo', 'KH00003', NULL);

-- 7. Tuyến xe
INSERT INTO tuyenxe (TuyenxeID, tenTuyen, diemDi, diemDen, diemDung, khoangCach, thoiGianUocTinh, giaCoBan, Nhaxe) VALUES 
('TXE00001', 'Hà Nội - Ninh Bình', 'Hà Nội', 'Ninh Bình', 'Phủ Lý, Cao Bồ', 95.0, '1 giờ 30 phút', 150000, 'NX00001'),
('TXE00002', 'Hà Nội - Thanh Hóa', 'Hà Nội', 'Thanh Hóa', 'Ninh Bình, Bỉm Sơn', 160.0, '2 giờ 30 phút', 220000, 'NX00001'),
('TXE00003', 'Ninh Bình - Thanh Hóa', 'Ninh Bình', 'Thanh Hóa', 'Tam Điệp, Bỉm Sơn', 65.0, '1 giờ 15 phút', 100000, 'NX00001'),
('TXE00004', 'Ninh Bình - Hà Nội', 'Ninh Bình', 'Hà Nội', 'Phủ Lý, Bến xe Nước Ngầm', 95.0, '1 giờ 30 phút', 150000, 'NX00001'),
('TXE00005', 'Thanh Hóa - Hà Nội', 'Thanh Hóa', 'Hà Nội', 'Bỉm Sơn, Ninh Bình, Bến xe Giáp Bát', 160.0, '2 giờ 30 phút', 220000, 'NX00001'),
('TXE00006', 'Thanh Hóa - Ninh Bình', 'Thanh Hóa', 'Ninh Bình', 'Bỉm Sơn, Tam Điệp', 65.0, '1 giờ 15 phút', 100000, 'NX00001');

-- 8. Chuyến xe (Dùng hàm CURDATE() cho ngày hôm nay và DATE_ADD cho các ngày tới)
INSERT INTO chuyenxe (ChuyenxeID, Tuyenxe, Xe, TaiXe, ngayKhoiHanh, gioDi, gioDen, giaVe, trangThai) VALUES 
('CX00001', 'TXE00001', 'XE00001', 'TX00001', CURDATE(), '06:30', '08:00', 150000, 'Chưa hoàn thành'),
('CX00002', 'TXE00001', 'XE00003', 'TX00002', CURDATE(), '08:30', '10:00', 150000, 'Chưa hoàn thành'),
('CX00003', 'TXE00001', 'XE00001', 'TX00003', CURDATE(), '10:30', '12:00', 150000, 'Chưa hoàn thành'),
('CX00004', 'TXE00001', 'XE00003', 'TX00001', CURDATE(), '13:30', '15:00', 150000, 'Chưa hoàn thành'),
('CX00005', 'TXE00001', 'XE00001', 'TX00002', CURDATE(), '15:30', '17:00', 150000, 'Chưa hoàn thành'),
('CX00006', 'TXE00001', 'XE00003', 'TX00004', CURDATE(), '18:00', '19:30', 150000, 'Chưa hoàn thành'),
('CX00007', 'TXE00002', 'XE00002', 'TX00005', CURDATE(), '07:00', '09:30', 220000, 'Chưa hoàn thành'),
('CX00008', 'TXE00002', 'XE00004', 'TX00006', CURDATE(), '09:30', '12:00', 220000, 'Chưa hoàn thành'),
('CX00009', 'TXE00002', 'XE00002', 'TX00005', CURDATE(), '14:00', '16:30', 220000, 'Chưa hoàn thành'),
('CX00010', 'TXE00002', 'XE00004', 'TX00006', CURDATE(), '17:30', '20:00', 220000, 'Chưa hoàn thành'),
('CX00011', 'TXE00003', 'XE00005', 'TX00004', CURDATE(), '08:00', '09:15', 100000, 'Chưa hoàn thành'),
('CX00012', 'TXE00003', 'XE00005', 'TX00004', CURDATE(), '15:00', '16:15', 100000, 'Chưa hoàn thành'),
('CX00013', 'TXE00004', 'XE00001', 'TX00002', CURDATE(), '07:30', '09:00', 150000, 'Chưa hoàn thành'),
('CX00014', 'TXE00004', 'XE00003', 'TX00003', CURDATE(), '13:00', '14:30', 150000, 'Chưa hoàn thành'),
('CX00015', 'TXE00005', 'XE00002', 'TX00005', CURDATE(), '06:00', '08:30', 220000, 'Chưa hoàn thành'),
('CX00016', 'TXE00005', 'XE00004', 'TX00006', CURDATE(), '13:30', '16:00', 220000, 'Chưa hoàn thành'),
('CX00017', 'TXE00001', 'XE00001', 'TX00001', DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:00', '09:30', 150000, 'Chưa hoàn thành'),
('CX00018', 'TXE00001', 'XE00003', 'TX00002', DATE_ADD(CURDATE(), INTERVAL 1 DAY), '14:00', '15:30', 150000, 'Chưa hoàn thành'),
('CX00019', 'TXE00002', 'XE00002', 'TX00005', DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:30', '11:00', 220000, 'Chưa hoàn thành'),
('CX00020', 'TXE00002', 'XE00004', 'TX00006', DATE_ADD(CURDATE(), INTERVAL 1 DAY), '15:00', '17:30', 220000, 'Chưa hoàn thành'),
('CX00021', 'TXE00001', 'XE00001', 'TX00003', DATE_ADD(CURDATE(), INTERVAL 2 DAY), '09:30', '11:00', 150000, 'Chưa hoàn thành'),
('CX00022', 'TXE00002', 'XE00002', 'TX00005', DATE_ADD(CURDATE(), INTERVAL 2 DAY), '14:00', '16:30', 220000, 'Chưa hoàn thành'),
('CX00023', 'TXE00001', 'XE00003', 'TX00001', DATE_ADD(CURDATE(), INTERVAL 3 DAY), '08:30', '10:00', 150000, 'Chưa hoàn thành'),
('CX00099', 'TXE00001', 'XE00001', 'TX00001', DATE_SUB(CURDATE(), INTERVAL 1 DAY), '08:00', '09:30', 150000, 'Hoàn thành'),
('CX00098', 'TXE00002', 'XE00002', 'TX00005', DATE_SUB(CURDATE(), INTERVAL 2 DAY), '14:00', '16:30', 220000, 'Hoàn thành');

-- 9. Vé mẫu (Đầy đủ cả 3 trạng thái: Đã đặt, Đã đi, Đã hủy)
INSERT INTO ve (VeID, Chuyenxe, KhachHang, soLuongGhe, danhSachGhe, tongTien, diemDon, diemTra, ngayDat, trangThai, trangThaiThanhToan) VALUES 
('VE00001', 'CX00001', 'KH00001', 2, 'A01, A02', 300000, 'Bến xe Mỹ Đình, Hà Nội', 'Bến xe Ninh Bình', CONCAT(CURDATE(), ' 06:00'), 'Đã đặt', 'Đã thanh toán'),
('VE00002', 'CX00007', 'KH00001', 1, 'A05', 220000, 'Bến xe Giáp Bát, Hà Nội', 'Bến xe phía Bắc Thanh Hóa', CONCAT(CURDATE(), ' 06:30'), 'Đã đặt', 'Chưa thanh toán'),
('VE00003', 'CX00099', 'KH00001', 1, 'B02', 150000, 'Rạp xiếc Trung ương, Hà Nội', 'Bến xe Ninh Bình', CONCAT(DATE_SUB(CURDATE(), INTERVAL 1 DAY), ' 07:30'), 'Đã đi', 'Đã thanh toán'),
('VE00004', 'CX00098', 'KH00001', 2, 'A03, A04', 440000, 'Bến xe Nước Ngầm, Hà Nội', 'Bến xe Sầm Sơn, Thanh Hóa', CONCAT(DATE_SUB(CURDATE(), INTERVAL 2 DAY), ' 13:00'), 'Đã đi', 'Đã thanh toán'),
('VE00005', 'CX00002', 'KH00001', 1, 'A08', 150000, 'Bến xe Giáp Bát, Hà Nội', 'Bến xe Ninh Bình', CONCAT(CURDATE(), ' 07:00'), 'Đã hủy', 'Đã hoàn tiền'),
('VE00006', 'CX00001', 'KH00002', 1, 'A06', 150000, 'Bến xe Mỹ Đình, Hà Nội', 'Bến xe Ninh Bình', CONCAT(CURDATE(), ' 06:10'), 'Đã đặt', 'Đã thanh toán'),
('VE00007', 'CX00099', 'KH00002', 1, 'A07', 150000, 'Bến xe Nước Ngầm, Hà Nội', 'Bến xe Ninh Bình', CONCAT(DATE_SUB(CURDATE(), INTERVAL 1 DAY), ' 07:45'), 'Đã đi', 'Đã thanh toán');

-- 10. Vé hủy
INSERT INTO vehuy (HuyID, Ve, KhachHang, lyDoHuy, ngayHuy) VALUES 
(1, 'VE00005', 'KH00001', 'Khách bận việc đột xuất cần đổi lịch trình', CONCAT(CURDATE(), ' 07:15'));

-- 11. Đánh giá mẫu
INSERT INTO danhgia (DanhgiaID, Ve, KhachHang, soSao, noiDung, ngayDanhGia) VALUES 
(1, 'VE00004', 'KH00001', 5, 'Xe Limousine rất mới, ghế massage êm ái, bác tài chạy cẩn thận đúng giờ. 10 điểm chất lượng!', CONCAT(DATE_SUB(CURDATE(), INTERVAL 2 DAY), ' 18:00')),
(2, 'VE00007', 'KH00002', 5, 'Dịch vụ đón tận nơi rất chu đáo, nước uống và khăn lạnh đầy đủ. Sẽ tiếp tục ủng hộ nhà xe!', CONCAT(DATE_SUB(CURDATE(), INTERVAL 1 DAY), ' 20:00')),
(3, 'VE00008', 'KH00003', 5, 'Đi tuyến Hà Nội - Thanh Hóa xe chạy cao tốc cực nhanh, chỉ hơn 2 tiếng là tới. Rất hài lòng!', CONCAT(DATE_SUB(CURDATE(), INTERVAL 1 DAY), ' 16:30'));
