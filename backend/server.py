import sys
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass
import re
import json
import sqlite3
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime, date, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "vexe.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database(force_reseed=False):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()

    if force_reseed:
        tables = ['loaixe', 'nhaxe', 'khachhang', 'nguoidung', 'taixe', 'chitiettaixe', 'xe', 'tuyenxe', 'chuyenxe', 'ghengoi', 've', 'vehuy', 'danhgia']
        for t in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {t}")
        conn.commit()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS loaixe (
        LoaixeID TEXT PRIMARY KEY,
        tenLoai TEXT NOT NULL,
        soCho INTEGER NOT NULL,
        giaChuan INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS nhaxe (
        NhaxeID TEXT PRIMARY KEY,
        tenNhaXe TEXT NOT NULL,
        diaChi TEXT,
        soDienThoai TEXT,
        email TEXT,
        nguoiDaiDien TEXT,
        giayPhepKinhDoanh TEXT,
        logo TEXT
    );

    CREATE TABLE IF NOT EXISTS khachhang (
        KhachHangID TEXT PRIMARY KEY,
        hoTen TEXT NOT NULL,
        Email TEXT,
        Ngaysinh TEXT,
        soDienThoai TEXT,
        AnhDaiDienURL TEXT
    );

    CREATE TABLE IF NOT EXISTS nguoidung (
        UserID TEXT PRIMARY KEY,
        TenDangNhap TEXT UNIQUE,
        MatKhau TEXT NOT NULL,
        Email TEXT,
        SoDienThoai TEXT,
        Vaitro TEXT NOT NULL,
        Hovaten TEXT,
        KhachHangID TEXT,
        NhaxeID TEXT,
        TaiXeID TEXT
    );

    CREATE TABLE IF NOT EXISTS taixe (
        TaiXeID TEXT PRIMARY KEY,
        HoTen TEXT NOT NULL,
        SoDienThoai TEXT,
        SoBangLai TEXT,
        Nhaxe TEXT,
        AnhDaiDien TEXT
    );

    CREATE TABLE IF NOT EXISTS chitiettaixe (
        ChiTietID TEXT PRIMARY KEY,
        TaiXe TEXT,
        HoTen TEXT,
        SoDienThoai TEXT,
        SoBangLai TEXT,
        Nhaxe TEXT,
        AnhDaiDien TEXT
    );

    CREATE TABLE IF NOT EXISTS xe (
        XeID TEXT PRIMARY KEY,
        bienSo TEXT NOT NULL,
        Loaixe TEXT,
        Nhaxe TEXT,
        trangThai TEXT DEFAULT 'Hoạt động'
    );

    CREATE TABLE IF NOT EXISTS tuyenxe (
        TuyenxeID TEXT PRIMARY KEY,
        tenTuyen TEXT NOT NULL,
        diemDi TEXT NOT NULL,
        diemDen TEXT NOT NULL,
        diemDung TEXT,
        khoangCach REAL DEFAULT 0,
        thoiGianUocTinh TEXT,
        giaCoBan INTEGER DEFAULT 0,
        Nhaxe TEXT
    );

    CREATE TABLE IF NOT EXISTS chuyenxe (
        ChuyenxeID TEXT PRIMARY KEY,
        Tuyenxe TEXT,
        Xe TEXT,
        TaiXe TEXT,
        ngayKhoiHanh TEXT NOT NULL,
        gioDi TEXT NOT NULL,
        gioDen TEXT,
        giaVe INTEGER NOT NULL,
        trangThai TEXT DEFAULT 'Sắp chạy'
    );

    CREATE TABLE IF NOT EXISTS ghengoi (
        GheID TEXT PRIMARY KEY,
        Chuyenxe TEXT,
        soGhe TEXT NOT NULL,
        trangThai TEXT DEFAULT 'Trống'
    );

    CREATE TABLE IF NOT EXISTS ve (
        VeID TEXT PRIMARY KEY,
        Chuyenxe TEXT,
        KhachHang TEXT,
        soLuongGhe INTEGER NOT NULL,
        danhSachGhe TEXT NOT NULL,
        tongTien INTEGER NOT NULL,
        diemDon TEXT,
        diemTra TEXT,
        ngayDat TEXT,
        trangThai TEXT DEFAULT 'Đã đặt',
        trangThaiThanhToan TEXT DEFAULT 'Chưa thanh toán'
    );

    CREATE TABLE IF NOT EXISTS vehuy (
        HuyID INTEGER PRIMARY KEY AUTOINCREMENT,
        Ve TEXT,
        KhachHang TEXT,
        lyDoHuy TEXT,
        ngayHuy TEXT
    );

    CREATE TABLE IF NOT EXISTS danhgia (
        DanhgiaID INTEGER PRIMARY KEY AUTOINCREMENT,
        Ve TEXT,
        KhachHang TEXT,
        soSao INTEGER DEFAULT 5,
        noiDung TEXT,
        ngayDanhGia TEXT
    );
    """)

    cursor.execute("SELECT COUNT(*) FROM loaixe")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO loaixe VALUES (?, ?, ?, ?)", [
            ('LX01', 'Limousine VIP 34 chỗ', 34, 180000),
            ('LX02', 'Xe Giường Nằm 40 chỗ', 40, 150000),
            ('LX03', 'Xe Ghế Ngồi 29 chỗ', 29, 120000),
            ('LX04', 'Limousine Cung Điện 22 phòng', 22, 250000),
        ])

        cursor.executemany("INSERT INTO nhaxe VALUES (?, ?, ?, ?, ?, ?, ?, ?)", [
            ('NX00001', 'Tràng An Limousine', '107 Bến xe Mỹ Đình, Nam Từ Liêm, Hà Nội', '0988123456', 'trangan@vexeapp.com', 'Nguyễn Văn Hải', 'GP-2024-HN', ''),
            ('NX00002', 'Vân Anh Limousine', '29 Lê Hoàn, Phường Điện Biên, TP. Thanh Hóa', '0905888999', 'vananh@vexeapp.com', 'Trần Văn Trang', 'GP-2023-TH', '')
        ])

        drivers_data = [
            ('TX00001', 'Nguyễn Văn Bình', '0988111222', 'B2-998877', 'NX00001', ''),
            ('TX00002', 'Trần Đình Trọng', '0988333444', 'E-556677', 'NX00001', ''),
            ('TX00003', 'Lê Văn Hùng', '0988555666', 'E-667788', 'NX00001', ''),
            ('TX00004', 'Phạm Quốc Tuấn', '0988777888', 'D-334455', 'NX00001', ''),
            ('TX00005', 'Hoàng Đức Anh', '0988999000', 'E-112233', 'NX00002', ''),
            ('TX00006', 'Đỗ Minh Quân', '0988222333', 'D-445566', 'NX00002', ''),
            ('TX00007', 'Lê Thanh Tùng', '0988444555', 'E-778899', 'NX00002', ''),
            ('TX00008', 'Vũ Hải Nam', '0988666777', 'D-889900', 'NX00002', '')
        ]
        cursor.executemany("INSERT INTO taixe VALUES (?, ?, ?, ?, ?, ?)", drivers_data)

        for d in drivers_data:
            cursor.execute("INSERT INTO chitiettaixe VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (d[0], d[0], d[1], d[2], d[3], d[4], d[5]))

        cursor.executemany("INSERT INTO xe VALUES (?, ?, ?, ?, ?)", [
            ('XE00001', '29B-123.45', 'LX01', 'NX00001', 'Hoạt động'),
            ('XE00002', '29B-567.89', 'LX02', 'NX00001', 'Hoạt động'),
            ('XE00003', '35B-012.34', 'LX01', 'NX00001', 'Hoạt động'),
            ('XE00004', '36B-056.78', 'LX02', 'NX00002', 'Hoạt động'),
            ('XE00005', '29B-333.44', 'LX03', 'NX00001', 'Hoạt động'),
            ('XE00006', '29B-888.99', 'LX04', 'NX00001', 'Hoạt động'),
            ('XE00007', '36B-023.45', 'LX01', 'NX00002', 'Hoạt động'),
            ('XE00008', '36B-067.89', 'LX02', 'NX00002', 'Hoạt động')
        ])

        cursor.executemany("INSERT INTO khachhang VALUES (?, ?, ?, ?, ?, ?)", [
            ('KH00001', 'Lê Hoàng Nam', 'nam.le@vexeapp.com', '2001-05-15', '0912345678', ''),
            ('KH00002', 'Nguyễn Thu Hà', 'ha.nguyen@vexeapp.com', '2002-08-20', '0987654321', ''),
            ('KH00003', 'Trần Quốc Bảo', 'bao.tran@vexeapp.com', '1998-11-10', '0905123987', '')
        ])

        cursor.executemany("INSERT INTO nguoidung VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            ('US00001', 'haivan', '123456', 'trangan@vexeapp.com', '0988123456', 'Nhaxe', 'Tràng An Limousine', None, 'NX00001', None),
            ('US00006', 'trangan', '123456', 'trangan@vexeapp.com', '0988123456', 'Nhaxe', 'Tràng An Limousine', None, 'NX00001', None),
            ('US00002', 'phuongtrang', '123456', 'vananh@vexeapp.com', '0905888999', 'Nhaxe', 'Vân Anh Limousine', None, 'NX00002', None),
            ('US00007', 'vananh', '123456', 'vananh@vexeapp.com', '0905888999', 'Nhaxe', 'Vân Anh Limousine', None, 'NX00002', None),
            ('US00003', '0912345678', '123456', 'nam.le@vexeapp.com', '0912345678', 'KhachHang', 'Lê Hoàng Nam', 'KH00001', None, None),
            ('US00004', '0987654321', '123456', 'ha.nguyen@vexeapp.com', '0987654321', 'KhachHang', 'Nguyễn Thu Hà', 'KH00002', None, None),
            ('US00005', '0905123987', '123456', 'bao.tran@vexeapp.com', '0905123987', 'KhachHang', 'Trần Quốc Bảo', 'KH00003', None, None),
            ('US00010', 'taixe1', '123456', 'binh.nguyen@vexeapp.com', '0988111222', 'TaiXe', 'Nguyễn Văn Bình', None, 'NX00001', 'TX00001'),
            ('US00011', 'taixe2', '123456', 'trong.tran@vexeapp.com', '0988333444', 'TaiXe', 'Trần Đình Trọng', None, 'NX00001', 'TX00002'),
            ('US00012', 'taixe3', '123456', 'hung.le@vexeapp.com', '0988555666', 'TaiXe', 'Lê Văn Hùng', None, 'NX00001', 'TX00003'),
            ('US00013', 'taixe4', '123456', 'tuan.pham@vexeapp.com', '0988777888', 'TaiXe', 'Phạm Quốc Tuấn', None, 'NX00001', 'TX00004'),
            ('US00014', 'taixe5', '123456', 'anh.hoang@vexeapp.com', '0988999000', 'TaiXe', 'Hoàng Đức Anh', None, 'NX00002', 'TX00005'),
            ('US00015', 'taixe6', '123456', 'quan.do@vexeapp.com', '0988222333', 'TaiXe', 'Đỗ Minh Quân', None, 'NX00002', 'TX00006'),
            ('US00016', 'taixe7', '123456', 'tung.le@vexeapp.com', '0988444555', 'TaiXe', 'Lê Thanh Tùng', None, 'NX00002', 'TX00007'),
            ('US00017', 'taixe8', '123456', 'nam.vu@vexeapp.com', '0988666777', 'TaiXe', 'Vũ Hải Nam', None, 'NX00002', 'TX00008')
        ])

        cursor.executemany("INSERT INTO tuyenxe VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            ('TXE00001', 'Hà Nội - Ninh Bình', 'Hà Nội', 'Ninh Bình', 'Phủ Lý, Cao Bồ', 95.0, '1 giờ 30 phút', 150000, 'NX00001'),
            ('TXE00002', 'Hà Nội - Thanh Hóa', 'Hà Nội', 'Thanh Hóa', 'Ninh Bình, Bỉm Sơn', 160.0, '2 giờ 30 phút', 220000, 'NX00002'),
            ('TXE00003', 'Ninh Bình - Thanh Hóa', 'Ninh Bình', 'Thanh Hóa', 'Tam Điệp, Bỉm Sơn', 65.0, '1 giờ 15 phút', 100000, 'NX00002'),
            ('TXE00004', 'Ninh Bình - Hà Nội', 'Ninh Bình', 'Hà Nội', 'Phủ Lý, Bến xe Nước Ngầm', 95.0, '1 giờ 30 phút', 150000, 'NX00001'),
            ('TXE00005', 'Thanh Hóa - Hà Nội', 'Thanh Hóa', 'Hà Nội', 'Bỉm Sơn, Ninh Bình, Bến xe Giáp Bát', 160.0, '2 giờ 30 phút', 220000, 'NX00002'),
            ('TXE00006', 'Thanh Hóa - Ninh Bình', 'Thanh Hóa', 'Ninh Bình', 'Bỉm Sơn, Tam Điệp', 65.0, '1 giờ 15 phút', 100000, 'NX00002')
        ])

        today = date.today()
        today_s = today.isoformat()
        yesterday_s = (today - timedelta(days=1)).isoformat()
        two_days_ago_s = (today - timedelta(days=2)).isoformat()
        tomorrow_s = (today + timedelta(days=1)).isoformat()
        after_s = (today + timedelta(days=2)).isoformat()
        after_3_s = (today + timedelta(days=3)).isoformat()

        trips_data = [
            ('CX00001', 'TXE00001', 'XE00001', 'TX00001', today_s, '06:30', '08:00', 150000, 'Chưa hoàn thành'),
            ('CX00002', 'TXE00001', 'XE00003', 'TX00002', today_s, '08:30', '10:00', 150000, 'Chưa hoàn thành'),
            ('CX00003', 'TXE00001', 'XE00001', 'TX00003', today_s, '10:30', '12:00', 150000, 'Chưa hoàn thành'),
            ('CX00004', 'TXE00001', 'XE00003', 'TX00001', today_s, '13:30', '15:00', 150000, 'Chưa hoàn thành'),
            ('CX00005', 'TXE00001', 'XE00001', 'TX00002', today_s, '15:30', '17:00', 150000, 'Chưa hoàn thành'),
            ('CX00006', 'TXE00001', 'XE00003', 'TX00004', today_s, '18:00', '19:30', 150000, 'Chưa hoàn thành'),
            ('CX00007', 'TXE00002', 'XE00007', 'TX00005', today_s, '07:00', '09:30', 220000, 'Chưa hoàn thành'),
            ('CX00008', 'TXE00002', 'XE00004', 'TX00006', today_s, '09:30', '12:00', 220000, 'Chưa hoàn thành'),
            ('CX00009', 'TXE00002', 'XE00007', 'TX00005', today_s, '14:00', '16:30', 220000, 'Chưa hoàn thành'),
            ('CX00010', 'TXE00002', 'XE00004', 'TX00006', today_s, '17:30', '20:00', 220000, 'Chưa hoàn thành'),
            ('CX00011', 'TXE00003', 'XE00008', 'TX00005', today_s, '08:00', '09:15', 100000, 'Chưa hoàn thành'),
            ('CX00012', 'TXE00003', 'XE00008', 'TX00005', today_s, '15:00', '16:15', 100000, 'Chưa hoàn thành'),
            ('CX00013', 'TXE00004', 'XE00001', 'TX00002', today_s, '07:30', '09:00', 150000, 'Chưa hoàn thành'),
            ('CX00014', 'TXE00004', 'XE00003', 'TX00003', today_s, '13:00', '14:30', 150000, 'Chưa hoàn thành'),
            ('CX00015', 'TXE00005', 'XE00007', 'TX00005', today_s, '06:00', '08:30', 220000, 'Chưa hoàn thành'),
            ('CX00016', 'TXE00005', 'XE00004', 'TX00006', today_s, '13:30', '16:00', 220000, 'Chưa hoàn thành'),
            ('CX00024', 'TXE00006', 'XE00008', 'TX00006', today_s, '09:00', '10:15', 100000, 'Chưa hoàn thành'),
            ('CX00025', 'TXE00006', 'XE00008', 'TX00006', today_s, '16:30', '17:45', 100000, 'Chưa hoàn thành'),
            ('CX00017', 'TXE00001', 'XE00001', 'TX00001', tomorrow_s, '08:00', '09:30', 150000, 'Chưa hoàn thành'),
            ('CX00018', 'TXE00001', 'XE00003', 'TX00002', tomorrow_s, '14:00', '15:30', 150000, 'Chưa hoàn thành'),
            ('CX00019', 'TXE00002', 'XE00007', 'TX00005', tomorrow_s, '08:30', '11:00', 220000, 'Chưa hoàn thành'),
            ('CX00020', 'TXE00002', 'XE00004', 'TX00006', tomorrow_s, '15:00', '17:30', 220000, 'Chưa hoàn thành'),
            ('CX00021', 'TXE00001', 'XE00001', 'TX00003', after_s, '09:30', '11:00', 150000, 'Chưa hoàn thành'),
            ('CX00022', 'TXE00002', 'XE00007', 'TX00005', after_s, '14:00', '16:30', 220000, 'Chưa hoàn thành'),
            ('CX00023', 'TXE00001', 'XE00003', 'TX00001', after_3_s, '08:30', '10:00', 150000, 'Chưa hoàn thành'),
            ('CX00099', 'TXE00001', 'XE00001', 'TX00001', yesterday_s, '08:00', '09:30', 150000, 'Hoàn thành'),
            ('CX00098', 'TXE00002', 'XE00007', 'TX00005', two_days_ago_s, '14:00', '16:30', 220000, 'Hoàn thành')
        ]
        cursor.executemany("INSERT INTO chuyenxe VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", trips_data)

        for tr in trips_data:
            t_id = tr[0]
            for s in range(1, 35):
                seat_num = f"A{s:02d}" if s <= 17 else f"B{s-17:02d}"
                cursor.execute("INSERT INTO ghengoi VALUES (?, ?, ?, ?)", (f"{seat_num}_{t_id}", t_id, seat_num, 'Trống'))

        cursor.executemany("INSERT INTO ve VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            ('VE00001', 'CX00001', 'KH00001', 2, 'A01, A02', 300000, 'Bến xe Mỹ Đình, Hà Nội', 'Bến xe Ninh Bình', today_s + ' 06:00', 'Đã đặt', 'Đã thanh toán'),
            ('VE00002', 'CX00007', 'KH00001', 1, 'A05', 220000, 'Bến xe Giáp Bát, Hà Nội', 'Bến xe phía Bắc Thanh Hóa', today_s + ' 06:30', 'Đã đặt', 'Chưa thanh toán'),
            ('VE00003', 'CX00099', 'KH00001', 1, 'B02', 150000, 'Rạp xiếc Trung ương, Hà Nội', 'Bến xe Ninh Bình', yesterday_s + ' 07:30', 'Đã đi', 'Đã thanh toán'),
            ('VE00004', 'CX00098', 'KH00001', 2, 'A03, A04', 440000, 'Bến xe Nước Ngầm, Hà Nội', 'Bến xe Sầm Sơn, Thanh Hóa', two_days_ago_s + ' 13:00', 'Đã đi', 'Đã thanh toán'),
            ('VE00005', 'CX00002', 'KH00001', 1, 'A08', 150000, 'Bến xe Giáp Bát, Hà Nội', 'Bến xe Ninh Bình', today_s + ' 07:00', 'Đã hủy', 'Đã hoàn tiền'),
            ('VE00006', 'CX00001', 'KH00002', 1, 'A06', 150000, 'Bến xe Mỹ Đình, Hà Nội', 'Bến xe Ninh Bình', today_s + ' 06:10', 'Đã đặt', 'Đã thanh toán'),
            ('VE00007', 'CX00099', 'KH00002', 1, 'A07', 150000, 'Bến xe Nước Ngầm, Hà Nội', 'Bến xe Ninh Bình', yesterday_s + ' 07:45', 'Đã đi', 'Đã thanh toán')
        ])

        cursor.executemany("INSERT INTO vehuy (Ve, KhachHang, lyDoHuy, ngayHuy) VALUES (?, ?, ?, ?)", [
            ('VE00005', 'KH00001', 'Khách bận việc đột xuất cần đổi lịch trình', today_s + ' 07:15')
        ])

        cursor.executemany("INSERT INTO danhgia (Ve, KhachHang, soSao, noiDung, ngayDanhGia) VALUES (?, ?, ?, ?, ?)", [
            ('VE00004', 'KH00001', 5, 'Xe Limousine rất mới, ghế massage êm ái, bác tài chạy cẩn thận đúng giờ. 10 điểm chất lượng!', two_days_ago_s + ' 18:00'),
            ('VE00007', 'KH00002', 5, 'Dịch vụ đón tận nơi rất chu đáo, nước uống và khăn lạnh đầy đủ. Sẽ tiếp tục ủng hộ nhà xe!', yesterday_s + ' 20:00'),
            ('VE00008', 'KH00003', 5, 'Đi tuyến Hà Nội - Thanh Hóa xe chạy cao tốc cực nhanh, chỉ hơn 2 tiếng là tới. Rất hài lòng!', yesterday_s + ' 16:30')
        ])

        cursor.execute("UPDATE ghengoi SET trangThai = 'Đã đặt' WHERE (Chuyenxe = 'CX00001' AND (soGhe = 'A01' OR soGhe = 'A02' OR soGhe = 'A06'))")
        cursor.execute("UPDATE ghengoi SET trangThai = 'Đã đặt' WHERE (Chuyenxe = 'CX00002' AND soGhe = 'A08')")
        cursor.execute("UPDATE ghengoi SET trangThai = 'Đã đặt' WHERE (Chuyenxe = 'CX00007' AND soGhe = 'A05')")
        cursor.execute("UPDATE ghengoi SET trangThai = 'Đã đặt' WHERE (Chuyenxe = 'CX00099' AND (soGhe = 'B02' OR soGhe = 'A07'))")
        cursor.execute("UPDATE ghengoi SET trangThai = 'Đã đặt' WHERE (Chuyenxe = 'CX00098' AND (soGhe = 'A03' OR soGhe = 'A04'))")
        conn.commit()
    conn.close()

def auto_generate_seats_if_needed(conn, trip_id, car_type_id="LX01"):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ghengoi WHERE Chuyenxe = ?", (trip_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute("SELECT soCho FROM loaixe WHERE LoaixeID = ?", (car_type_id,))
        row = cursor.fetchone()
        so_cho = row[0] if row else 34
        for s in range(1, so_cho + 1):
            seat_num = f"A{s:02d}" if s <= so_cho // 2 else f"B{s - so_cho // 2:02d}"
            cursor.execute("INSERT INTO ghengoi VALUES (?, ?, ?, ?)", (f"{seat_num}_{trip_id}", trip_id, seat_num, 'Trống'))
        conn.commit()

def generate_web_dashboard(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM chuyenxe")
    total_trips = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM xe")
    total_vehicles = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM taixe")
    total_drivers = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ve WHERE trangThai != 'Đã hủy'")
    total_tickets = cursor.fetchone()[0]
    cursor.execute("SELECT COALESCE(SUM(tongTien), 0) FROM ve WHERE trangThai != 'Đã hủy'")
    total_revenue = cursor.fetchone()[0]

    cursor.execute("""
    SELECT c.ChuyenxeID, t.tenTuyen, x.bienSo, tx.HoTen, c.ngayKhoiHanh, c.gioDi, c.gioDen, c.giaVe, c.trangThai
    FROM chuyenxe c
    LEFT JOIN tuyenxe t ON c.Tuyenxe = t.TuyenxeID
    LEFT JOIN xe x ON c.Xe = x.XeID
    LEFT JOIN taixe tx ON c.TaiXe = tx.TaiXeID
    ORDER BY c.ngayKhoiHanh DESC, c.gioDi ASC
    """)
    trips = cursor.fetchall()

    cursor.execute("""
    SELECT v.VeID, v.Chuyenxe, kh.hoTen, kh.soDienThoai, v.danhSachGhe, v.soLuongGhe, v.tongTien, v.diemDon, v.diemTra, v.trangThai, v.trangThaiThanhToan
    FROM ve v
    LEFT JOIN khachhang kh ON v.KhachHang = kh.KhachHangID
    ORDER BY v.VeID DESC
    """)
    tickets = cursor.fetchall()

    cursor.execute("""
    SELECT x.XeID, x.bienSo, l.tenLoai, l.soCho, n.tenNhaXe, x.trangThai
    FROM xe x
    LEFT JOIN loaixe l ON x.Loaixe = l.LoaixeID
    LEFT JOIN nhaxe n ON x.Nhaxe = n.NhaxeID
    """)
    vehicles = cursor.fetchall()

    cursor.execute("SELECT * FROM taixe")
    drivers = cursor.fetchall()

    cursor.execute("SELECT * FROM tuyenxe")
    routes = cursor.fetchall()

    cursor.execute("SELECT * FROM nguoidung")
    users = cursor.fetchall()

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VeXeApp - Bảng Điều Hành & Quản Lý Nhà Xe</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: #005B96;
            --primary-gradient: linear-gradient(135deg, #005B96 0%, #00B0FF 100%);
            --secondary-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            --warning-gradient: linear-gradient(135deg, #f2994a 0%, #f2c94c 100%);
            --danger-gradient: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
            --purple-gradient: linear-gradient(135deg, #8e2de2 0%, #4a00e0 100%);
            --bg-color: #f4f7fb;
            --card-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
        }}
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            color: #2c3e50;
        }}
        .navbar-brand {{
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        .gradient-header {{
            background: var(--primary-gradient);
            color: white;
            padding: 30px 0;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0, 91, 150, 0.15);
        }}
        .stat-card {{
            border: none;
            border-radius: 16px;
            padding: 22px;
            box-shadow: var(--card-shadow);
            transition: transform 0.25s ease, box-shadow 0.25s ease;
            background: white;
            position: relative;
            overflow: hidden;
        }}
        .stat-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
        }}
        .stat-icon {{
            width: 50px;
            height: 50px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white;
        }}
        .table-card {{
            border: none;
            border-radius: 16px;
            box-shadow: var(--card-shadow);
            background: white;
            overflow: hidden;
        }}
        .table thead th {{
            background-color: #f8fafc;
            color: #64748b;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid #e2e8f0;
            padding: 14px 18px;
        }}
        .table tbody td {{
            padding: 16px 18px;
            vertical-align: middle;
            font-size: 14px;
        }}
        .badge-status {{
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 12px;
            font-weight: 600;
        }}
        .badge-sap-chay {{ background-color: #e0f2fe; color: #0284c7; }}
        .badge-dang-chay {{ background-color: #fef3c7; color: #d97706; }}
        .badge-hoan-thanh {{ background-color: #dcfce7; color: #16a34a; }}
        .badge-da-huy {{ background-color: #fee2e2; color: #dc2626; }}
        .nav-pills .nav-link {{
            border-radius: 10px;
            font-weight: 600;
            color: #64748b;
            padding: 10px 20px;
            transition: all 0.2s;
        }}
        .nav-pills .nav-link.active {{
            background: var(--primary-gradient);
            color: white;
            box-shadow: 0 4px 12px rgba(0, 91, 150, 0.25);
        }}
        .search-box {{
            border-radius: 10px;
            padding: 10px 16px;
            border: 1px solid #cbd5e1;
        }}
    </style>
</head>
<body>

    <!-- HEADER BANNER -->
    <div class="gradient-header">
        <div class="container">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h2 class="mb-1 fw-bold"><i class="fa-solid fa-bus-simple me-2"></i>VeXeApp - Bảng Quản Trị Hệ Thống</h2>
                    <p class="mb-0 opacity-75">Hệ thống điều hành xe khách & Giám sát đặt vé trực tuyến thời gian thực</p>
                </div>
                <div class="text-end">
                    <span class="badge bg-light text-dark px-3 py-2 fw-semibold"><i class="fa-solid fa-server text-success me-1"></i> API Server: Đang hoạt động (Port 8000)</span>
                    <div class="mt-2 text-white-50 small"><i class="fa-regular fa-clock me-1"></i> {datetime.now().strftime('%H:%M:%S - %d/%m/%Y')}</div>
                </div>
            </div>
        </div>
    </div>

    <div class="container pb-5">

        <!-- STATS ROW -->
        <div class="row g-4 mb-4">
            <div class="col-xl-3 col-md-6">
                <div class="stat-card">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <div class="text-muted small fw-semibold text-uppercase">Chuyến Xe</div>
                            <h3 class="fw-bold mt-1 mb-0">{total_trips}</h3>
                        </div>
                        <div class="stat-icon" style="background: var(--primary-gradient);">
                            <i class="fa-solid fa-route"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-md-6">
                <div class="stat-card">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <div class="text-muted small fw-semibold text-uppercase">Phương Tiện</div>
                            <h3 class="fw-bold mt-1 mb-0">{total_vehicles}</h3>
                        </div>
                        <div class="stat-icon" style="background: var(--secondary-gradient);">
                            <i class="fa-solid fa-van-shuttle"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-md-6">
                <div class="stat-card">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <div class="text-muted small fw-semibold text-uppercase">Tài Xế</div>
                            <h3 class="fw-bold mt-1 mb-0">{total_drivers}</h3>
                        </div>
                        <div class="stat-icon" style="background: var(--warning-gradient);">
                            <i class="fa-solid fa-id-card"></i>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-3 col-md-6">
                <div class="stat-card">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <div class="text-muted small fw-semibold text-uppercase">Vé Đã Đặt / Doanh Thu</div>
                            <h4 class="fw-bold mt-1 mb-0 text-primary">{total_tickets} vé <span class="fs-6 fw-normal text-muted">({total_revenue:,.0f} đ)</span></h4>
                        </div>
                        <div class="stat-icon" style="background: var(--purple-gradient);">
                            <i class="fa-solid fa-ticket"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- NAVIGATION TABS -->
        <div class="d-flex justify-content-between align-items-center mb-4">
            <ul class="nav nav-pills" id="adminTabs" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="trips-tab" data-bs-toggle="pill" data-bs-target="#trips" type="button"><i class="fa-solid fa-bus me-2"></i>Chuyến Xe ({len(trips)})</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="tickets-tab" data-bs-toggle="pill" data-bs-target="#tickets" type="button"><i class="fa-solid fa-receipt me-2"></i>Vé Xe Đã Đặt ({len(tickets)})</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="vehicles-tab" data-bs-toggle="pill" data-bs-target="#vehicles" type="button"><i class="fa-solid fa-car-side me-2"></i>Phương Tiện ({len(vehicles)})</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="drivers-tab" data-bs-toggle="pill" data-bs-target="#drivers" type="button"><i class="fa-solid fa-user-tie me-2"></i>Tài Xế ({len(drivers)})</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="routes-tab" data-bs-toggle="pill" data-bs-target="#routes" type="button"><i class="fa-solid fa-signs-post me-2"></i>Tuyến Đường ({len(routes)})</button>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link" id="users-tab" data-bs-toggle="pill" data-bs-target="#users" type="button"><i class="fa-solid fa-users me-2"></i>Tài Khoản ({len(users)})</button>
                </li>
            </ul>
            <button class="btn btn-outline-primary fw-semibold" onclick="location.reload()"><i class="fa-solid fa-arrows-rotate me-1"></i> Làm mới</button>
        </div>

        <!-- TAB CONTENTS -->
        <div class="tab-content" id="adminTabsContent">

            <!-- TAB 1: CHUYẾN XE -->
            <div class="tab-pane fade show active" id="trips" role="tabpanel">
                <div class="table-card p-3">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead>
                                <tr>
                                    <th>Mã Chuyến</th>
                                    <th>Tuyến Đường</th>
                                    <th>Biển Số Xe</th>
                                    <th>Tài Xế</th>
                                    <th>Ngày Đi</th>
                                    <th>Giờ Chạy</th>
                                    <th>Giá Vé</th>
                                    <th>Trạng Thái</th>
                                </tr>
                            </thead>
                            <tbody>"""

    for r in trips:
        st = r["trangThai"]
        badge_cls = "badge-sap-chay"
        if st == "Đang chạy": badge_cls = "badge-dang-chay"
        elif st == "Hoàn thành" or st == "Đã hoàn thành": badge_cls = "badge-hoan-thanh"
        elif st == "Đã hủy": badge_cls = "badge-da-huy"

        html += f"""
                                <tr>
                                    <td><span class="badge bg-light text-dark border fw-bold">{r["ChuyenxeID"]}</span></td>
                                    <td class="fw-bold text-primary">{r["tenTuyen"] or "N/A"}</td>
                                    <td><span class="badge bg-secondary">{r["bienSo"] or "Chưa gán"}</span></td>
                                    <td>{r["HoTen"] or "Chưa phân"}</td>
                                    <td>{r["ngayKhoiHanh"]}</td>
                                    <td><span class="badge bg-info text-dark">{r["gioDi"]} - {r["gioDen"] or ""}</span></td>
                                    <td class="fw-bold text-danger">{r["giaVe"]:,.0f} đ</td>
                                    <td><span class="badge-status {badge_cls}">{st}</span></td>
                                </tr>"""

    html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB 2: VÉ ĐÃ ĐẶT -->
            <div class="tab-pane fade" id="tickets" role="tabpanel">
                <div class="table-card p-3">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead>
                                <tr>
                                    <th>Mã Vé</th>
                                    <th>Chuyến</th>
                                    <th>Hành Khách</th>
                                    <th>Số Điện Thoại</th>
                                    <th>Ghế Đặt</th>
                                    <th>Tổng Tiền</th>
                                    <th>Điểm Đón / Trả</th>
                                    <th>Thanh Toán</th>
                                    <th>Trạng Thái</th>
                                </tr>
                            </thead>
                            <tbody>"""

    for v in tickets:
        pay_cls = "bg-warning text-dark" if v["trangThaiThanhToan"] == "Chưa thanh toán" else "bg-success"
        html += f"""
                                <tr>
                                    <td class="fw-bold text-primary">{v["VeID"]}</td>
                                    <td><span class="badge bg-light text-dark border">{v["Chuyenxe"]}</span></td>
                                    <td class="fw-bold">{v["hoTen"] or "Khách lẻ"}</td>
                                    <td>{v["soDienThoai"] or "N/A"}</td>
                                    <td><span class="badge bg-primary">{v["danhSachGhe"]}</span></td>
                                    <td class="fw-bold text-danger">{v["tongTien"]:,.0f} đ</td>
                                    <td class="small">{v["diemDon"] or "Điểm hẹn"} &rarr; {v["diemTra"] or "Điểm đến"}</td>
                                    <td><span class="badge {pay_cls}">{v["trangThaiThanhToan"]}</span></td>
                                    <td><span class="badge bg-light text-dark border">{v["trangThai"]}</span></td>
                                </tr>"""

    html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB 3: PHƯƠNG TIỆN -->
            <div class="tab-pane fade" id="vehicles" role="tabpanel">
                <div class="table-card p-3">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead>
                                <tr>
                                    <th>Mã Xe</th>
                                    <th>Biển Số</th>
                                    <th>Loại Xe</th>
                                    <th>Số Chỗ</th>
                                    <th>Nhà Xe Sở Hữu</th>
                                    <th>Tình Trạng</th>
                                </tr>
                            </thead>
                            <tbody>"""

    for x in vehicles:
        html += f"""
                                <tr>
                                    <td class="fw-bold">{x["XeID"]}</td>
                                    <td><span class="badge bg-dark fs-6">{x["bienSo"]}</span></td>
                                    <td class="fw-semibold text-primary">{x["tenLoai"]}</td>
                                    <td>{x["soCho"]} chỗ ngồi</td>
                                    <td>{x["tenNhaXe"] or "Tràng An Limousine"}</td>
                                    <td><span class="badge bg-success">{x["trangThai"]}</span></td>
                                </tr>"""

    html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB 4: TÀI XẾ -->
            <div class="tab-pane fade" id="drivers" role="tabpanel">
                <div class="table-card p-3">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead>
                                <tr>
                                    <th>Mã Tài Xế</th>
                                    <th>Họ Và Tên</th>
                                    <th>Số Điện Thoại</th>
                                    <th>Hạng Bằng Lái</th>
                                    <th>Nhà Xe</th>
                                </tr>
                            </thead>
                            <tbody>"""

    for tx in drivers:
        html += f"""
                                <tr>
                                    <td class="fw-bold">{tx["TaiXeID"]}</td>
                                    <td class="fw-bold text-primary"><i class="fa-solid fa-user-circle me-1 text-muted"></i>{tx["HoTen"]}</td>
                                    <td><a href="tel:{tx["SoDienThoai"]}" class="text-decoration-none">{tx["SoDienThoai"]}</a></td>
                                    <td><span class="badge bg-secondary">{tx["SoBangLai"]}</span></td>
                                    <td>{"Tràng An Limousine" if ("Nhaxe" in tx.keys() and tx["Nhaxe"] == "NX00001") else "Vân Anh Limousine"}</td>
                                </tr>"""

    html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB 5: TUYẾN ĐƯỜNG -->
            <div class="tab-pane fade" id="routes" role="tabpanel">
                <div class="table-card p-3">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead>
                                <tr>
                                    <th>Mã Tuyến</th>
                                    <th>Tên Tuyến Xe</th>
                                    <th>Nhà Xe Vận Hành</th>
                                    <th>Điểm Xuất Phát</th>
                                    <th>Điểm Đích Đến</th>
                                    <th>Cự Ly (km)</th>
                                    <th>Thời Gian Dự Kiến</th>
                                    <th>Giá Cước Cơ Bản</th>
                                </tr>
                            </thead>
                            <tbody>"""

    for r in routes:
        html += f"""
                                <tr>
                                    <td class="fw-bold">{r["TuyenxeID"]}</td>
                                    <td class="fw-bold text-primary">{r["tenTuyen"]}</td>
                                    <td><span class="badge bg-primary">{"Tràng An Limousine" if ("Nhaxe" in r.keys() and r["Nhaxe"] == "NX00001") else "Vân Anh Limousine"}</span></td>
                                    <td><i class="fa-solid fa-location-dot text-danger me-1"></i>{r["diemDi"]}</td>
                                    <td><i class="fa-solid fa-flag-checkered text-success me-1"></i>{r["diemDen"]}</td>
                                    <td>{r["khoangCach"]} km</td>
                                    <td><span class="badge bg-light text-dark border">{r["thoiGianUocTinh"]}</span></td>
                                    <td class="fw-bold text-danger">{r["giaCoBan"]:,.0f} đ</td>
                                </tr>"""

    html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB 6: TÀI KHOẢN -->
            <div class="tab-pane fade" id="users" role="tabpanel">
                <div class="table-card p-3">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle mb-0">
                            <thead>
                                <tr>
                                    <th>User ID</th>
                                    <th>Tên Đăng Nhập / SĐT</th>
                                    <th>Mật Khẩu</th>
                                    <th>Họ Và Tên</th>
                                    <th>Email</th>
                                    <th>Vai Trò</th>
                                </tr>
                            </thead>
                            <tbody>"""

    for u in users:
        role_badge = "bg-primary" if u["Vaitro"] == "Nhaxe" else "bg-info text-dark"
        html += f"""
                                <tr>
                                    <td>{u["UserID"]}</td>
                                    <td class="fw-bold">{u["TenDangNhap"]}</td>
                                    <td><code>{u["MatKhau"]}</code></td>
                                    <td>{u["Hovaten"]}</td>
                                    <td class="small text-muted">{u["Email"] or "N/A"}</td>
                                    <td><span class="badge {role_badge}">{u["Vaitro"]}</span></td>
                                </tr>"""

    html += """
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
    return html

class VeXeApiHandler(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self._send_cors_headers()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html_content, status=200):
        body = html_content.encode('utf-8')
        self.send_response(status)
        self._send_cors_headers()
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _parse_body(self):
        content_len = int(self.headers.get('Content-Length', 0))
        if content_len == 0:
            return {}
        try:
            raw = self.rfile.read(content_len).decode('utf-8')
            return json.loads(raw)
        except Exception:
            return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        qs = parse_qs(parsed.query)
        conn = get_db()
        cursor = conn.cursor()

        try:
            # WEB DASHBOARD (Trang chủ web)
            if path == '' or path == '/admin':
                return self._send_html(generate_web_dashboard(conn))

            # 1. USER AUTH
            elif path == '/api/user-auth':
                cursor.execute("SELECT * FROM nguoidung")
                rows = [dict(r) for r in cursor.fetchall()]
                users = []
                for u in rows:
                    users.append({
                        "UserID": u["UserID"],
                        "TenDangNhap": u["TenDangNhap"],
                        "MatKhau": u["MatKhau"],
                        "Email": u["Email"],
                        "SoDienThoai": u["SoDienThoai"],
                        "Vaitro": u["Vaitro"],
                        "Hovaten": u["Hovaten"],
                        "KhachHang": u["KhachHangID"],
                        "KhachHangID": u["KhachHangID"],
                        "Nhaxe": u["NhaxeID"],
                        "NhaxeID": u["NhaxeID"],
                        "Taixe": u.get("TaiXeID") or u.get("NhaxeID"),
                        "TaiXe": u.get("TaiXeID") or u.get("NhaxeID"),
                        "TaiXeID": u.get("TaiXeID") or u.get("NhaxeID")
                    })
                return self._send_json(users)

            elif path.startswith('/api/user-auth/'):
                uid = path.split('/')[-1]
                cursor.execute("SELECT * FROM nguoidung WHERE UserID = ? OR TenDangNhap = ?", (uid, uid))
                row = cursor.fetchone()
                if row:
                    u = dict(row)
                    u["KhachHang"] = u.get("KhachHangID")
                    u["Nhaxe"] = u.get("NhaxeID")
                    u["Taixe"] = u.get("TaiXeID")
                    u["TaiXe"] = u.get("TaiXeID")
                    return self._send_json(u)
                return self._send_json({}, 404)

            # 2. KHÁCH HÀNG
            elif path == '/api/khachhang':
                cursor.execute("SELECT * FROM khachhang")
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["Hovaten"] = r["hoTen"]
                    d["name"] = r["hoTen"]
                    d["soDienThoai"] = r["soDienThoai"]
                    d["SoDienThoai"] = r["soDienThoai"]
                    d["phone"] = r["soDienThoai"]
                    d["NgayDangKy"] = "2026-01-01"
                    rows.append(d)
                return self._send_json(rows)

            elif path.startswith('/api/khachhang/') and path.endswith('/lich-su-ve'):
                kh_id = path.split('/')[3]
                cursor.execute("SELECT v.*, c.ngayKhoiHanh, c.gioDi, t.tenTuyen, n.tenNhaXe, l.soCho FROM ve v LEFT JOIN chuyenxe c ON v.Chuyenxe = c.ChuyenxeID LEFT JOIN tuyenxe t ON c.Tuyenxe = t.TuyenxeID LEFT JOIN nhaxe n ON t.Nhaxe = n.NhaxeID LEFT JOIN xe x ON c.Xe = x.XeID LEFT JOIN loaixe l ON x.Loaixe = l.LoaixeID WHERE v.KhachHang = ?", (kh_id,))
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["time"] = r["gioDi"]
                    d["date"] = r["ngayKhoiHanh"]
                    d["route"] = r["tenTuyen"] or "Tuyến xe"
                    d["car"] = f"Limousine {r['soCho'] or 34} chỗ"
                    d["seatCount"] = f"{r['soLuongGhe']} chỗ"
                    d["seats"] = r["danhSachGhe"]
                    d["status"] = r["trangThai"]
                    rows.append(d)
                return self._send_json(rows)

            elif path.startswith('/api/khachhang/'):
                kh_id = path.split('/')[-1]
                cursor.execute("SELECT * FROM khachhang WHERE KhachHangID = ? OR soDienThoai = ?", (kh_id, kh_id))
                row = cursor.fetchone()
                if row:
                    d = dict(row)
                    d["Hovaten"] = row["hoTen"]
                    d["name"] = row["hoTen"]
                    d["soDienThoai"] = row["soDienThoai"]
                    d["SoDienThoai"] = row["soDienThoai"]
                    d["phone"] = row["soDienThoai"]
                    d["NgayDangKy"] = "2026-01-01"
                    return self._send_json(d)
                return self._send_json({}, 404)

            # 3. NHÀ XE
            elif path == '/api/nhaxe':
                cursor.execute("SELECT * FROM nhaxe")
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["Tennhaxe"] = r["tenNhaXe"]
                    d["BusName"] = r["tenNhaXe"]
                    d["busName"] = r["tenNhaXe"]
                    d["TenNguoiDaiDien"] = r["nguoiDaiDien"]
                    d["DiaChiTruSo"] = r["diaChi"]
                    d["SoDienThoai"] = r["soDienThoai"]
                    d["AnhDaiDien"] = r["logo"]
                    rows.append(d)
                return self._send_json(rows)

            elif path.startswith('/api/nhaxe/'):
                nx_id = path.split('/')[-1]
                cursor.execute("SELECT * FROM nhaxe WHERE NhaxeID = ?", (nx_id,))
                row = cursor.fetchone()
                if row:
                    d = dict(row)
                    d["Tennhaxe"] = row["tenNhaXe"]
                    d["BusName"] = row["tenNhaXe"]
                    d["busName"] = row["tenNhaXe"]
                    d["TenNguoiDaiDien"] = row["nguoiDaiDien"]
                    d["DiaChiTruSo"] = row["diaChi"]
                    d["SoDienThoai"] = row["soDienThoai"]
                    d["AnhDaiDien"] = row["logo"]
                    return self._send_json(d)
                return self._send_json({}, 404)

            # 4. TÀI XẾ & CHI TIẾT TÀI XẾ
            elif path == '/api/taixe':
                nx_filter = qs.get('Nhaxe', [''])[0] or qs.get('nhaxe', [''])[0] or qs.get('nhaxe_id', [''])[0]
                if nx_filter:
                    cursor.execute("SELECT * FROM taixe WHERE Nhaxe = ?", (nx_filter,))
                else:
                    cursor.execute("SELECT * FROM taixe")
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["TaixeID"] = r["TaiXeID"]
                    d["TaiXeID"] = r["TaiXeID"]
                    d["Taixe"] = r["TaiXeID"]
                    d["TaiXe"] = r["TaiXeID"]
                    d["taixe"] = r["TaiXeID"]
                    d["id"] = r["TaiXeID"]
                    d["HoTen"] = r["HoTen"]
                    d["hoTen"] = r["HoTen"]
                    d["name"] = r["HoTen"]
                    d["SoDienThoai"] = r["SoDienThoai"]
                    d["soDienThoai"] = r["SoDienThoai"]
                    d["phone"] = r["SoDienThoai"]
                    d["SoBangLai"] = r["SoBangLai"]
                    d["soBangLai"] = r["SoBangLai"]
                    d["Nhaxe"] = r["Nhaxe"] if "Nhaxe" in r.keys() else ""
                    d["nhaxe"] = r["Nhaxe"] if "Nhaxe" in r.keys() else ""
                    d["soCCCD"] = "037198001234"
                    d["LoaiBangLai"] = "Hạng D"
                    d["NgayHetHanBangLai"] = "2028-12-31"
                    d["HinhAnhURL"] = r["AnhDaiDien"]
                    rows.append(d)
                return self._send_json(rows)

            elif path.startswith('/api/taixe/'):
                tx_id = path.split('/')[-1]
                cursor.execute("SELECT * FROM taixe WHERE TaiXeID = ?", (tx_id,))
                row = cursor.fetchone()
                if row:
                    d = dict(row)
                    d["TaixeID"] = row["TaiXeID"]
                    d["TaiXeID"] = row["TaiXeID"]
                    d["Taixe"] = row["TaiXeID"]
                    d["TaiXe"] = row["TaiXeID"]
                    d["id"] = row["TaiXeID"]
                    d["HoTen"] = row["HoTen"]
                    d["hoTen"] = row["HoTen"]
                    d["SoDienThoai"] = row["SoDienThoai"]
                    d["soDienThoai"] = row["SoDienThoai"]
                    d["SoBangLai"] = row["SoBangLai"]
                    d["soBangLai"] = row["SoBangLai"]
                    d["soCCCD"] = "037198001234"
                    d["LoaiBangLai"] = "Hạng D"
                    d["NgayHetHanBangLai"] = "2028-12-31"
                    d["HinhAnhURL"] = row["AnhDaiDien"]
                    return self._send_json(d)
                return self._send_json({}, 404)

            elif path == '/api/chitiettaixe':
                nx_filter = qs.get('Nhaxe', [''])[0] or qs.get('nhaxe', [''])[0] or qs.get('nhaxe_id', [''])[0]
                if nx_filter:
                    cursor.execute("SELECT c.*, t.HoTen, t.SoDienThoai, t.SoBangLai, t.AnhDaiDien, n.tenNhaXe FROM chitiettaixe c LEFT JOIN taixe t ON c.TaiXe = t.TaiXeID LEFT JOIN nhaxe n ON c.Nhaxe = n.NhaxeID WHERE c.Nhaxe = ?", (nx_filter,))
                else:
                    cursor.execute("SELECT c.*, t.HoTen, t.SoDienThoai, t.SoBangLai, t.AnhDaiDien, n.tenNhaXe FROM chitiettaixe c LEFT JOIN taixe t ON c.TaiXe = t.TaiXeID LEFT JOIN nhaxe n ON c.Nhaxe = n.NhaxeID")
                rows = []
                for idx, r in enumerate(cursor.fetchall(), start=1):
                    d = dict(r)
                    d["id"] = idx
                    d["ChiTietID"] = r["ChiTietID"]
                    d["Taixe"] = r["TaiXe"]
                    d["TaiXe"] = r["TaiXe"]
                    d["TaiXeID"] = r["TaiXe"]
                    d["taixe"] = r["TaiXe"]
                    d["taiXeID"] = r["TaiXe"]
                    d["HoTen"] = r["HoTen"]
                    d["hoTen"] = r["HoTen"]
                    d["SoDienThoai"] = r["SoDienThoai"]
                    d["soDienThoai"] = r["SoDienThoai"]
                    d["SoBangLai"] = r["SoBangLai"]
                    d["Nhaxe"] = r["Nhaxe"]
                    d["nhaxe"] = r["Nhaxe"]
                    d["Tennhaxe"] = r["tenNhaXe"] or "Tràng An Limousine"
                    d["tennhaxe"] = r["tenNhaXe"] or "Tràng An Limousine"
                    d["NgayBatDau"] = "2024-01-01"
                    d["NgayKetThuc"] = "2026-12-31"
                    d["HinhAnhURL"] = r["AnhDaiDien"]
                    rows.append(d)
                return self._send_json(rows)

            # 5. XE & LOẠI XE
            elif path == '/api/xe':
                cursor.execute("SELECT x.*, l.tenLoai, l.soCho, n.tenNhaXe FROM xe x LEFT JOIN loaixe l ON x.Loaixe = l.LoaixeID LEFT JOIN nhaxe n ON x.Nhaxe = n.NhaxeID")
                rows = []
                for r in cursor.fetchall():
                    status_val = r["trangThai"] or "Đang hoạt động"
                    d = {
                        "XeID": r["XeID"],
                        "id": r["XeID"],
                        "bienSo": r["bienSo"],
                        "BienSoXe": r["bienSo"],
                        "BienSo": r["bienSo"],
                        "plateNumber": r["bienSo"],
                        "trangThai": status_val,
                        "TrangThai": status_val,
                        "status": status_val,
                        "soCho": r["soCho"] or 34,
                        "SoGhe": r["soCho"] or 34,
                        "soGhe": r["soCho"] or 34,
                        "totalSeats": r["soCho"] or 34,
                        "Loaixe": {
                            "LoaixeID": r["Loaixe"],
                            "id": r["Loaixe"],
                            "TenLoai": r["tenLoai"],
                            "tenLoai": r["tenLoai"],
                            "SoCho": r["soCho"] or 34,
                            "soCho": r["soCho"] or 34
                        },
                        "loaiXe": r["Loaixe"],
                        "LoaiXeID": r["Loaixe"],
                        "Nhaxe": r["Nhaxe"],
                        "nhaXe": r["Nhaxe"],
                        "NhaxeID": r["Nhaxe"],
                        "tenNhaXe": r["tenNhaXe"] or "Tràng An Limousine"
                    }
                    rows.append(d)
                return self._send_json(rows)

            elif path.startswith('/api/xe/'):
                xid = path.split('/')[-1]
                cursor.execute("SELECT x.*, l.tenLoai, l.soCho, n.tenNhaXe FROM xe x LEFT JOIN loaixe l ON x.Loaixe = l.LoaixeID LEFT JOIN nhaxe n ON x.Nhaxe = n.NhaxeID WHERE x.XeID = ?", (xid,))
                row = cursor.fetchone()
                if row:
                    status_val = row["trangThai"] or "Đang hoạt động"
                    d = {
                        "XeID": row["XeID"],
                        "id": row["XeID"],
                        "bienSo": row["bienSo"],
                        "BienSoXe": row["bienSo"],
                        "BienSo": row["bienSo"],
                        "plateNumber": row["bienSo"],
                        "trangThai": status_val,
                        "TrangThai": status_val,
                        "status": status_val,
                        "soCho": row["soCho"] or 34,
                        "SoGhe": row["soCho"] or 34,
                        "soGhe": row["soCho"] or 34,
                        "totalSeats": row["soCho"] or 34,
                        "Loaixe": {
                            "LoaixeID": row["Loaixe"],
                            "id": row["Loaixe"],
                            "TenLoai": row["tenLoai"],
                            "tenLoai": row["tenLoai"],
                            "SoCho": row["soCho"] or 34,
                            "soCho": row["soCho"] or 34
                        },
                        "loaiXe": row["Loaixe"],
                        "LoaiXeID": row["Loaixe"],
                        "Nhaxe": row["Nhaxe"],
                        "nhaXe": row["Nhaxe"],
                        "NhaxeID": row["Nhaxe"],
                        "tenNhaXe": row["tenNhaXe"] or "Tràng An Limousine"
                    }
                    return self._send_json(d)
                return self._send_json({}, 404)

            elif path == '/api/loaixe':
                cursor.execute("SELECT * FROM loaixe")
                rows = []
                for r in cursor.fetchall():
                    d = {
                        "LoaixeID": r["LoaixeID"],
                        "id": r["LoaixeID"],
                        "loaixeID": r["LoaixeID"],
                        "tenLoai": r["tenLoai"],
                        "TenLoai": r["tenLoai"],
                        "name": r["tenLoai"],
                        "SoCho": r["soCho"],
                        "soCho": r["soCho"],
                        "seats": r["soCho"],
                        "GiaVe": str(r["giaChuan"] or 150000),
                        "giaVe": str(r["giaChuan"] or 150000),
                        "giaChuan": r["giaChuan"] or 150000,
                        "NgayCapNhatGia": "2026-10-27",
                        "ngayCapNhatGia": "2026-10-27",
                        "SoDoGheNgoiURL": "",
                        "soDoGheNgoiURL": ""
                    }
                    rows.append(d)
                return self._send_json(rows)

            elif path.startswith('/api/loaixe/'):
                lid = path.split('/')[-1]
                cursor.execute("SELECT * FROM loaixe WHERE LoaixeID = ?", (lid,))
                r = cursor.fetchone()
                if r:
                    d = {
                        "LoaixeID": r["LoaixeID"],
                        "id": r["LoaixeID"],
                        "loaixeID": r["LoaixeID"],
                        "tenLoai": r["tenLoai"],
                        "TenLoai": r["tenLoai"],
                        "name": r["tenLoai"],
                        "SoCho": r["soCho"],
                        "soCho": r["soCho"],
                        "seats": r["soCho"],
                        "GiaVe": str(r["giaChuan"] or 150000),
                        "giaVe": str(r["giaChuan"] or 150000),
                        "giaChuan": r["giaChuan"] or 150000,
                        "NgayCapNhatGia": "2026-10-27",
                        "ngayCapNhatGia": "2026-10-27",
                        "SoDoGheNgoiURL": "",
                        "soDoGheNgoiURL": ""
                    }
                    return self._send_json(d)
                return self._send_json({}, 404)

            # 6. TUYẾN XE
            elif path == '/api/tuyenxe':
                cursor.execute("SELECT * FROM tuyenxe")
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["tuyenXeID"] = r["TuyenxeID"]
                    d["TuyenxeID"] = r["TuyenxeID"]
                    d["id"] = r["TuyenxeID"]
                    d["name"] = r["tenTuyen"]
                    d["tenTuyen"] = r["tenTuyen"]
                    d["diemDi"] = r["diemDi"]
                    d["startPoint"] = r["diemDi"]
                    d["diemDen"] = r["diemDen"]
                    d["endPoint"] = r["diemDen"]
                    d["DiemTrungGian"] = r["diemDung"] or ""
                    d["midPoint"] = r["diemDung"] or ""
                    d["QuangDuong"] = f"{r['khoangCach']} km" if r['khoangCach'] else "100 km"
                    d["distance"] = f"{r['khoangCach']} km" if r['khoangCach'] else "100 km"
                    d["ThoiGian"] = r["thoiGianUocTinh"] or "1 giờ 30 phút"
                    d["time"] = r["thoiGianUocTinh"] or "1 giờ 30 phút"
                    d["TrangThai"] = "Đang hoạt động"
                    d["trangThai"] = "Đang hoạt động"
                    d["status"] = "Đang hoạt động"
                    d["nhaXe"] = r["Nhaxe"]
                    d["Nhaxe"] = r["Nhaxe"]
                    d["nhaXeId"] = r["Nhaxe"]
                    rows.append(d)
                return self._send_json(rows)

            # 7. CHUYẾN XE (TRIP)
            elif path == '/api/chuyenxe':
                cursor.execute("SELECT c.*, t.tenTuyen, t.diemDi, t.diemDen, t.thoiGianUocTinh, x.bienSo, x.Loaixe as loaiXeId, l.tenLoai as loaiXeTen, l.soCho, tx.HoTen as tenTaiXe, n.tenNhaXe FROM chuyenxe c LEFT JOIN tuyenxe t ON c.Tuyenxe = t.TuyenxeID LEFT JOIN xe x ON c.Xe = x.XeID LEFT JOIN loaixe l ON x.Loaixe = l.LoaixeID LEFT JOIN taixe tx ON c.TaiXe = tx.TaiXeID LEFT JOIN nhaxe n ON t.Nhaxe = n.NhaxeID ORDER BY c.ngayKhoiHanh DESC, c.gioDi ASC")
                res = []
                for r in cursor.fetchall():
                    item = {
                        "ChuyenXeID": r["ChuyenxeID"],
                        "NgayKhoiHanh": r["ngayKhoiHanh"],
                        "GioDi": r["gioDi"],
                        "GioDen": r["gioDen"],
                        "TrangThai": r["trangThai"] or "Chưa hoàn thành",
                        "Xe": r["Xe"] or r["bienSo"],
                        "TuyenXe": r["Tuyenxe"],
                        "Taixe": r["TaiXe"],
                        "TenTuyen": r["tenTuyen"],
                        "LoaiXe": r["loaiXeTen"] or "Limousine VIP 34 chỗ",
                        "GiaVe": str(r["giaVe"] if r["giaVe"] else 200000),
                        "TenNhaXe": r["tenNhaXe"] or "Tràng An Limousine",
                        "SoChoTrong": r["soCho"] or 34,
                        "ThoiGian": r["thoiGianUocTinh"] or "1 giờ 30 phút",

                        "ChuyenxeID": r["ChuyenxeID"],
                        "id": r["ChuyenxeID"],
                        "Tuyenxe": r["Tuyenxe"],
                        "TuyenxeID": r["Tuyenxe"],
                        "tuyen": r["Tuyenxe"],
                        "tuyenXeName": r["tenTuyen"],
                        "routeName": r["tenTuyen"],
                        "diemDi": r["diemDi"],
                        "diemDen": r["diemDen"],
                        "date": r["ngayKhoiHanh"],
                        "ngayKhoiHanh": r["ngayKhoiHanh"],
                        "time": r["gioDi"],
                        "gioDi": r["gioDi"],
                        "startTime": r["gioDi"],
                        "endTime": r["gioDen"],
                        "gioDen": r["gioDen"],
                        "price": r["giaVe"],
                        "giaVe": r["giaVe"],
                        "status": r["trangThai"] or "Chưa hoàn thành",
                        "trangThai": r["trangThai"] or "Chưa hoàn thành",
                        "carType": r["loaiXeTen"] or "Limousine VIP 34 chỗ",
                        "loaiXe": r["loaiXeTen"] or "Limousine VIP 34 chỗ",
                        "totalSeats": r["soCho"] or 34,
                        "availableSeats": r["soCho"] or 34,
                        "TaiXeID": r["TaiXe"],
                        "TaiXe": r["TaiXe"],
                        "taixe": r["TaiXe"],
                        "taiXeID": r["TaiXe"],
                        "tenTaiXe": r["tenTaiXe"],
                        "TenTaiXe": r["tenTaiXe"],
                        "tenNhaXe": r["tenNhaXe"] or "Tràng An Limousine",
                        "duration": r["thoiGianUocTinh"] or "1 giờ 30 phút",
                        "XeID": r["Xe"],
                        "bienSo": r["bienSo"],
                        "BienSo": r["bienSo"],
                        "bienSoXe": r["bienSo"]
                    }
                    res.append(item)
                return self._send_json(res)

            elif path.startswith('/api/chuyenxe/'):
                cid = path.split('/')[-1]
                cursor.execute("SELECT c.*, t.tenTuyen, t.diemDi, t.diemDen, t.thoiGianUocTinh, x.bienSo, l.tenLoai, l.soCho, tx.HoTen as tenTaiXe, n.tenNhaXe FROM chuyenxe c LEFT JOIN tuyenxe t ON c.Tuyenxe = t.TuyenxeID LEFT JOIN xe x ON c.Xe = x.XeID LEFT JOIN loaixe l ON x.Loaixe = l.LoaixeID LEFT JOIN taixe tx ON c.TaiXe = tx.TaiXeID LEFT JOIN nhaxe n ON t.Nhaxe = n.NhaxeID WHERE c.ChuyenxeID = ?", (cid,))
                r = cursor.fetchone()
                if r:
                    item = {
                        "ChuyenXeID": r["ChuyenxeID"],
                        "ChuyenxeID": r["ChuyenxeID"],
                        "id": r["ChuyenxeID"],
                        "NgayKhoiHanh": r["ngayKhoiHanh"],
                        "ngayKhoiHanh": r["ngayKhoiHanh"],
                        "date": r["ngayKhoiHanh"],
                        "GioDi": r["gioDi"],
                        "gioDi": r["gioDi"],
                        "time": r["gioDi"],
                        "GioDen": r["gioDen"],
                        "gioDen": r["gioDen"],
                        "endTime": r["gioDen"],
                        "TrangThai": r["trangThai"] or "Chưa hoàn thành",
                        "trangThai": r["trangThai"] or "Chưa hoàn thành",
                        "status": r["trangThai"] or "Chưa hoàn thành",
                        "Xe": r["Xe"],
                        "XeID": r["Xe"],
                        "bienSo": r["bienSo"],
                        "TuyenXe": r["Tuyenxe"],
                        "Tuyenxe": r["Tuyenxe"],
                        "Taixe": r["TaiXe"],
                        "TaiXe": r["TaiXe"],
                        "tenTaiXe": r["tenTaiXe"],
                        "TenTuyen": r["tenTuyen"],
                        "tenTuyen": r["tenTuyen"],
                        "LoaiXe": r["tenLoai"] or "Limousine VIP 34 chỗ",
                        "GiaVe": str(r["giaVe"] if r["giaVe"] else 200000),
                        "giaVe": r["giaVe"] if r["giaVe"] else 200000,
                        "TenNhaXe": r["tenNhaXe"] or "Tràng An Limousine",
                        "SoChoTrong": r["soCho"] or 34,
                        "ThoiGian": r["thoiGianUocTinh"] or "1 giờ 30 phút",
                        "TenTaiXe": r["tenTaiXe"],
                        "tenTaiXe": r["tenTaiXe"],
                        "BienSo": r["bienSo"],
                        "bienSo": r["bienSo"],
                        "bienSoXe": r["bienSo"],
                        "diemDi": r["diemDi"],
                        "diemDen": r["diemDen"]
                    }
                    return self._send_json(item)
                return self._send_json({}, 404)

            # 8. GHẾ NGỒI
            elif path == '/api/ghengoi':
                chuyen_xe_id = qs.get('ChuyenXe', [''])[0]
                if chuyen_xe_id:
                    auto_generate_seats_if_needed(conn, chuyen_xe_id)
                    cursor.execute("SELECT * FROM ghengoi WHERE Chuyenxe = ? ORDER BY soGhe", (chuyen_xe_id,))
                else:
                    cursor.execute("SELECT * FROM ghengoi")
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["gheID"] = r["GheID"]
                    d["GheID"] = r["GheID"]
                    d["soGhe"] = r["soGhe"]
                    d["SoGhe"] = r["soGhe"]
                    d["trangThai"] = r["trangThai"]
                    d["TrangThai"] = r["trangThai"]
                    d["status"] = r["trangThai"]
                    d["ChuyenXe"] = r["Chuyenxe"]
                    d["Chuyenxe"] = r["Chuyenxe"]
                    d["chuyenXe"] = r["Chuyenxe"]
                    rows.append(d)
                return self._send_json(rows)

            # 9. VÉ XE
            elif path == '/api/ve':
                kh_id = qs.get('KhachHang', [''])[0]
                status = qs.get('TrangThai', [''])[0]
                cx_id = qs.get('ChuyenXe', [''])[0]
                nx_filter = qs.get('Nhaxe', [''])[0] or qs.get('nhaXeId', [''])[0] or qs.get('nhaxe', [''])[0]

                query = """SELECT v.*, c.ngayKhoiHanh, c.gioDi, t.tenTuyen, t.Nhaxe as nhaXeId, n.tenNhaXe,
                                  k.hoTen as tenKhachHang, k.soDienThoai as sdtKhachHang
                           FROM ve v
                           LEFT JOIN chuyenxe c ON v.Chuyenxe = c.ChuyenxeID
                           LEFT JOIN tuyenxe t ON c.Tuyenxe = t.TuyenxeID
                           LEFT JOIN nhaxe n ON t.Nhaxe = n.NhaxeID
                           LEFT JOIN khachhang k ON v.KhachHang = k.KhachHangID
                           WHERE 1=1"""
                params = []
                if kh_id:
                    query += " AND v.KhachHang = ?"
                    params.append(kh_id)
                if status:
                    if status in ['Đã đặt', 'active']:
                        query += " AND v.trangThai IN ('Đã đặt', 'Đã xác nhận', 'Chờ thanh toán', 'Chờ xác nhận')"
                    else:
                        query += " AND v.trangThai = ?"
                        params.append(status)
                if cx_id:
                    query += " AND v.Chuyenxe = ?"
                    params.append(cx_id)
                if nx_filter:
                    query += " AND t.Nhaxe = ?"
                    params.append(nx_filter)

                cursor.execute(query, params)
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["VeID"] = r["VeID"]
                    d["TenTuyen"] = r["tenTuyen"] or "Tuyến xe"
                    d["tenTuyen"] = r["tenTuyen"] or "Tuyến xe"
                    d["TenNhaXe"] = r["tenNhaXe"] or "Nhà xe"
                    d["tenNhaXe"] = r["tenNhaXe"] or "Nhà xe"
                    d["Nhaxe"] = r["nhaXeId"] or ""
                    d["nhaxe"] = r["nhaXeId"] or ""
                    d["nhaXeId"] = r["nhaXeId"] or ""
                    d["HoTenKhachHang"] = r["tenKhachHang"] or ""
                    d["hoTenKhachHang"] = r["tenKhachHang"] or ""
                    d["SoDienThoaiKhachHang"] = r["sdtKhachHang"] or ""
                    d["soDienThoaiKhachHang"] = r["sdtKhachHang"] or ""
                    d["NgayKhoiHanh"] = r["ngayKhoiHanh"]
                    d["ngayKhoiHanh"] = r["ngayKhoiHanh"]
                    d["GioDi"] = r["gioDi"]
                    d["gioDi"] = r["gioDi"]
                    d["SoLuongGhe"] = r["soLuongGhe"]
                    d["soLuongGhe"] = r["soLuongGhe"]
                    d["DanhSachGhe"] = r["danhSachGhe"]
                    d["danhSachGhe"] = r["danhSachGhe"]
                    d["TongTien"] = float(r["tongTien"] or 0)
                    d["tongTien"] = float(r["tongTien"] or 0)
                    d["TrangThai"] = r["trangThai"]
                    d["trangThai"] = r["trangThai"]
                    d["TrangThaiThanhToan"] = r["trangThaiThanhToan"]
                    d["trangThaiThanhToan"] = r["trangThaiThanhToan"]
                    d["KhachHang"] = r["KhachHang"]
                    d["khachHang"] = r["KhachHang"]
                    d["ChuyenXe"] = r["Chuyenxe"]
                    d["chuyenXe"] = r["Chuyenxe"]
                    d["Chuyenxe"] = r["Chuyenxe"]
                    d["DiemDon"] = r["diemDon"] or ""
                    d["diemDon"] = r["diemDon"] or ""
                    d["DiemTra"] = r["diemTra"] or ""
                    d["diemTra"] = r["diemTra"] or ""
                    rows.append(d)
                return self._send_json(rows)

            elif path == '/api/vehuy':
                kh_id = qs.get('KhachHang', [''])[0]
                query = "SELECT v.*, c.ngayKhoiHanh, c.gioDi, t.tenTuyen, n.tenNhaXe, vh.lyDoHuy, vh.ngayHuy FROM ve v LEFT JOIN chuyenxe c ON v.Chuyenxe = c.ChuyenxeID LEFT JOIN tuyenxe t ON c.Tuyenxe = t.TuyenxeID LEFT JOIN nhaxe n ON t.Nhaxe = n.NhaxeID LEFT JOIN vehuy vh ON v.VeID = vh.Ve WHERE v.trangThai = 'Đã hủy'"
                params = []
                if kh_id:
                    query += " AND v.KhachHang = ?"
                    params.append(kh_id)
                cursor.execute(query, params)
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["VeID"] = r["VeID"]
                    d["VeHuyID"] = r["VeID"]
                    d["TenTuyen"] = r["tenTuyen"] or "Tuyến xe"
                    d["tenTuyen"] = r["tenTuyen"] or "Tuyến xe"
                    d["TenNhaXe"] = r["tenNhaXe"] or "Tràng An Limousine"
                    d["tenNhaXe"] = r["tenNhaXe"] or "Tràng An Limousine"
                    d["NgayKhoiHanh"] = r["ngayKhoiHanh"]
                    d["ngayKhoiHanh"] = r["ngayKhoiHanh"]
                    d["GioDi"] = r["gioDi"]
                    d["gioDi"] = r["gioDi"]
                    d["SoLuongGhe"] = r["soLuongGhe"]
                    d["soLuongGhe"] = r["soLuongGhe"]
                    d["DanhSachGhe"] = r["danhSachGhe"]
                    d["danhSachGhe"] = r["danhSachGhe"]
                    d["TongTien"] = float(r["tongTien"] or 0)
                    d["tongTien"] = float(r["tongTien"] or 0)
                    d["TrangThai"] = r["trangThai"]
                    d["trangThai"] = r["trangThai"]
                    d["TrangThaiThanhToan"] = r["trangThaiThanhToan"]
                    d["trangThaiThanhToan"] = r["trangThaiThanhToan"]
                    d["KhachHang"] = r["KhachHang"]
                    d["khachHang"] = r["KhachHang"]
                    d["ChuyenXe"] = r["Chuyenxe"]
                    d["chuyenXe"] = r["Chuyenxe"]
                    d["Chuyenxe"] = r["Chuyenxe"]
                    rows.append(d)
                return self._send_json(rows)

            # 10. ĐÁNH GIÁ
            elif path == '/api/danhgia':
                cursor.execute("SELECT * FROM danhgia")
                return self._send_json([dict(r) for r in cursor.fetchall()])

            else:
                return self._send_json({"error": "Endpoint not found"}, 404)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return self._send_json({"error": str(e)}, 500)
        finally:
            conn.close()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        data = self._parse_body()
        conn = get_db()
        cursor = conn.cursor()

        try:
            # USER AUTH / REGISTER / LOGIN
            if path == '/api/user-auth':
                if "username" in data and "password" in data:
                    user = data.get("username")
                    pw = data.get("password")
                    cursor.execute("SELECT * FROM nguoidung WHERE (TenDangNhap = ? OR SoDienThoai = ?) AND MatKhau = ?", (user, user, pw))
                    row = cursor.fetchone()
                    if row:
                        u = dict(row)
                        u["KhachHang"] = u.get("KhachHangID")
                        u["Nhaxe"] = u.get("NhaxeID")
                        u["Taixe"] = u.get("TaiXeID")
                        return self._send_json({"status": "success", "user": u, "token": f"mock_token_{row['UserID']}", "username": row["TenDangNhap"]})
                    return self._send_json({"error": "Sai tài khoản hoặc mật khẩu"}, 400)
                else:
                    uid = data.get("UserID") or f"US{int(datetime.now().timestamp()*1000)%1000000:06d}"
                    phone = data.get("SoDienThoai") or data.get("phone") or ""
                    cursor.execute("INSERT OR REPLACE INTO nguoidung (UserID, TenDangNhap, MatKhau, Email, SoDienThoai, Vaitro, Hovaten, KhachHangID, NhaxeID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        uid,
                        data.get("TenDangNhap") or phone or uid,
                        data.get("MatKhau") or data.get("password") or "123456",
                        data.get("Email") or f"user{phone}@vexeapp.com",
                        phone,
                        data.get("Vaitro") or "KhachHang",
                        data.get("Hovaten") or data.get("name") or "",
                        data.get("KhachHangID") or data.get("KhachHang"),
                        data.get("NhaxeID") or data.get("Nhaxe")
                    ))
                    conn.commit()
                    return self._send_json({"status": "success", "UserID": uid}, 201)

            # KHÁCH HÀNG REGISTER / CREATE
            elif path == '/api/khachhang':
                kh_id = data.get("KhachHangID") or f"KH{int(datetime.now().timestamp()*1000)%1000000:06d}"
                cursor.execute("INSERT OR REPLACE INTO khachhang (KhachHangID, hoTen, Email, Ngaysinh, soDienThoai, AnhDaiDienURL) VALUES (?, ?, ?, ?, ?, ?)", (
                    kh_id,
                    data.get("Hovaten") or data.get("hoTen") or data.get("name") or "",
                    data.get("Email") or data.get("email") or "",
                    data.get("Ngaysinh") or data.get("ngaySinh") or "2000-01-01",
                    data.get("soDienThoai") or data.get("SoDienThoai") or data.get("phone") or "",
                    data.get("AnhDaiDienURL") or ""
                ))
                conn.commit()
                return self._send_json({
                    "KhachHangID": kh_id,
                    "Hovaten": data.get("Hovaten") or data.get("hoTen") or "",
                    "hoTen": data.get("Hovaten") or data.get("hoTen") or "",
                    "Email": data.get("Email") or "",
                    "Ngaysinh": data.get("Ngaysinh") or "2000-01-01",
                    "soDienThoai": data.get("soDienThoai") or "",
                    "status": "success"
                }, 201)

            # NHÀ XE REGISTER
            elif path == '/api/nhaxe':
                nx_id = data.get("NhaxeID") or f"NX{int(datetime.now().timestamp()*1000)%1000000:06d}"
                cursor.execute("INSERT OR REPLACE INTO nhaxe (NhaxeID, tenNhaXe, diaChi, soDienThoai, email, nguoiDaiDien, giayPhepKinhDoanh, logo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
                    nx_id,
                    data.get("tenNhaXe") or data.get("Tennhaxe") or "",
                    data.get("diaChi") or data.get("DiaChiTruSo") or "",
                    data.get("soDienThoai") or data.get("SoDienThoai") or "",
                    data.get("email") or data.get("Email") or "",
                    data.get("nguoiDaiDien") or data.get("TenNguoiDaiDien") or "",
                    data.get("giayPhepKinhDoanh") or "",
                    data.get("logo") or data.get("AnhDaiDien") or ""
                ))
                conn.commit()
                return self._send_json({"status": "success", "NhaxeID": nx_id}, 201)

            # ĐẶT VÉ (BOOK TICKET)
            elif path == '/api/dat-ve':
                ve_id = data.get("ve_id") or data.get("VeID") or f"VE{int(datetime.now().timestamp()*1000)%1000000:06d}"
                chuyen_xe_id = data.get("chuyen_xe") or data.get("chuyen_xe_id") or data.get("ChuyenXe") or data.get("Chuyenxe")
                khach_hang_input = data.get("khach_hang") or data.get("so_dien_thoai") or data.get("KhachHang") or ""
                ghe_ids = data.get("danh_sach_ghe") or data.get("ghe_ids") or []
                tong_tien = data.get("tong_tien") or data.get("tongTien") or data.get("TongTien") or 0
                diem_don = data.get("diem_don") or data.get("diemDon") or data.get("DiemDon") or ""
                diem_tra = data.get("diem_tra") or data.get("diemTra") or data.get("DiemTra") or ""

                if isinstance(ghe_ids, str):
                    ghe_ids = [s.strip() for s in ghe_ids.split(",") if s.strip()]

                kh_id = None
                if khach_hang_input.startswith("KH"):
                    cursor.execute("SELECT KhachHangID FROM khachhang WHERE KhachHangID = ?", (khach_hang_input,))
                    r = cursor.fetchone()
                    if r:
                        kh_id = r[0]
                if not kh_id:
                    cursor.execute("SELECT KhachHangID FROM khachhang WHERE soDienThoai = ? OR KhachHangID = ?", (khach_hang_input, khach_hang_input))
                    row = cursor.fetchone()
                    if row:
                        kh_id = row[0]
                    else:
                        kh_id = f"KH{int(datetime.now().timestamp()*1000)%1000000:06d}"
                        cursor.execute("INSERT INTO khachhang (KhachHangID, hoTen, soDienThoai) VALUES (?, ?, ?)",
                                       (kh_id, f"Khách hàng {khach_hang_input}", khach_hang_input))

                danh_sach_ghe_str = ", ".join(ghe_ids)

                cursor.execute("""
                INSERT INTO ve (VeID, Chuyenxe, KhachHang, soLuongGhe, danhSachGhe, tongTien, diemDon, diemTra, ngayDat, trangThai, trangThaiThanhToan)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Chờ thanh toán', 'Chưa thanh toán')
                """, (
                    ve_id, chuyen_xe_id, kh_id, len(ghe_ids), danh_sach_ghe_str,
                    tong_tien, diem_don, diem_tra, datetime.now().strftime("%Y-%m-%d %H:%M")
                ))

                for g in ghe_ids:
                    cursor.execute("UPDATE ghengoi SET trangThai = 'Đã đặt' WHERE Chuyenxe = ? AND soGhe = ?", (chuyen_xe_id, g))

                conn.commit()
                return self._send_json({"status": "success", "message": "Đặt vé thành công!", "VeID": ve_id, "ve_id": ve_id}, 201)

            # HỦY VÉ (CANCEL TICKET)
            elif path == '/api/huy-ve':
                ve_id = data.get("ve_id") or data.get("VeID") or data.get("Ve")
                cursor.execute("SELECT * FROM ve WHERE VeID = ?", (ve_id,))
                ticket = cursor.fetchone()
                if ticket:
                    cursor.execute("UPDATE ve SET trangThai = 'Đã hủy' WHERE VeID = ?", (ve_id,))
                    danh_sach = ticket["danhSachGhe"].split(", ")
                    for s in danh_sach:
                        cursor.execute("UPDATE ghengoi SET trangThai = 'Trống' WHERE Chuyenxe = ? AND soGhe = ?", (ticket["Chuyenxe"], s.strip()))
                    cursor.execute("INSERT INTO vehuy (Ve, KhachHang, lyDoHuy, ngayHuy) VALUES (?, ?, ?, ?)",
                                   (ve_id, ticket["KhachHang"], data.get("lyDoHuy") or data.get("ly_do_huy", "Khách yêu cầu hủy"), datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    return self._send_json({"status": "success", "message": "Hủy vé thành công!"})
                return self._send_json({"error": "Không tìm thấy vé"}, 404)

            # TẠO PHƯƠNG TIỆN
            elif path == '/api/xe':
                xe_id = data.get("XeID") or data.get("id") or f"XE{int(datetime.now().timestamp()*1000)%1000000:06d}"
                plate = data.get("BienSoXe") or data.get("bienSo") or data.get("BienSo") or ""
                loaixe = data.get("Loaixe") or data.get("loaiXe") or data.get("LoaiXeID") or "LX01"
                nhaxe = data.get("Nhaxe") or data.get("nhaXe") or data.get("NhaxeID") or "NX00001"
                status = data.get("TrangThai") or data.get("trangThai") or data.get("status") or "Đang hoạt động"

                cursor.execute("INSERT INTO xe (XeID, bienSo, Loaixe, Nhaxe, trangThai) VALUES (?, ?, ?, ?, ?)",
                               (xe_id, plate, loaixe, nhaxe, status))
                conn.commit()

                cursor.execute("SELECT soCho, tenLoai FROM loaixe WHERE LoaixeID = ?", (loaixe,))
                l_row = cursor.fetchone()
                so_cho = l_row[0] if l_row else 34
                ten_loai = l_row[1] if l_row else "Limousine VIP"

                return self._send_json({
                    "XeID": xe_id,
                    "id": xe_id,
                    "BienSoXe": plate,
                    "bienSo": plate,
                    "TrangThai": status,
                    "trangThai": status,
                    "SoGhe": so_cho,
                    "soCho": so_cho,
                    "Loaixe": {
                        "LoaixeID": loaixe,
                        "TenLoai": ten_loai,
                        "tenLoai": ten_loai,
                        "SoCho": so_cho
                    },
                    "Nhaxe": nhaxe
                }, 201)

            # TẠO TUYẾN XE
            elif path == '/api/tuyenxe':
                txe_id = data.get("TuyenxeID") or data.get("tuyenXeID") or f"TXE{int(datetime.now().timestamp()*1000)%1000000:06d}"
                raw_dist = str(data.get("khoangCach") or data.get("QuangDuong") or "100")
                clean_dist = re.sub(r'[^0-9.]', '', raw_dist.replace(',', '.'))
                khoang_cach = float(clean_dist) if clean_dist else 100.0

                raw_price = str(data.get("giaCoBan") or data.get("giaVe") or "150000")
                clean_price = re.sub(r'[^0-9]', '', raw_price)
                gia_co_ban = int(clean_price) if clean_price else 150000

                cursor.execute("""
                INSERT OR REPLACE INTO tuyenxe (TuyenxeID, tenTuyen, diemDi, diemDen, diemDung, khoangCach, thoiGianUocTinh, giaCoBan, Nhaxe)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    txe_id, data.get("tenTuyen") or data.get("name"),
                    data.get("diemDi") or data.get("startPoint"),
                    data.get("diemDen") or data.get("endPoint"),
                    data.get("diemDung") or data.get("DiemTrungGian", ""),
                    khoang_cach,
                    data.get("thoiGianUocTinh") or data.get("ThoiGian", "1 giờ 30 phút"),
                    gia_co_ban,
                    data.get("Nhaxe") or data.get("nhaXe", "NX00001")
                ))
                conn.commit()
                return self._send_json({"status": "success", "TuyenxeID": txe_id, "tuyenXeID": txe_id}, 201)

            # TẠO CHUYẾN XE
            elif path == '/api/chuyenxe':
                cx_id = data.get("ChuyenXeID") or data.get("ChuyenxeID") or data.get("id") or f"CX{int(datetime.now().timestamp()*1000)%1000000:06d}"
                tuyen_id = data.get("TuyenXe") or data.get("Tuyenxe") or data.get("TuyenxeID")
                xe_id = data.get("Xe") or data.get("XeID")
                taixe_id = data.get("Taixe") or data.get("TaiXe") or data.get("TaiXeID")
                ngay_di = data.get("NgayKhoiHanh") or data.get("ngayKhoiHanh") or date.today().isoformat()
                gio_di = data.get("GioDi") or data.get("gioDi", "08:00")
                gio_den = data.get("GioDen") or data.get("gioDen", "10:30")
                
                raw_price = str(data.get("GiaVe") or data.get("giaVe") or "160000")
                clean_price = re.sub(r'[^0-9]', '', raw_price)
                gia_ve = int(clean_price) if clean_price else 160000
                trang_thai = data.get("TrangThai") or data.get("trangThai", "Chưa hoàn thành")

                cursor.execute("INSERT OR REPLACE INTO chuyenxe (ChuyenxeID, Tuyenxe, Xe, TaiXe, ngayKhoiHanh, gioDi, gioDen, giaVe, trangThai) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                               (cx_id, tuyen_id, xe_id, taixe_id, ngay_di, gio_di, gio_den, gia_ve, trang_thai))
                conn.commit()

                car_type_id = "LX01"
                if xe_id:
                    cursor.execute("SELECT Loaixe FROM xe WHERE XeID = ?", (xe_id,))
                    row_xe = cursor.fetchone()
                    if row_xe and row_xe[0]:
                        car_type_id = row_xe[0]
                auto_generate_seats_if_needed(conn, cx_id, car_type_id)

                trip_obj = {
                    "ChuyenXeID": cx_id,
                    "ChuyenxeID": cx_id,
                    "id": cx_id,
                    "TuyenXe": tuyen_id,
                    "Xe": xe_id,
                    "Taixe": taixe_id,
                    "NgayKhoiHanh": ngay_di,
                    "ngayKhoiHanh": ngay_di,
                    "GioDi": gio_di,
                    "gioDi": gio_di,
                    "GioDen": gio_den,
                    "gioDen": gio_den,
                    "GiaVe": str(gia_ve),
                    "giaVe": gia_ve,
                    "TrangThai": trang_thai,
                    "trangThai": trang_thai
                }
                return self._send_json(trip_obj, 201)

            # TẠO TÀI XẾ
            elif path == '/api/taixe' or path == '/api/chitiettaixe':
                tx_id = data.get("TaiXeID") or data.get("TaixeID") or data.get("TaiXe") or data.get("Taixe") or f"TX{int(datetime.now().timestamp()*1000)%1000000:06d}"
                hoten = data.get("HoTen") or data.get("hoTen") or data.get("name", "")
                sdt = data.get("SoDienThoai") or data.get("soDienThoai") or data.get("phone", "")
                banglai = data.get("SoBangLai") or data.get("soBangLai", "")
                nhaxe = data.get("Nhaxe") or data.get("nhaxe", "NX00001")
                anh = data.get("AnhDaiDien") or data.get("HinhAnhURL", "")

                cursor.execute("INSERT OR REPLACE INTO taixe (TaiXeID, HoTen, SoDienThoai, SoBangLai, Nhaxe, AnhDaiDien) VALUES (?, ?, ?, ?, ?, ?)", (tx_id, hoten, sdt, banglai, nhaxe, anh))
                cursor.execute("INSERT OR REPLACE INTO chitiettaixe (ChiTietID, TaiXe, HoTen, SoDienThoai, SoBangLai, Nhaxe, AnhDaiDien) VALUES (?, ?, ?, ?, ?, ?, ?)", (tx_id, tx_id, hoten, sdt, banglai, nhaxe, anh))
                conn.commit()
                return self._send_json({
                    "TaiXeID": tx_id,
                    "TaixeID": tx_id,
                    "HoTen": hoten,
                    "SoDienThoai": sdt,
                    "SoBangLai": banglai,
                    "soCCCD": "037198001234",
                    "LoaiBangLai": "Hạng D",
                    "NgayHetHanBangLai": "2028-12-31"
                }, 201)

            # TẠO GHẾ NGỒI
            elif path == '/api/ghengoi':
                cx_id = data.get("Chuyenxe") or data.get("ChuyenXe")
                so_ghe = data.get("soGhe") or data.get("SoGhe")
                status = data.get("trangThai") or data.get("TrangThai") or "Trống"
                if "Còn trống" in status:
                    status = "Trống"
                gid = data.get("GheID") or data.get("gheID") or f"{so_ghe}_{cx_id}"
                cursor.execute("INSERT OR REPLACE INTO ghengoi (GheID, Chuyenxe, soGhe, trangThai) VALUES (?, ?, ?, ?)",
                               (gid, cx_id, so_ghe, status))
                conn.commit()
                return self._send_json({"status": "success", "GheID": gid}, 201)

            # GỬI ĐÁNH GIÁ (FEEDBACK)
            elif path == '/api/danhgia':
                cursor.execute("""
                INSERT INTO danhgia (Ve, KhachHang, soSao, noiDung, ngayDanhGia)
                VALUES (?, ?, ?, ?, ?)
                """, (
                    data.get("ve_id") or data.get("Ve"),
                    data.get("khach_hang_id") or data.get("KhachHang"),
                    int(data.get("so_sao") or data.get("soSao", 5)),
                    data.get("noi_dung") or data.get("noiDung", ""),
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                ))
                conn.commit()
                return self._send_json({"status": "success", "message": "Gửi đánh giá thành công!"}, 201)

            # THANH TOÁN VÉ (CUSTOMER MARKS PAID VIA QR)
            elif path == '/api/thanh-toan-ve':
                ve_id = data.get("ve_id") or data.get("VeID") or data.get("Ve")
                if not ve_id:
                    return self._send_json({"status": "error", "message": "Thiếu mã vé"}, 400)
                cursor.execute("UPDATE ve SET trangThai = 'Chờ xác nhận', trangThaiThanhToan = 'Chờ xác nhận' WHERE VeID = ?", (ve_id,))
                conn.commit()
                return self._send_json({"status": "success", "message": "Đã thanh toán, chờ nhà xe xác nhận!", "ve_id": ve_id})

            # XÁC NHẬN VÉ (OPERATOR CONFIRMS TICKET)
            elif path == '/api/xac-nhan-ve':
                ve_id = data.get("ve_id") or data.get("VeID") or data.get("Ve")
                if not ve_id:
                    return self._send_json({"status": "error", "message": "Thiếu mã vé"}, 400)
                cursor.execute("UPDATE ve SET trangThai = 'Đã đặt', trangThaiThanhToan = 'Đã thanh toán' WHERE VeID = ?", (ve_id,))
                conn.commit()
                return self._send_json({"status": "success", "message": "Nhà xe đã xác nhận vé thành công!", "ve_id": ve_id})

            # TẠO MỚI LOẠI XE (CREATE CAR TYPE)
            elif path == '/api/loaixe':
                loaixe_id = data.get("LoaixeID") or data.get("loaixe_id") or f"LX{int(datetime.now().timestamp()*1000)%1000000:06d}"
                ten_loai = data.get("tenLoai") or data.get("TenLoai") or f"Xe {data.get('soCho', 34)} chỗ"
                so_cho = int(data.get("soCho") or data.get("SoCho") or 34)
                gia_chuan = int(data.get("giaChuan") or data.get("GiaChuan") or data.get("giaVe") or data.get("GiaVe") or 150000)
                cursor.execute("INSERT OR REPLACE INTO loaixe (LoaixeID, tenLoai, soCho, giaChuan) VALUES (?, ?, ?, ?)",
                               (loaixe_id, ten_loai, so_cho, gia_chuan))
                conn.commit()
                return self._send_json({
                    "status": "success",
                    "LoaixeID": loaixe_id,
                    "loaixeID": loaixe_id,
                    "id": loaixe_id,
                    "tenLoai": ten_loai,
                    "TenLoai": ten_loai,
                    "soCho": so_cho,
                    "SoCho": so_cho,
                    "giaChuan": gia_chuan,
                    "giaVe": str(gia_chuan),
                    "GiaVe": str(gia_chuan)
                }, 201)

            else:
                return self._send_json({"status": "ok"}, 200)

        finally:
            conn.close()

    def do_PUT(self):
        self.do_PATCH()

    def do_PATCH(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        data = self._parse_body()
        parts = path.split('/')
        conn = get_db()
        cursor = conn.cursor()

        try:
            if len(parts) >= 4 and parts[1] == 'api':
                resource = parts[2]
                res_id = parts[3]

                if resource == 'chuyenxe':
                    for k, v in data.items():
                        if k in ['trangThai', 'TrangThai', 'status']:
                            cursor.execute("UPDATE chuyenxe SET trangThai = ? WHERE ChuyenxeID = ?", (v, res_id))
                        elif k in ['TaiXe', 'TaiXeID', 'Taixe', 'taixe']:
                            cursor.execute("UPDATE chuyenxe SET TaiXe = ? WHERE ChuyenxeID = ?", (v, res_id))
                        elif k in ['Xe', 'XeID']:
                            cursor.execute("UPDATE chuyenxe SET Xe = ? WHERE ChuyenxeID = ?", (v, res_id))
                        elif k in ['Tuyenxe', 'TuyenXe']:
                            cursor.execute("UPDATE chuyenxe SET Tuyenxe = ? WHERE ChuyenxeID = ?", (v, res_id))
                        elif k in ['ngayKhoiHanh', 'NgayKhoiHanh']:
                            cursor.execute("UPDATE chuyenxe SET ngayKhoiHanh = ? WHERE ChuyenxeID = ?", (v, res_id))
                        elif k in ['gioDi', 'GioDi']:
                            cursor.execute("UPDATE chuyenxe SET gioDi = ? WHERE ChuyenxeID = ?", (v, res_id))
                        elif k in ['gioDen', 'GioDen']:
                            cursor.execute("UPDATE chuyenxe SET gioDen = ? WHERE ChuyenxeID = ?", (v, res_id))
                        elif k in ['giaVe', 'GiaVe']:
                            clean_price = re.sub(r'[^0-9]', '', str(v))
                            cursor.execute("UPDATE chuyenxe SET giaVe = ? WHERE ChuyenxeID = ?", (int(clean_price) if clean_price else 160000, res_id))
                    conn.commit()
                    return self._send_json({"status": "success", "ChuyenxeID": res_id})

                elif resource == 'tuyenxe':
                    for k, v in data.items():
                        if k in ['tenTuyen', 'name', 'TenTuyen']:
                            cursor.execute("UPDATE tuyenxe SET tenTuyen = ? WHERE TuyenxeID = ?", (v, res_id))
                        elif k in ['diemDi', 'startPoint', 'DiemDi']:
                            cursor.execute("UPDATE tuyenxe SET diemDi = ? WHERE TuyenxeID = ?", (v, res_id))
                        elif k in ['diemDen', 'endPoint', 'DiemDen']:
                            cursor.execute("UPDATE tuyenxe SET diemDen = ? WHERE TuyenxeID = ?", (v, res_id))
                        elif k in ['diemDung', 'DiemTrungGian', 'midPoint']:
                            cursor.execute("UPDATE tuyenxe SET diemDung = ? WHERE TuyenxeID = ?", (v, res_id))
                        elif k in ['khoangCach', 'QuangDuong', 'distance']:
                            clean_dist = re.sub(r'[^0-9.]', '', str(v).replace(',', '.'))
                            cursor.execute("UPDATE tuyenxe SET khoangCach = ? WHERE TuyenxeID = ?", (float(clean_dist) if clean_dist else 100.0, res_id))
                        elif k in ['thoiGianUocTinh', 'ThoiGian', 'time']:
                            cursor.execute("UPDATE tuyenxe SET thoiGianUocTinh = ? WHERE TuyenxeID = ?", (str(v), res_id))
                        elif k in ['giaCoBan', 'giaVe', 'price']:
                            clean_price = re.sub(r'[^0-9]', '', str(v))
                            cursor.execute("UPDATE tuyenxe SET giaCoBan = ? WHERE TuyenxeID = ?", (int(clean_price) if clean_price else 150000, res_id))
                        elif k in ['Nhaxe', 'nhaXe']:
                            cursor.execute("UPDATE tuyenxe SET Nhaxe = ? WHERE TuyenxeID = ?", (v, res_id))
                    conn.commit()
                    return self._send_json({"status": "success", "TuyenxeID": res_id})

                elif resource == 'xe':
                    for k, v in data.items():
                        if k in ['trangThai', 'TrangThai', 'status']:
                            cursor.execute("UPDATE xe SET trangThai = ? WHERE XeID = ?", (v, res_id))
                        elif k in ['bienSo', 'BienSoXe', 'BienSo', 'plateNumber']:
                            cursor.execute("UPDATE xe SET bienSo = ? WHERE XeID = ?", (v, res_id))
                        elif k in ['Loaixe', 'loaiXe', 'LoaiXeID']:
                            cursor.execute("UPDATE xe SET Loaixe = ? WHERE XeID = ?", (v, res_id))
                        elif k in ['Nhaxe', 'nhaXe']:
                            cursor.execute("UPDATE xe SET Nhaxe = ? WHERE XeID = ?", (v, res_id))
                    conn.commit()

                    cursor.execute("SELECT x.*, l.tenLoai, l.soCho, n.tenNhaXe FROM xe x LEFT JOIN loaixe l ON x.Loaixe = l.LoaixeID LEFT JOIN nhaxe n ON x.Nhaxe = n.NhaxeID WHERE x.XeID = ?", (res_id,))
                    row = cursor.fetchone()
                    if row:
                        status_val = row["trangThai"] or "Đang hoạt động"
                        return self._send_json({
                            "XeID": row["XeID"],
                            "id": row["XeID"],
                            "BienSoXe": row["bienSo"],
                            "bienSo": row["bienSo"],
                            "TrangThai": status_val,
                            "trangThai": status_val,
                            "SoGhe": row["soCho"] or 34,
                            "soCho": row["soCho"] or 34,
                            "Loaixe": {
                                "LoaixeID": row["Loaixe"],
                                "TenLoai": row["tenLoai"],
                                "tenLoai": row["tenLoai"],
                                "SoCho": row["soCho"] or 34
                            },
                            "Nhaxe": row["Nhaxe"]
                        })
                    return self._send_json({"status": "success"})

                elif resource == 'khachhang':
                    if "Hovaten" in data or "hoTen" in data or "name" in data:
                        cursor.execute("UPDATE khachhang SET hoTen = ? WHERE KhachHangID = ?", (data.get("Hovaten") or data.get("hoTen") or data.get("name"), res_id))
                    if "Email" in data or "email" in data:
                        cursor.execute("UPDATE khachhang SET Email = ? WHERE KhachHangID = ?", (data.get("Email") or data.get("email"), res_id))
                    if "Ngaysinh" in data or "ngaySinh" in data:
                        cursor.execute("UPDATE khachhang SET Ngaysinh = ? WHERE KhachHangID = ?", (data.get("Ngaysinh") or data.get("ngaySinh"), res_id))
                    if "soDienThoai" in data or "SoDienThoai" in data:
                        cursor.execute("UPDATE khachhang SET soDienThoai = ? WHERE KhachHangID = ?", (data.get("soDienThoai") or data.get("SoDienThoai"), res_id))
                    if "AnhDaiDienURL" in data:
                        cursor.execute("UPDATE khachhang SET AnhDaiDienURL = ? WHERE KhachHangID = ?", (data.get("AnhDaiDienURL"), res_id))
                    conn.commit()
                    return self._send_json({"status": "success", "KhachHangID": res_id})

                elif resource == 'nhaxe':
                    col_map = {
                        'tenNhaXe': 'tenNhaXe', 'Tennhaxe': 'tenNhaXe', 'busName': 'tenNhaXe',
                        'diaChi': 'diaChi', 'DiaChiTruSo': 'diaChi',
                        'soDienThoai': 'soDienThoai', 'SoDienThoai': 'soDienThoai',
                        'email': 'email', 'Email': 'email',
                        'nguoiDaiDien': 'nguoiDaiDien', 'TenNguoiDaiDien': 'nguoiDaiDien',
                        'logo': 'logo', 'AnhDaiDien': 'logo'
                    }
                    for k, col in col_map.items():
                        if k in data:
                            cursor.execute(f"UPDATE nhaxe SET {col} = ? WHERE NhaxeID = ?", (data[k], res_id))
                    conn.commit()
                    return self._send_json({"status": "success", "NhaxeID": res_id})

                elif resource == 'loaixe':
                    if "tenLoai" in data or "TenLoai" in data or "name" in data:
                        name = data.get("tenLoai") or data.get("TenLoai") or data.get("name")
                        cursor.execute("UPDATE loaixe SET tenLoai = ? WHERE LoaixeID = ?", (name, res_id))
                    if "giaVe" in data or "GiaVe" in data or "giaChuan" in data or "GiaChuan" in data:
                        price = int(data.get("giaVe") or data.get("GiaVe") or data.get("giaChuan") or data.get("GiaChuan"))
                        cursor.execute("UPDATE loaixe SET giaChuan = ? WHERE LoaixeID = ?", (price, res_id))
                    if "soCho" in data or "SoCho" in data:
                        seats = int(data.get("soCho") or data.get("SoCho"))
                        cursor.execute("UPDATE loaixe SET soCho = ? WHERE LoaixeID = ?", (seats, res_id))
                    conn.commit()
                    cursor.execute("SELECT * FROM loaixe WHERE LoaixeID = ?", (res_id,))
                    r = cursor.fetchone()
                    if r:
                        return self._send_json({
                            "LoaixeID": r["LoaixeID"],
                            "tenLoai": r["tenLoai"],
                            "SoCho": r["soCho"],
                            "soCho": r["soCho"],
                            "GiaVe": str(r["giaChuan"]),
                            "giaVe": str(r["giaChuan"])
                        })
                    return self._send_json({"status": "success"})

                elif resource == 've':
                    for k, v in data.items():
                        if k in ['trangThai', 'TrangThai']:
                            cursor.execute("UPDATE ve SET trangThai = ? WHERE VeID = ?", (v, res_id))
                        elif k in ['trangThaiThanhToan', 'TrangThaiThanhToan']:
                            cursor.execute("UPDATE ve SET trangThaiThanhToan = ? WHERE VeID = ?", (v, res_id))
                    conn.commit()
                    return self._send_json({"status": "success", "VeID": res_id})

                elif resource == 'ghengoi':
                    if "trangThai" in data or "TrangThai" in data:
                        st = data.get("trangThai") or data.get("TrangThai")
                        if "Còn trống" in st:
                            st = "Trống"
                        cursor.execute("UPDATE ghengoi SET trangThai = ? WHERE GheID = ?", (st, res_id))
                        conn.commit()
                    return self._send_json({"status": "success"})

            return self._send_json({"status": "success"})
        finally:
            conn.close()

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip('/')
        parts = path.split('/')
        conn = get_db()
        cursor = conn.cursor()

        try:
            if len(parts) >= 4 and parts[1] == 'api':
                resource = parts[2]
                res_id = parts[3]
                table_map = {
                    "xe": ("xe", "XeID"),
                    "tuyenxe": ("tuyenxe", "TuyenxeID"),
                    "taixe": ("taixe", "TaiXeID"),
                    "chuyenxe": ("chuyenxe", "ChuyenxeID"),
                    "khachhang": ("khachhang", "KhachHangID"),
                    "user-auth": ("nguoidung", "UserID"),
                    "ve": ("ve", "VeID"),
                    "loaixe": ("loaixe", "LoaixeID")
                }
                if resource in table_map:
                    tbl, col = table_map[resource]
                    cursor.execute(f"DELETE FROM {tbl} WHERE {col} = ?", (res_id,))
                    conn.commit()
                    return self._send_json({"status": "deleted"})
            return self._send_json({"status": "deleted"})
        finally:
            conn.close()
def run_server(port=8000):
    init_database(force_reseed=False)
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, VeXeApiHandler)
    print("=" * 65)
    print(f"🚀 VEXEAPP BACKEND SERVER & WEB DASHBOARD ĐÃ KHỞI CHẠY!")
    print(f"🌐 Xem Web Quản Trị trên trình duyệt: http://localhost:{port}/")
    print(f"📱 Đối với Android Emulator: http://10.0.2.2:{port}/")
    print(f"📁 Cơ sở dữ liệu SQLite: {DB_PATH}")
    print("=" * 65)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã tắt Server.")
        httpd.server_close()

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port)
