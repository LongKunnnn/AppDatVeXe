with open("database/vexe_database.sql", "r", encoding="utf-8") as f:
    sql = f.read()

target = """-- 1. Loại xe
INSERT INTO loaixe (LoaixeID, tenLoai, soCho, giaChuan) VALUES 
('LX01', 'Limousine VIP 34 chỗ', 34, 180000),
('LX02', 'Xe Giường Nằm 40 chỗ', 40, 150000),
('LX03', 'Xe Ghế Ngồi 29 chỗ', 29, 120000),
('LX04', 'Limousine Cung Điện 22 phòng', 22, 250000);
('LX05', 'Limousine Cung Điện 99 phòng', 99, 25000000);"""

replacement = """-- 1. Loại xe
INSERT INTO loaixe (LoaixeID, tenLoai, soCho, giaChuan) VALUES 
('LX01', 'Limousine VIP 34 chỗ', 34, 180000),
('LX02', 'Xe Giường Nằm 40 chỗ', 40, 150000),
('LX03', 'Xe Ghế Ngồi 29 chỗ', 29, 120000),
('LX04', 'Limousine Cung Điện 22 phòng', 22, 250000);"""

assert target in sql, "target not found in vexe_database.sql"
sql = sql.replace(target, replacement, 1)

with open("database/vexe_database.sql", "w", encoding="utf-8") as f:
    f.write(sql)

print("SUCCESS: vexe_database.sql fixed!")

