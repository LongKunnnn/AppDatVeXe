# VeXeApp - Ứng Dụng Quản Lý & Đặt Vé Xe Khách

Ứng dụng Android Native kết hợp Backend REST API phục vụ quản trị nhà xe và đặt vé xe trực tuyến.

---

## 📌 1. Các Tính Năng Nổi Bật

### Dành cho Khách hàng:
- **Đăng ký / Đăng nhập:** Đăng ký tài khoản với xác thực OTP giả lập, đăng nhập nhanh qua số điện thoại.
- **Tìm kiếm vé & Lịch sử tìm kiếm:** Tìm chuyến theo Điểm đi, Điểm đến, Ngày đi, Giờ đi; tự động lưu lịch sử tìm kiếm gần nhất.
- **Sơ đồ chọn ghế ngồi trực quan:** Lưới hiển thị trạng thái ghế (Trống, Đang chọn, Đã đặt), tự động tính tổng tiền.
- **Đặt vé & Nhập điểm đón/trả:** Xác nhận đặt vé, lưu trữ thông tin chuyến.
- **Quản lý vé:** Xem danh sách vé theo tab (Đã đặt, Đã đi, Đã hủy); xem chi tiết vé, thực hiện hủy vé khi cần.
- **Đánh giá & Nhận xét:** Chấm điểm sao và gửi nhận xét cho các chuyến xe đã hoàn thành.
- **Quản lý hồ sơ cá nhân:** Cập nhật họ tên, ngày sinh, đổi ảnh đại diện.

### Dành cho Nhà xe:
- **Đăng nhập quản trị:** Tài khoản nhà xe với vai trò điều hành.
- **Lịch biểu điều hành ma trận:** Bảng điều phối các tài xế và ca chạy trong các ngày tới.
- **Quản lý chuyến xe:** Thêm mới chuyến xe, cập nhật trạng thái (Sắp chạy, Đang chạy, Hoàn thành, Hủy), phân tài xế phụ trách.
- **Bản đồ lộ trình OpenStreetMap:** Xem tuyến đường tương tác và vị trí các điểm đón/trả của hành khách.
- **Quản lý tài xế:** Danh sách tài xế, tạo tài khoản tài xế mới, giám sát lịch trình.
- **Quản lý tuyến đường:** Thêm/sửa/xóa các tuyến xe, cự ly và thời gian di chuyển.
- **Quản lý phương tiện & Loại xe:** Cấu hình loại xe (Limousine, Giường nằm,...), quản lý biển số xe và trạng thái bảo dưỡng.

---

## 🛠️ 2. Công Nghệ Sử Dụng

- **Android Client:** Java, Compile SDK 35, Min SDK 24, Android Gradle Plugin 9.0+, Gradle 9.1.
- **Thư viện UI/Network:** Retrofit 2, Gson, Glide, CircleImageView, Material Design 3.
- **Bản đồ số:** OpenStreetMap (`osmdroid-android`, `osmbonuspack`) - miễn phí, không cần token tính phí.
- **Backend & Database:** Python HTTP Server + SQLite (đã có sẵn trong thư mục `backend/` và `database/`).
- **Database Script:** File `database/vexe_database.sql` tương thích MySQL / MariaDB / PostgreSQL.

---

## 🚀 3. Hướng Dẫn Chạy Dự Án

### Bước 1: Khởi động Backend Server
Mở terminal tại thư mục gốc của dự án và chạy:
```bash
python backend/server.py
```
Server sẽ chạy tại `http://localhost:8000/`.

### Bước 2: Cấu hình URL trong ứng dụng Android
Mở file `app/src/main/java/com/vexeapp/api/ApiClient.java`:
- Nếu chạy trên **máy ảo Android Emulator**: Sử dụng `"http://10.0.2.2:8000/"`.
- Nếu chạy trên **điện thoại thật** (cùng mạng Wi-Fi với máy tính): Thay bằng IP máy tính của bạn, ví dụ `"http://192.168.1.100:8000/"`.
- Nếu dùng **Cloud API Render**: `"https://api-vexeapp.onrender.com/"`.

### Bước 3: Mở & Chạy ứng dụng trên Android Studio
1. Mở Android Studio -> Chọn `Open` -> Chọn thư mục dự án `AppDatVeXe`.
2. Kiểm tra Gradle JDK: Chọn **JDK 17** trong `Settings` > `Build, Execution, Deployment` > `Build Tools` > `Gradle`.
3. Bấm nút **Sync Project with Gradle Files**.
4. Chọn máy ảo Android (API 33+) và nhấn nút **Run 'app'** (`Shift + F10`).

---

## 🔑 4. Tài Khoản Thử Nghiệm

| Vai trò | Tên đăng nhập / SĐT | Mật khẩu | Ghi chú |
| :--- | :--- | :--- | :--- |
| **Nhà xe** | `haivan` | `123456` | Hải Vân Limousine (Mã: `NX00001`) |
| **Khách hàng** | `0912345678` | *(Đăng nhập bằng SĐT)* | Lê Hoàng Nam (Mã: `KH00001`) |
| **Khách hàng mới** | Nhập SĐT bất kỳ | OTP xác nhận | Tự động tạo hồ sơ mới |


