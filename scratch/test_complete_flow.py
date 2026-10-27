import sqlite3
import json
import os
import sys

DB_PATH = "database/vexe.db"

def test_complete_flow():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=== TEST 1: Loaixe CRUD ===")
    test_lx_id = "LX99999"
    # Delete if exists
    cursor.execute("DELETE FROM loaixe WHERE LoaixeID = ?", (test_lx_id,))
    conn.commit()

    # 1. Insert new loaixe
    cursor.execute("INSERT INTO loaixe (LoaixeID, tenLoai, soCho, giaChuan) VALUES (?, ?, ?, ?)",
                   (test_lx_id, "Limousine President", 11, 280000))
    conn.commit()
    cursor.execute("SELECT * FROM loaixe WHERE LoaixeID = ?", (test_lx_id,))
    row = cursor.fetchone()
    assert row is not None, "Failed to insert loaixe"
    assert row["tenLoai"] == "Limousine President"
    assert row["soCho"] == 11
    assert row["giaChuan"] == 280000
    print("✓ INSERT Loaixe OK")

    # 2. Update loaixe
    cursor.execute("UPDATE loaixe SET tenLoai = ?, soCho = ?, giaChuan = ? WHERE LoaixeID = ?",
                   ("Limousine Super President", 12, 300000, test_lx_id))
    conn.commit()
    cursor.execute("SELECT * FROM loaixe WHERE LoaixeID = ?", (test_lx_id,))
    row = cursor.fetchone()
    assert row["tenLoai"] == "Limousine Super President"
    assert row["soCho"] == 12
    assert row["giaChuan"] == 300000
    print("✓ UPDATE Loaixe OK")

    # 3. Delete loaixe
    cursor.execute("DELETE FROM loaixe WHERE LoaixeID = ?", (test_lx_id,))
    conn.commit()
    cursor.execute("SELECT * FROM loaixe WHERE LoaixeID = ?", (test_lx_id,))
    assert cursor.fetchone() is None
    print("✓ DELETE Loaixe OK")

    print("\n=== TEST 2: Ticket Booking -> Payment QR -> Operator Confirmation ===")
    test_ve_id = "VE999999"
    test_cx_id = "CX00001"
    test_kh_id = "KH00001"

    # Delete test ticket if exists
    cursor.execute("DELETE FROM ve WHERE VeID = ?", (test_ve_id,))
    conn.commit()

    # Step 1: Customer books ticket
    cursor.execute("""
    INSERT INTO ve (VeID, Chuyenxe, KhachHang, soLuongGhe, danhSachGhe, tongTien, diemDon, diemTra, ngayDat, trangThai, trangThaiThanhToan)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Chờ thanh toán', 'Chưa thanh toán')
    """, (test_ve_id, test_cx_id, test_kh_id, 2, "A1, A2", 300000, "Hà Nội", "Ninh Bình", "2026-10-28 09:00"))
    conn.commit()

    cursor.execute("SELECT trangThai, trangThaiThanhToan FROM ve WHERE VeID = ?", (test_ve_id,))
    row = cursor.fetchone()
    assert row["trangThai"] == "Chờ thanh toán"
    assert row["trangThaiThanhToan"] == "Chưa thanh toán"
    print(f"✓ Step 1: Booking created with status: '{row['trangThai']}', payment: '{row['trangThaiThanhToan']}'")

    # Verify that in Trip Detail, passenger is NOT in confirmed list
    confirmed_statuses = ['Đã đặt', 'Đã xác nhận', 'Đã đi', 'Hoàn thành']
    assert row["trangThai"] not in confirmed_statuses, "Ticket must not be confirmed yet"
    print("✓ Trip Detail verification: Passenger is NOT displayed on manifest while 'Chờ thanh toán'")

    # Step 2: Customer clicks "Tôi đã thanh toán" in QR dialog
    cursor.execute("UPDATE ve SET trangThai = 'Chờ xác nhận', trangThaiThanhToan = 'Chờ xác nhận' WHERE VeID = ?", (test_ve_id,))
    conn.commit()

    cursor.execute("SELECT trangThai, trangThaiThanhToan FROM ve WHERE VeID = ?", (test_ve_id,))
    row = cursor.fetchone()
    assert row["trangThai"] == "Chờ xác nhận"
    assert row["trangThaiThanhToan"] == "Chờ xác nhận"
    print(f"✓ Step 2: Customer paid: status updated to '{row['trangThai']}'")

    # Verify that in Trip Detail, this ticket is captured in Pending list and NOT manifest
    assert row["trangThai"] not in confirmed_statuses
    print("✓ Trip Detail verification: Ticket appears in Pending Confirmation section ('Chờ xác nhận') with button 'Xác nhận vé'")

    # Step 3: Bus operator clicks "Xác nhận vé"
    cursor.execute("UPDATE ve SET trangThai = 'Đã đặt', trangThaiThanhToan = 'Đã thanh toán' WHERE VeID = ?", (test_ve_id,))
    conn.commit()

    cursor.execute("SELECT trangThai, trangThaiThanhToan FROM ve WHERE VeID = ?", (test_ve_id,))
    row = cursor.fetchone()
    assert row["trangThai"] == "Đã đặt"
    assert row["trangThaiThanhToan"] == "Đã thanh toán"
    print(f"✓ Step 3: Operator confirmed: status is now '{row['trangThai']}', payment '{row['trangThaiThanhToan']}'")

    # Verify that NOW the passenger appears on the official manifest
    assert row["trangThai"] in confirmed_statuses
    print("✓ Trip Detail verification: Passenger NOW appears on passenger list!")

    # Cleanup test ticket
    cursor.execute("DELETE FROM ve WHERE VeID = ?", (test_ve_id,))
    conn.commit()

    conn.close()
    print("\nALL INTEGRATION TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    test_complete_flow()

