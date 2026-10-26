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
        NhaxeID TEXT
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
            ('NX00001', 'Hải Vân Limousine', '233 Nguyễn Tri Phương, Thanh Khê, Đà Nẵng', '0905123456', 'haivan@vexeapp.com', 'Nguyễn Văn Hải', 'GP-2024-HV', ''),
            ('NX00002', 'Phương Trang Bus Lines', '201 Tôn Đức Thắng, Liên Chiểu, Đà Nẵng', '0905888999', 'phuongtrang@vexeapp.com', 'Trần Văn Trang', 'GP-2023-PT', '')
        ])

        drivers_data = [
            ('TX00001', 'Nguyễn Văn Bình', '0905111222', 'B2-998877', 'NX00001', ''),
            ('TX00002', 'Trần Đình Trọng', '0905333444', 'E-556677', 'NX00001', ''),
            ('TX00003', 'Lê Văn Hùng', '0905555666', 'E-667788', 'NX00001', ''),
            ('TX00004', 'Phạm Quốc Tuấn', '0905777888', 'D-334455', 'NX00001', ''),
            ('TX00005', 'Hoàng Đức Anh', '0905999000', 'E-112233', 'NX00001', ''),
            ('TX00006', 'Đỗ Minh Quân', '0905222333', 'D-445566', 'NX00001', '')
        ]
        cursor.executemany("INSERT INTO taixe VALUES (?, ?, ?, ?, ?, ?)", drivers_data)

        for d in drivers_data:
            cursor.execute("INSERT INTO chitiettaixe VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (d[0], d[0], d[1], d[2], d[3], d[4], d[5]))

        cursor.executemany("INSERT INTO xe VALUES (?, ?, ?, ?, ?)", [
            ('XE00001', '43B-012.34', 'LX01', 'NX00001', 'Hoạt động'),
            ('XE00002', '43B-056.78', 'LX02', 'NX00001', 'Hoạt động'),
            ('XE00003', '43B-088.88', 'LX01', 'NX00001', 'Hoạt động'),
            ('XE00004', '43B-099.99', 'LX02', 'NX00001', 'Hoạt động'),
            ('XE00005', '43B-034.56', 'LX03', 'NX00001', 'Hoạt động'),
            ('XE00006', '43B-077.77', 'LX04', 'NX00001', 'Hoạt động'),
            ('XE00007', '43B-023.45', 'LX01', 'NX00002', 'Hoạt động'),
            ('XE00008', '43B-067.89', 'LX02', 'NX00002', 'Hoạt động')
        ])

        cursor.executemany("INSERT INTO khachhang VALUES (?, ?, ?, ?, ?, ?)", [
            ('KH00001', 'Lê Hoàng Nam', 'nam.le@vexeapp.com', '2001-05-15', '0912345678', ''),
            ('KH00002', 'Nguyễn Thu Hà', 'ha.nguyen@vexeapp.com', '2002-08-20', '0987654321', ''),
            ('KH00003', 'Trần Quốc Bảo', 'bao.tran@vexeapp.com', '1998-11-10', '0905123987', '')
        ])

        cursor.executemany("INSERT INTO nguoidung VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            ('US00001', 'haivan', '123456', 'haivan@vexeapp.com', '0905123456', 'Nhaxe', 'Hải Vân Limousine', None, 'NX00001'),
            ('US00002', 'phuongtrang', '123456', 'phuongtrang@vexeapp.com', '0905888999', 'Nhaxe', 'Phương Trang Bus Lines', None, 'NX00002'),
            ('US00003', '0912345678', '123456', 'nam.le@vexeapp.com', '0912345678', 'KhachHang', 'Lê Hoàng Nam', 'KH00001', None),
            ('US00004', '0987654321', '123456', 'ha.nguyen@vexeapp.com', '0987654321', 'KhachHang', 'Nguyễn Thu Hà', 'KH00002', None),
            ('US00005', '0905123987', '123456', 'bao.tran@vexeapp.com', '0905123987', 'KhachHang', 'Trần Quốc Bảo', 'KH00003', None)
        ])

        cursor.executemany("INSERT INTO tuyenxe VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            ('TXE00001', 'Đà Nẵng - Huế', 'Đà Nẵng', 'Huế', 'Lăng Cô, Phú Lộc', 100.5, '2 giờ 15 phút', 160000, 'NX00001'),
            ('TXE00002', 'Đà Nẵng - Hội An', 'Đà Nẵng', 'Hội An', 'Ngũ Hành Sơn', 30.0, '45 phút', 70000, 'NX00001'),
            ('TXE00003', 'Đà Nẵng - Quy Nhơn', 'Đà Nẵng', 'Quy Nhơn', 'Tam Kỳ, Quảng Ngãi', 315.0, '6 giờ', 260000, 'NX00001'),
            ('TXE00004', 'Đà Nẵng - Nha Trang', 'Đà Nẵng', 'Nha Trang', 'Bình Định, Phú Yên', 530.0, '10 giờ', 380000, 'NX00001'),
            ('TXE00005', 'Huế - Đà Nẵng', 'Huế', 'Đà Nẵng', 'Phú Lộc, Hải Vân', 100.5, '2 giờ 15 phút', 160000, 'NX00001')
        ])

        today = date.today()
        today_s = today.isoformat()
        tomorrow_s = (today + timedelta(days=1)).isoformat()
        after_s = (today + timedelta(days=2)).isoformat()

        trips_data = [
            ('CX00001', 'TXE00001', 'XE00001', 'TX00001', today_s, '06:30', '08:45', 160000, 'Sắp chạy'),
            ('CX00002', 'TXE00001', 'XE00003', 'TX00002', today_s, '09:00', '11:15', 160000, 'Sắp chạy'),
            ('CX00003', 'TXE00001', 'XE00001', 'TX00003', today_s, '13:30', '15:45', 160000, 'Sắp chạy'),
            ('CX00004', 'TXE00001', 'XE00003', 'TX00001', today_s, '16:30', '18:45', 160000, 'Sắp chạy'),
            ('CX00005', 'TXE00002', 'XE00005', 'TX00004', today_s, '08:00', '08:45', 70000, 'Sắp chạy'),
            ('CX00006', 'TXE00002', 'XE00005', 'TX00004', today_s, '14:00', '14:45', 70000, 'Sắp chạy'),
            ('CX00007', 'TXE00003', 'XE00002', 'TX00005', today_s, '07:00', '13:00', 260000, 'Sắp chạy'),
            ('CX00008', 'TXE00003', 'XE00004', 'TX00006', today_s, '19:30', '01:30', 260000, 'Sắp chạy'),
            ('CX00009', 'TXE00004', 'XE00006', 'TX00005', today_s, '18:00', '04:00', 380000, 'Sắp chạy'),
            ('CX00010', 'TXE00005', 'XE00001', 'TX00002', today_s, '07:30', '09:45', 160000, 'Sắp chạy'),
            ('CX00011', 'TXE00001', 'XE00001', 'TX00001', tomorrow_s, '08:00', '10:15', 160000, 'Sắp chạy'),
            ('CX00012', 'TXE00001', 'XE00002', 'TX00002', tomorrow_s, '14:00', '16:15', 160000, 'Sắp chạy'),
            ('CX00013', 'TXE00003', 'XE00004', 'TX00005', tomorrow_s, '07:30', '13:30', 260000, 'Sắp chạy'),
            ('CX00014', 'TXE00001', 'XE00003', 'TX00003', after_s, '09:30', '11:45', 160000, 'Sắp chạy')
        ]
        cursor.executemany("INSERT INTO chuyenxe VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", trips_data)

        for tr in trips_data:
            t_id = tr[0]
            for s in range(1, 35):
                seat_num = f"A{s:02d}" if s <= 17 else f"B{s-17:02d}"
                cursor.execute("INSERT INTO ghengoi VALUES (?, ?, ?, ?)", (f"{seat_num}_{t_id}", t_id, seat_num, 'Trống'))

        cursor.executemany("INSERT INTO ve VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [
            ('VE00001', 'CX00001', 'KH00001', 2, 'A01, A02', 320000, 'Bến xe Trung tâm Đà Nẵng', 'Bến xe phía Nam Huế', today_s + ' 06:00', 'Đã đặt', 'Đã thanh toán'),
            ('VE00002', 'CX00005', 'KH00002', 1, 'A05', 70000, 'Cầu Rồng, Đà Nẵng', 'Phố cổ Hội An', today_s + ' 07:15', 'Đã đặt', 'Chưa thanh toán'),
            ('VE00003', 'CX00007', 'KH00001', 1, 'B02', 260000, 'Đà Nẵng', 'Bến xe Quy Nhơn', today_s + ' 06:15', 'Đã đặt', 'Đã thanh toán')
        ])

        cursor.execute("UPDATE ghengoi SET trangThai = 'Đã đặt' WHERE (Chuyenxe = 'CX00001' AND (soGhe = 'A01' OR soGhe = 'A02'))")
        cursor.execute("UPDATE ghengoi SET trangThai = 'Đã đặt' WHERE (Chuyenxe = 'CX00005' AND soGhe = 'A05')")
        cursor.execute("UPDATE ghengoi SET trangThai = 'Đã đặt' WHERE (Chuyenxe = 'CX00007' AND soGhe = 'B02')")

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
                                    <td>{x["tenNhaXe"] or "Hải Vân Limousine"}</td>
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
                                    <td>Hải Vân Limousine</td>
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
                        "Nhaxe": u["NhaxeID"]
                    })
                return self._send_json(users)

            elif path.startswith('/api/user-auth/'):
                uid = path.split('/')[-1]
                cursor.execute("SELECT * FROM nguoidung WHERE UserID = ? OR TenDangNhap = ?", (uid, uid))
                row = cursor.fetchone()
                return self._send_json(dict(row) if row else {}, 200 if row else 404)

            # 2. KHÁCH HÀNG
            elif path == '/api/khachhang':
                cursor.execute("SELECT * FROM khachhang")
                return self._send_json([dict(r) for r in cursor.fetchall()])

            elif path.startswith('/api/khachhang/') and path.endswith('/lich-su-ve'):
                kh_id = path.split('/')[3]
                cursor.execute("SELECT * FROM ve WHERE KhachHang = ?", (kh_id,))
                return self._send_json([dict(r) for r in cursor.fetchall()])

            elif path.startswith('/api/khachhang/'):
                kh_id = path.split('/')[-1]
                cursor.execute("SELECT * FROM khachhang WHERE KhachHangID = ? OR soDienThoai = ?", (kh_id, kh_id))
                row = cursor.fetchone()
                return self._send_json(dict(row) if row else {}, 200 if row else 404)

            # 3. NHÀ XE
            elif path.startswith('/api/nhaxe/'):
                nx_id = path.split('/')[-1]
                cursor.execute("SELECT * FROM nhaxe WHERE NhaxeID = ?", (nx_id,))
                row = cursor.fetchone()
                if row:
                    d = dict(row)
                    d["BusName"] = d["tenNhaXe"]
                    return self._send_json(d)
                return self._send_json({}, 404)

            # 4. TÀI XẾ & CHI TIẾT TÀI XẾ
            elif path == '/api/taixe':
                cursor.execute("SELECT * FROM taixe")
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["TaixeID"] = d.get("TaiXeID")
                    d["Taixe"] = d.get("TaiXeID")
                    d["HinhAnhURL"] = d.get("AnhDaiDien")
                    rows.append(d)
                return self._send_json(rows)

            elif path == '/api/chitiettaixe':
                cursor.execute("SELECT * FROM chitiettaixe")
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["Taixe"] = d.get("TaiXe")
                    d["TaixeID"] = d.get("TaiXe")
                    d["TaiXeID"] = d.get("TaiXe")
                    d["HinhAnhURL"] = d.get("AnhDaiDien")
                    rows.append(d)
                return self._send_json(rows)

            # 5. XE & LOẠI XE
            elif path == '/api/xe':
                cursor.execute("""
                SELECT x.*, l.tenLoai, l.soCho, n.tenNhaXe 
                FROM xe x 
                LEFT JOIN loaixe l ON x.Loaixe = l.LoaixeID 
                LEFT JOIN nhaxe n ON x.Nhaxe = n.NhaxeID
                """)
                rows = []
                for r in cursor.fetchall():
                    d = dict(r)
                    d["loaiXe"] = d["Loaixe"]
                    d["nhaXe"] = d["Nhaxe"]
                    rows.append(d)
                return self._send_json(rows)

            elif path == '/api/loaixe':
                cursor.execute("SELECT * FROM loaixe")
                return self._send_json([dict(r) for r in cursor.fetchall()])

            # 6. TUYẾN XE
            elif path == '/api/tuyenxe':
                cursor.execute("SELECT * FROM tuyenxe")
                return self._send_json([dict(r) for r in cursor.fetchall()])

            # 7. CHUYẾN XE (TRIP)
            elif path == '/api/chuyenxe':
                cursor.execute("""
                SELECT c.*, t.tenTuyen, t.diemDi, t.diemDen, t.thoiGianUocTinh,
                       x.bienSo, x.Loaixe as loaiXeId, l.tenLoai as loaiXeTen, l.soCho,
                       tx.HoTen as tenTaiXe, n.tenNhaXe
                FROM chuyenxe c
                LEFT JOIN tuyenxe t ON c.Tuyenxe = t.TuyenxeID
                LEFT JOIN xe x ON c.Xe = x.XeID
                LEFT JOIN loaixe l ON x.Loaixe = l.LoaixeID
                LEFT JOIN taixe tx ON c.TaiXe = tx.TaiXeID
                LEFT JOIN nhaxe n ON t.Nhaxe = n.NhaxeID
                ORDER BY c.ngayKhoiHanh DESC, c.gioDi ASC
                """)
                res = []
                for r in cursor.fetchall():
                    item = {
                        "ChuyenxeID": r["ChuyenxeID"],
                        "id": r["ChuyenxeID"],
                        "Tuyenxe": r["Tuyenxe"],
                        "TuyenxeID": r["Tuyenxe"],
                        "tuyenXeName": r["tenTuyen"],
                        "routeName": r["tenTuyen"],
                        "diemDi": r["diemDi"],
                        "diemDen": r["diemDen"],
                        "date": r["ngayKhoiHanh"],
                        "ngayKhoiHanh": r["ngayKhoiHanh"],
                        "time": r["gioDi"],
                        "gioDi": r["gioDi"],
                        "endTime": r["gioDen"],
                        "gioDen": r["gioDen"],
                        "price": r["giaVe"],
                        "giaVe": r["giaVe"],
                        "status": r["trangThai"],
                        "trangThai": r["trangThai"],
                        "carType": r["loaiXeTen"] or "Limousine VIP",
                        "totalSeats": r["soCho"] or 34,
                        "availableSeats": r["soCho"] or 34,
                        "TaiXeID": r["TaiXe"],
                        "tenTaiXe": r["tenTaiXe"],
                        "tenNhaXe": r["tenNhaXe"] or "Hải Vân Limousine",
                        "duration": r["thoiGianUocTinh"] or "2 giờ"
                    }
                    res.append(item)
                return self._send_json(res)

            elif path.startswith('/api/chuyenxe/'):
                cid = path.split('/')[-1]
                cursor.execute("""
                SELECT c.*, t.tenTuyen, x.bienSo, l.soCho 
                FROM chuyenxe c
                LEFT JOIN tuyenxe t ON c.Tuyenxe = t.TuyenxeID
                LEFT JOIN xe x ON c.Xe = x.XeID
                LEFT JOIN loaixe l ON x.Loaixe = l.LoaixeID
                WHERE c.ChuyenxeID = ?
                """, (cid,))
                row = cursor.fetchone()
                return self._send_json(dict(row) if row else {}, 200 if row else 404)

            # 8. GHẾ NGỒI
            elif path == '/api/ghengoi':
                chuyen_xe_id = qs.get('ChuyenXe', [''])[0]
                if chuyen_xe_id:
                    auto_generate_seats_if_needed(conn, chuyen_xe_id)
                    cursor.execute("SELECT * FROM ghengoi WHERE Chuyenxe = ? ORDER BY soGhe", (chuyen_xe_id,))
                else:
                    cursor.execute("SELECT * FROM ghengoi")
                return self._send_json([dict(r) for r in cursor.fetchall()])

            # 9. VÉ XE
            elif path == '/api/ve':
                kh_id = qs.get('KhachHang', [''])[0]
                status = qs.get('TrangThai', [''])[0]
                cx_id = qs.get('ChuyenXe', [''])[0]

                query = "SELECT * FROM ve WHERE 1=1"
                params = []
                if kh_id:
                    query += " AND KhachHang = ?"
                    params.append(kh_id)
                if status:
                    query += " AND trangThai = ?"
                    params.append(status)
                if cx_id:
                    query += " AND Chuyenxe = ?"
                    params.append(cx_id)

                cursor.execute(query, params)
                return self._send_json([dict(r) for r in cursor.fetchall()])

            elif path == '/api/vehuy':
                kh_id = qs.get('KhachHang', [''])[0]
                if kh_id:
                    cursor.execute("SELECT * FROM ve WHERE KhachHang = ? AND trangThai = 'Đã hủy'", (kh_id,))
                else:
                    cursor.execute("SELECT * FROM ve WHERE trangThai = 'Đã hủy'")
                return self._send_json([dict(r) for r in cursor.fetchall()])

            # 10. ĐÁNH GIÁ
            elif path == '/api/danhgia':
                cursor.execute("SELECT * FROM danhgia")
                return self._send_json([dict(r) for r in cursor.fetchall()])

            else:
                return self._send_json({"error": "Endpoint not found"}, 404)

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
                        return self._send_json({"status": "success", "user": dict(row)})
                    return self._send_json({"error": "Sai tài khoản hoặc mật khẩu"}, 400)
                else:
                    uid = data.get("UserID") or f"US{int(datetime.now().timestamp()*1000)%1000000:06d}"
                    phone = data.get("SoDienThoai") or data.get("phone") or ""
                    cursor.execute("""
                    INSERT OR REPLACE INTO nguoidung (UserID, TenDangNhap, MatKhau, Email, SoDienThoai, Vaitro, Hovaten, KhachHangID, NhaxeID)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
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
                cursor.execute("""
                INSERT OR REPLACE INTO khachhang (KhachHangID, hoTen, Email, Ngaysinh, soDienThoai, AnhDaiDienURL)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    kh_id,
                    data.get("Hovaten") or data.get("hoTen") or "",
                    data.get("Email") or "",
                    data.get("Ngaysinh") or "2000-01-01",
                    data.get("soDienThoai") or data.get("SoDienThoai") or "",
                    data.get("AnhDaiDienURL") or ""
                ))
                conn.commit()
                return self._send_json({"status": "success", "KhachHangID": kh_id}, 201)

            # NHÀ XE REGISTER
            elif path == '/api/nhaxe':
                nx_id = data.get("NhaxeID") or f"NX{int(datetime.now().timestamp()*1000)%1000000:06d}"
                cursor.execute("""
                INSERT OR REPLACE INTO nhaxe (NhaxeID, tenNhaXe, diaChi, soDienThoai, email, nguoiDaiDien, giayPhepKinhDoanh, logo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    nx_id,
                    data.get("tenNhaXe") or "",
                    data.get("diaChi") or "",
                    data.get("soDienThoai") or "",
                    data.get("email") or "",
                    data.get("nguoiDaiDien") or "",
                    data.get("giayPhepKinhDoanh") or "",
                    data.get("logo") or ""
                ))
                conn.commit()
                return self._send_json({"status": "success", "NhaxeID": nx_id}, 201)

            # ĐẶT VÉ (BOOK TICKET)
            elif path == '/api/dat-ve':
                ve_id = data.get("ve_id") or f"VE{int(datetime.now().timestamp()*1000)%1000000:06d}"
                chuyen_xe_id = data.get("chuyen_xe_id")
                so_dien_thoai = data.get("so_dien_thoai")
                ghe_ids = data.get("ghe_ids", [])
                tong_tien = data.get("tong_tien", 0)
                diem_don = data.get("diem_don", "")
                diem_tra = data.get("diem_tra", "")

                cursor.execute("SELECT KhachHangID FROM khachhang WHERE soDienThoai = ?", (so_dien_thoai,))
                row = cursor.fetchone()
                if row:
                    kh_id = row[0]
                else:
                    kh_id = f"KH{int(datetime.now().timestamp()*1000)%1000000:06d}"
                    cursor.execute("INSERT INTO khachhang (KhachHangID, hoTen, soDienThoai) VALUES (?, ?, ?)",
                                   (kh_id, f"Khách hàng {so_dien_thoai}", so_dien_thoai))

                danh_sach_ghe_str = ", ".join(ghe_ids) if isinstance(ghe_ids, list) else str(ghe_ids)

                cursor.execute("""
                INSERT INTO ve (VeID, Chuyenxe, KhachHang, soLuongGhe, danhSachGhe, tongTien, diemDon, diemTra, ngayDat, trangThai, trangThaiThanhToan)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Đã đặt', 'Chưa thanh toán')
                """, (
                    ve_id, chuyen_xe_id, kh_id, len(ghe_ids), danh_sach_ghe_str,
                    tong_tien, diem_don, diem_tra, datetime.now().strftime("%Y-%m-%d %H:%M")
                ))

                for g in ghe_ids:
                    cursor.execute("UPDATE ghengoi SET trangThai = 'Đã đặt' WHERE Chuyenxe = ? AND soGhe = ?", (chuyen_xe_id, g))

                conn.commit()
                return self._send_json({"status": "success", "message": "Đặt vé thành công!", "VeID": ve_id}, 201)

            # HỦY VÉ (CANCEL TICKET)
            elif path == '/api/huy-ve':
                ve_id = data.get("ve_id")
                cursor.execute("SELECT * FROM ve WHERE VeID = ?", (ve_id,))
                ticket = cursor.fetchone()
                if ticket:
                    cursor.execute("UPDATE ve SET trangThai = 'Đã hủy' WHERE VeID = ?", (ve_id,))
                    danh_sach = ticket["danhSachGhe"].split(", ")
                    for s in danh_sach:
                        cursor.execute("UPDATE ghengoi SET trangThai = 'Trống' WHERE Chuyenxe = ? AND soGhe = ?", (ticket["Chuyenxe"], s.strip()))
                    cursor.execute("INSERT INTO vehuy (Ve, KhachHang, lyDoHuy, ngayHuy) VALUES (?, ?, ?, ?)",
                                   (ve_id, ticket["KhachHang"], data.get("lyDoHuy", "Khách yêu cầu hủy"), datetime.now().strftime("%Y-%m-%d %H:%M")))
                    conn.commit()
                    return self._send_json({"status": "success", "message": "Hủy vé thành công!"})
                return self._send_json({"error": "Không tìm thấy vé"}, 404)

            # TẠO PHƯƠNG TIỆN
            elif path == '/api/xe':
                xe_id = data.get("XeID") or f"XE{int(datetime.now().timestamp()*1000)%1000000:06d}"
                cursor.execute("INSERT INTO xe (XeID, bienSo, Loaixe, Nhaxe, trangThai) VALUES (?, ?, ?, ?, ?)",
                               (xe_id, data.get("bienSo"), data.get("Loaixe") or data.get("loaiXe"), data.get("Nhaxe") or data.get("nhaXe"), data.get("trangThai", "Hoạt động")))
                conn.commit()
                return self._send_json({"status": "success", "XeID": xe_id}, 201)

            # TẠO TUYẾN XE
            elif path == '/api/tuyenxe':
                txe_id = data.get("TuyenxeID") or f"TXE{int(datetime.now().timestamp()*1000)%1000000:06d}"
                cursor.execute("""
                INSERT INTO tuyenxe (TuyenxeID, tenTuyen, diemDi, diemDen, diemDung, khoangCach, thoiGianUocTinh, giaCoBan, Nhaxe)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    txe_id, data.get("tenTuyen"), data.get("diemDi"), data.get("diemDen"),
                    data.get("diemDung", ""), float(data.get("khoangCach", 0)),
                    data.get("thoiGianUocTinh", "2 giờ"), int(data.get("giaCoBan", 150000)),
                    data.get("Nhaxe", "NX00001")
                ))
                conn.commit()
                return self._send_json({"status": "success", "TuyenxeID": txe_id}, 201)

            # TẠO CHUYẾN XE
            elif path == '/api/chuyenxe':
                cx_id = data.get("ChuyenxeID") or f"CX{int(datetime.now().timestamp()*1000)%1000000:06d}"
                cursor.execute("""
                INSERT INTO chuyenxe (ChuyenxeID, Tuyenxe, Xe, TaiXe, ngayKhoiHanh, gioDi, gioDen, giaVe, trangThai)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    cx_id, data.get("Tuyenxe") or data.get("TuyenxeID"),
                    data.get("Xe") or data.get("XeID"),
                    data.get("TaiXe") or data.get("TaiXeID"),
                    data.get("ngayKhoiHanh") or date.today().isoformat(),
                    data.get("gioDi", "08:00"), data.get("gioDen", "10:30"),
                    int(data.get("giaVe", 160000)), data.get("trangThai", "Sắp chạy")
                ))
                conn.commit()
                auto_generate_seats_if_needed(conn, cx_id)
                return self._send_json({"status": "success", "ChuyenxeID": cx_id, "id": cx_id}, 201)

            # TẠO TÀI XẾ
            elif path == '/api/taixe' or path == '/api/chitiettaixe':
                tx_id = data.get("TaiXeID") or data.get("TaiXe") or f"TX{int(datetime.now().timestamp()*1000)%1000000:06d}"
                cursor.execute("""
                INSERT OR REPLACE INTO taixe (TaiXeID, HoTen, SoDienThoai, SoBangLai, Nhaxe, AnhDaiDien)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (tx_id, data.get("HoTen", ""), data.get("SoDienThoai", ""), data.get("SoBangLai", ""), data.get("Nhaxe", "NX00001"), data.get("AnhDaiDien", "")))
                cursor.execute("""
                INSERT OR REPLACE INTO chitiettaixe (ChiTietID, TaiXe, HoTen, SoDienThoai, SoBangLai, Nhaxe, AnhDaiDien)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (tx_id, tx_id, data.get("HoTen", ""), data.get("SoDienThoai", ""), data.get("SoBangLai", ""), data.get("Nhaxe", "NX00001"), data.get("AnhDaiDien", "")))
                conn.commit()
                return self._send_json({"status": "success", "TaiXeID": tx_id}, 201)

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
                        if k in ['trangThai', 'status']:
                            cursor.execute("UPDATE chuyenxe SET trangThai = ? WHERE ChuyenxeID = ?", (v, res_id))
                        elif k in ['TaiXe', 'TaiXeID']:
                            cursor.execute("UPDATE chuyenxe SET TaiXe = ? WHERE ChuyenxeID = ?", (v, res_id))
                    conn.commit()
                    return self._send_json({"status": "success"})

                elif resource == 'xe':
                    for k, v in data.items():
                        if k in ['trangThai', 'status']:
                            cursor.execute("UPDATE xe SET trangThai = ? WHERE XeID = ?", (v, res_id))
                        elif k in ['bienSo']:
                            cursor.execute("UPDATE xe SET bienSo = ? WHERE XeID = ?", (v, res_id))
                    conn.commit()
                    return self._send_json({"status": "success"})

                elif resource == 'khachhang':
                    if "Hovaten" in data or "hoTen" in data:
                        cursor.execute("UPDATE khachhang SET hoTen = ? WHERE KhachHangID = ?", (data.get("Hovaten") or data.get("hoTen"), res_id))
                    if "Email" in data:
                        cursor.execute("UPDATE khachhang SET Email = ? WHERE KhachHangID = ?", (data.get("Email"), res_id))
                    if "Ngaysinh" in data:
                        cursor.execute("UPDATE khachhang SET Ngaysinh = ? WHERE KhachHangID = ?", (data.get("Ngaysinh"), res_id))
                    if "AnhDaiDienURL" in data:
                        cursor.execute("UPDATE khachhang SET AnhDaiDienURL = ? WHERE KhachHangID = ?", (data.get("AnhDaiDienURL"), res_id))
                    conn.commit()
                    return self._send_json({"status": "success"})

                elif resource == 'nhaxe':
                    for col in ['tenNhaXe', 'diaChi', 'soDienThoai', 'email', 'nguoiDaiDien', 'logo']:
                        if col in data:
                            cursor.execute(f"UPDATE nhaxe SET {col} = ? WHERE NhaxeID = ?", (data[col], res_id))
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
                    "ve": ("ve", "VeID")
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
