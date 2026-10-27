import re

with open("backend/server.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update GET /api/ve to include Chờ thanh toán, Chờ xác nhận when querying for 'Đã đặt'
old_status_check = """                if status:
                    query += " AND v.trangThai = ?"
                    params.append(status)"""

new_status_check = """                if status:
                    if status in ['Đã đặt', 'active']:
                        query += " AND v.trangThai IN ('Đã đặt', 'Đã xác nhận', 'Chờ thanh toán', 'Chờ xác nhận')"
                    else:
                        query += " AND v.trangThai = ?"
                        params.append(status)"""

assert old_status_check in content, "old_status_check not found!"
content = content.replace(old_status_check, new_status_check, 1)

# 2. In POST /api/dat-ve: Set initial ticket status to 'Chờ thanh toán', 'Chưa thanh toán'
old_insert_ve = """                cursor.execute(\"\"\"
                INSERT INTO ve (VeID, Chuyenxe, KhachHang, soLuongGhe, danhSachGhe, tongTien, diemDon, diemTra, ngayDat, trangThai, trangThaiThanhToan)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Đã đặt', 'Chưa thanh toán')
                \"\"\", ("""

new_insert_ve = """                cursor.execute(\"\"\"
                INSERT INTO ve (VeID, Chuyenxe, KhachHang, soLuongGhe, danhSachGhe, tongTien, diemDon, diemTra, ngayDat, trangThai, trangThaiThanhToan)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Chờ thanh toán', 'Chưa thanh toán')
                \"\"\", ("""

assert old_insert_ve in content, "old_insert_ve not found!"
content = content.replace(old_insert_ve, new_insert_ve, 1)

# 3. Add POST /api/thanh-toan-ve, POST /api/xac-nhan-ve, and POST /api/loaixe
old_danhgia_post = """            # GỬI ĐÁNH GIÁ (FEEDBACK)
            elif path == '/api/danhgia':
                cursor.execute(\"\"\"
                INSERT INTO danhgia (Ve, KhachHang, soSao, noiDung, ngayDanhGia)
                VALUES (?, ?, ?, ?, ?)
                \"\"\", (
                    data.get("ve_id") or data.get("Ve"),
                    data.get("khach_hang_id") or data.get("KhachHang"),
                    int(data.get("so_sao") or data.get("soSao", 5)),
                    data.get("noi_dung") or data.get("noiDung", ""),
                    datetime.now().strftime("%Y-%m-%d %H:%M")
                ))
                conn.commit()
                return self._send_json({"status": "success", "message": "Gửi đánh giá thành công!"}, 201)"""

new_posts = """            # GỬI ĐÁNH GIÁ (FEEDBACK)
            elif path == '/api/danhgia':
                cursor.execute(\"\"\"
                INSERT INTO danhgia (Ve, KhachHang, soSao, noiDung, ngayDanhGia)
                VALUES (?, ?, ?, ?, ?)
                \"\"\", (
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
                }, 201)"""

assert old_danhgia_post in content, "old_danhgia_post not found!"
content = content.replace(old_danhgia_post, new_posts, 1)

# 4. Support tenLoai in do_PATCH for loaixe and resource == 've'
old_loaixe_patch = """                elif resource == 'loaixe':
                    if "giaVe" in data or "GiaVe" in data:
                        price = int(data.get("giaVe") or data.get("GiaVe"))
                        cursor.execute("UPDATE loaixe SET giaChuan = ? WHERE LoaixeID = ?", (price, res_id))
                    if "soCho" in data or "SoCho" in data:
                        seats = int(data.get("soCho") or data.get("SoCho"))
                        cursor.execute("UPDATE loaixe SET soCho = ? WHERE LoaixeID = ?", (seats, res_id))"""

new_loaixe_patch = """                elif resource == 'loaixe':
                    if "tenLoai" in data or "TenLoai" in data or "name" in data:
                        name = data.get("tenLoai") or data.get("TenLoai") or data.get("name")
                        cursor.execute("UPDATE loaixe SET tenLoai = ? WHERE LoaixeID = ?", (name, res_id))
                    if "giaVe" in data or "GiaVe" in data or "giaChuan" in data or "GiaChuan" in data:
                        price = int(data.get("giaVe") or data.get("GiaVe") or data.get("giaChuan") or data.get("GiaChuan"))
                        cursor.execute("UPDATE loaixe SET giaChuan = ? WHERE LoaixeID = ?", (price, res_id))
                    if "soCho" in data or "SoCho" in data:
                        seats = int(data.get("soCho") or data.get("SoCho"))
                        cursor.execute("UPDATE loaixe SET soCho = ? WHERE LoaixeID = ?", (seats, res_id))"""

assert old_loaixe_patch in content, "old_loaixe_patch not found!"
content = content.replace(old_loaixe_patch, new_loaixe_patch, 1)

# Add resource == 've' in do_PATCH
old_ghengoi_patch = """                elif resource == 'ghengoi':"""
new_ghengoi_patch = """                elif resource == 've':
                    for k, v in data.items():
                        if k in ['trangThai', 'TrangThai']:
                            cursor.execute("UPDATE ve SET trangThai = ? WHERE VeID = ?", (v, res_id))
                        elif k in ['trangThaiThanhToan', 'TrangThaiThanhToan']:
                            cursor.execute("UPDATE ve SET trangThaiThanhToan = ? WHERE VeID = ?", (v, res_id))
                    conn.commit()
                    return self._send_json({"status": "success", "VeID": res_id})

                elif resource == 'ghengoi':"""

assert old_ghengoi_patch in content, "old_ghengoi_patch not found!"
content = content.replace(old_ghengoi_patch, new_ghengoi_patch, 1)

# 5. In do_DELETE: add loaixe
old_table_map = """                table_map = {
                    "xe": ("xe", "XeID"),
                    "tuyenxe": ("tuyenxe", "TuyenxeID"),
                    "taixe": ("taixe", "TaiXeID"),
                    "chuyenxe": ("chuyenxe", "ChuyenxeID"),
                    "khachhang": ("khachhang", "KhachHangID"),
                    "user-auth": ("nguoidung", "UserID"),
                    "ve": ("ve", "VeID")
                }"""

new_table_map = """                table_map = {
                    "xe": ("xe", "XeID"),
                    "tuyenxe": ("tuyenxe", "TuyenxeID"),
                    "taixe": ("taixe", "TaiXeID"),
                    "chuyenxe": ("chuyenxe", "ChuyenxeID"),
                    "khachhang": ("khachhang", "KhachHangID"),
                    "user-auth": ("nguoidung", "UserID"),
                    "ve": ("ve", "VeID"),
                    "loaixe": ("loaixe", "LoaixeID")
                }"""

assert old_table_map in content, "old_table_map not found!"
content = content.replace(old_table_map, new_table_map, 1)

with open("backend/server.py", "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: backend/server.py updated successfully!")

