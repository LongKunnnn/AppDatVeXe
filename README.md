# 🚌 VeXeApp - Ứng Dụng Quản Lý & Đặt Vé Xe Khách Liên Tỉnh

> **Dự án Native Android (Java) kết hợp Backend REST API (Python) & Cơ sở dữ liệu SQLite.**  
> Dự án phục vụ đầy đủ 2 đối tượng người dùng: **Khách hàng** (tìm kiếm, chọn ghế, đặt vé trực tuyến) và **Nhà xe** (điều hành ma trận lịch chạy, quản lý tài xế, phương tiện, tuyến đường và theo dõi lộ trình bản đồ).

---

## 📋 Mục lục
1. [Yêu cầu môi trường cài đặt](#-1-yêu-cầu-môi-trường-cài-đặt)
2. [Hướng dẫn cài đặt & Chạy ứng dụng từng bước](#-2-hướng-dẫn-cài-đặt--chạy-ứng-dụng-từng-bước)
   - [Bước 1: Khởi động Backend Server](#bước-1-khởi-động-backend-server-bắt-buộc-chạy-trước)
   - [Bước 2: Mở dự án trong Android Studio](#bước-2-mở-dự-án-trong-android-studio)
   - [Bước 3: Cấu hình địa chỉ kết nối API](#bước-3-cấu-hình-địa-chỉ-kết-nối-api)
   - [Bước 4: Chạy ứng dụng lên thiết bị](#bước-4-chạy-ứng-dụng-lên-thiết-bị)
3. [Tài khoản thử nghiệm sẵn có](#-3-tài-khoản-thử-nghiệm-sẵn-có)
4. [Hướng dẫn trải nghiệm các tính năng chính](#-4-hướng-dẫn-trải-nghiệm-các-tính-năng-chính)
5. [Khắc phục các lỗi thường gặp (FAQ)](#-5-khắc-phục-các-lỗi-thường-gặp-faq)

---

## 💻 1. Yêu cầu môi trường cài đặt

Trước khi bắt đầu, máy tính của bạn cần có sẵn:

1. **Python 3.10 trở lên**:
   - Tải tại: [python.org](https://www.python.org/downloads/)
   - *Lưu ý quan trọng:* Khi cài đặt trên Windows, nhớ tích chọn **"Add python.exe to PATH"**.
2. **Android Studio**:
   - Phiên bản khuyến nghị: Flamingo, Hedgehog, Iguana, Koala hoặc mới hơn.
   - Đã cài đặt Android SDK (API 24 trở lên, tốt nhất là API 33 - 35).
   - JDK khuyến nghị: **JDK 17** (mặc định đi kèm trong Android Studio).
3. **Thiết bị chạy app**:
   - **Máy ảo Android (Emulator)**: Pixel 6/7/8 với Android 13/14 (API 33/34).
   - Hoặc **Điện thoại thật**: Chạy hệ điều hành Android 7.0 trở lên, bật chế độ *USB Debugging*.

---

## 🚀 2. Hướng dẫn cài đặt & Chạy ứng dụng từng bước

### Bước 1: Khởi động Backend Server *(Bắt buộc chạy trước)*

Backend cung cấp toàn bộ dữ liệu (tuyến xe, chuyến xe, tài khoản, vé) cho app hoạt động.

1. Mở cửa sổ **Terminal / Command Prompt / PowerShell** tại thư mục gốc dự án (`AppDatVeXe`).
2. Gõ lệnh sau để khởi động Server:
   ```bash
   python backend/server.py
   ```
   *(Nếu dùng macOS / Linux hoặc máy cài nhiều bản Python, có thể dùng `python3 backend/server.py`)*.

3. Khi màn hình xuất hiện thông báo sau là Server đã chạy thành công:
   ```text
   =================================================================
   🚀 VEXEAPP BACKEND SERVER & WEB DASHBOARD ĐÃ KHỞI CHẠY!
   🌐 Xem Web Quản Trị trên trình duyệt: http://localhost:8000/
   📱 Đối với Android Emulator: http://10.0.2.2:8000/
   📁 Cơ sở dữ liệu SQLite: ...\database\vexe.db
   =================================================================
   ```
   > 💡 **Mẹo:** Bạn có thể mở trình duyệt web và vào [http://localhost:8000/](http://localhost:8000/) để xem trực quan bảng điều khiển thống kê vé và các chuyến xe!  
   > ⚠️ **Chú ý:** Giữ nguyên cửa sổ terminal này, không tắt trong suốt quá trình test app.

---

### Bước 2: Mở dự án trong Android Studio

1. Mở phần mềm **Android Studio**.
2. Chọn **File** > **Open...** (hoặc chọn **Open** trên màn hình Welcome).
3. Tìm và chọn đúng thư mục dự án `AppDatVeXe`, sau đó nhấn **OK**.
4. Chờ Android Studio đồng bộ mã nguồn và tải các thư viện Gradle cần thiết.
   * *Kiểm tra phiên bản JDK:* Vào **File** > **Settings** (trên Mac: **Android Studio** > **Preferences**) > **Build, Execution, Deployment** > **Build Tools** > **Gradle** > Mục **Gradle JDK** chọn **Embedded JDK 17**.
5. Nhấn nút **Sync Project with Gradle Files** (biểu tượng chú voi 🐘 ở góc trên bên phải) để đảm bảo không có cảnh báo lỗi nào.

---

### Bước 3: Cấu hình địa chỉ kết nối API

Mở file: `app/src/main/java/com/vexeapp/api/ApiClient.java`.

Kiểm tra biến `BASE_URL` (khoảng dòng 22):

* **Trường hợp 1: Bạn chạy bằng Máy ảo Android Studio (Khuyên dùng)**:
  Giữ nguyên mặc định:
  ```java
  public static final String BASE_URL = "http://10.0.2.2:8000/";
  ```
  *(Địa chỉ `10.0.2.2` là IP đặc biệt của máy ảo trỏ về localhost máy tính của bạn).*

* **Trường hợp 2: Bạn chạy bằng Điện thoại thật cắm dây cáp**:
  1. Đảm bảo điện thoại và máy tính đang **bắt chung một mạng Wi-Fi**.
  2. Mở terminal trên máy tính, gõ lệnh `ipconfig` (Windows) hoặc `ifconfig` (Mac) để tìm địa chỉ IPv4 (ví dụ: `192.168.1.15`).
  3. Đổi lại `BASE_URL` trong file `ApiClient.java`:
     ```java
     public static final String BASE_URL = "http://192.168.1.15:8000/";
     ```

---

### Bước 4: Chạy ứng dụng lên thiết bị

1. Trên thanh công cụ Android Studio, chọn thiết bị đích (Ví dụ: `Pixel 7 API 34`).
2. Nhấn nút **Run 'app' ▶️** (phím tắt `Shift + F10`).
3. Chờ ứng dụng được biên dịch và tự động cài đặt, mở lên trên màn hình điện thoại.

---

## 🔑 3. Tài khoản thử nghiệm sẵn có

Hệ thống đã có sẵn dữ liệu tài khoản mẫu được kích hoạt sẵn để bạn kiểm tra ngay:

| Vai trò | Tên đăng nhập / Số điện thoại | Mật khẩu | Thông tin chi tiết |
| :--- | :--- | :--- | :--- |
| **Nhà xe (Quản trị)** | `haivan` | `123456` | Nhà xe Hải Vân Limousine (Đà Nẵng - Huế) |
| **Nhà xe (Quản trị)** | `phuongtrang` | `123456` | Phương Trang Bus Lines |
| **Khách hàng** | `0912345678` | `123456` | Khách hàng: Lê Hoàng Nam |
| **Khách hàng** | `0987654321` | `123456` | Khách hàng: Nguyễn Thu Hà |
| **Khách hàng mới** | Tự bấm **"Đăng ký"** | Tự đặt | Xác thực OTP trực tiếp, tự sinh ID |

---

## 📱 4. Hướng dẫn trải nghiệm các tính năng chính

### Phân hệ 1: Dành cho Khách hàng (Đặt vé trực tuyến)

1. **Đăng nhập:** Mở app, nhập SĐT `0912345678` và Mật khẩu `123456` -> Bấm **Đăng nhập**.
2. **Tìm kiếm vé:**
   - Chọn điểm đi: **Đà Nẵng**
   - Chọn điểm đến: **Huế** (hoặc Hội An)
   - Chọn ngày đi và nhấn **Tìm vé**.
3. **Chọn chuyến & Sơ đồ ghế:**
   - Chọn một chuyến xe trong danh sách kết quả.
   - Màn hình sơ đồ ghế hiện ra: Bấm chọn các ghế trống (ghế đổi màu cam và tự tính tổng tiền).
4. **Xác nhận đặt vé & Thanh toán:**
   - Chọn điểm đón và điểm trả khách.
   - Nhấn **Xác nhận đặt vé** -> App hiển thị thông tin hóa đơn và thông báo đặt vé thành công.
5. **Quản lý vé đã mua:**
   - Chuyển sang tab **Vé của tôi** ở thanh điều hướng dưới: Xem danh sách vé đã đặt, xem mã vé, thực hiện **Hủy vé** nếu muốn.
6. **Đánh giá chuyến đi:**
   - Vào các chuyến đã hoàn thành để chấm điểm số sao và viết nhận xét.

---

### Phân hệ 2: Dành cho Nhà xe (Điều hành & Quản lý)

1. **Đăng nhập nhà xe:**
   - Tại màn hình Đăng nhập, bấm vào dòng chữ: **"Bạn là nhà xe?"**.
   - Nhập tài khoản: `haivan` | Mật khẩu: `123456` -> Bấm **Đăng nhập**.
2. **Bảng ma trận điều hành lịch chạy (Trang chủ):**
   - Hiển thị danh sách các tài xế và lịch trình ca chạy theo từng ngày trong tuần.
   - Nhấn trực tiếp vào từng ô ca chạy để xem chi tiết danh sách khách đi xe.
3. **Quản lý Phương tiện:**
   - Bấm tab **Phương tiện** ở menu dưới: Xem danh sách xe, cấu hình Loại xe (Limousine, Giường nằm...), thêm xe mới với biển số xe và trạng thái.
4. **Quản lý Tuyến xe & Chuyến xe:**
   - Thêm tuyến mới (khoảng cách, thời gian dự kiến, giá vé cơ bản).
   - Tạo chuyến xe mới: Chỉ định tuyến, giờ xuất bến, gán biển số xe và tài xế phụ trách.
5. **Xem bản đồ lộ trình di chuyển (OpenStreetMap):**
   - Xem tuyến đường tương tác và các vị trí đón/trả khách của hành khách trên nền bản đồ số vệ tinh.

---

## 🛠️ 5. Khắc phục các lỗi thường gặp (FAQ)

#### ❓ Lỗi 1: Ứng dụng báo "Lỗi kết nối server!" khi bấm đăng nhập/tìm vé
* **Nguyên nhân:** Backend Python chưa được bật, hoặc điện thoại không kết nối được tới server.
* **Cách sửa:**
  1. Đảm bảo cửa sổ `python backend/server.py` vẫn đang chạy và không bị tắt.
  2. Nếu dùng máy ảo, đảm bảo `ApiClient.java` đang dùng `http://10.0.2.2:8000/`.
  3. Nếu dùng điện thoại thật, kiểm tra máy tính và điện thoại đã kết nối chung 1 mạng Wi-Fi chưa.

#### ❓ Lỗi 2: Tắt server rồi mở lại thì dữ liệu vé vừa đặt bị mất
* **Nguyên nhân:** File `backend/server.py` đang bật chế độ reset database (`force_reseed=True`).
* **Cách sửa:** Mở file `backend/server.py` (khoảng dòng 1321), đổi thành:
  ```python
  init_database(force_reseed=False)
  ```
  Sau khi đổi thành `False`, dữ liệu vé đặt, tài khoản mới sẽ được giữ nguyên vĩnh viễn trong file SQLite `database/vexe.db`.

#### ❓ Lỗi 3: Android Studio báo lỗi XML Manifest khi build
* Đảm bảo không còn thẻ trống nào trong file `app/src/main/AndroidManifest.xml`.
* Vào menu **Build** > **Clean Project** rồi **Rebuild Project**.

---

## 👨‍💻 Tác giả & Giấy phép
* Dự án được xây dựng và duy trì bởi **VeXeApp Team**.
* Giấy phép mã nguồn mở phục vụ mục đích học tập và nghiên cứu.
