# 🚌 VeXeApp - Ứng Dụng Quản Lý & Đặt Vé Xe Khách Liên Tỉnh

> **Dự án Native Android (Java) kết hợp Backend REST API (Python) & Cơ sở dữ liệu SQLite.**  
> Tuyến trọng điểm: **Hà Nội ⇄ Ninh Bình ⇄ Thanh Hóa**  
> Nhà xe đại diện: **Tràng An Limousine** (`NX00001`) và **Vân Anh Limousine** (`NX00002`).  
> Dự án phục vụ đầy đủ 2 đối tượng người dùng: **Khách hàng** (tìm kiếm chuyến xe thực tế, chọn ghế, thanh toán QR, quản lý vé) và **Nhà xe** (ma trận điều hành ca chạy, phân công tài xế, quản lý phương tiện, CRUD loại xe, duyệt xác nhận vé hành khách).

---

## 📋 Mục lục
1. [Kiến trúc & Công nghệ sử dụng](#-1-kiến-trúc--công-nghệ-sử-dụng)
2. [Yêu cầu môi trường cài đặt](#-2-yêu-cầu-môi-trường-cài-đặt)
3. [Hướng dẫn cài đặt & Khởi chạy từng bước](#-3-hướng-dẫn-cài-đặt--khởi-chạy-từng-bước)
   - [Bước 1: Khởi động Backend Server (bắt buộc trước)](#bước-1-khởi-động-backend-server-bắt-buộc-chạy-trước)
   - [Bước 2: Mở dự án trong Android Studio](#bước-2-mở-dự-án-trong-android-studio)
   - [Bước 3: Cấu hình địa chỉ IP API](#bước-3-cấu-hình-địa-chỉ-ip-api)
   - [Bước 4: Chạy ứng dụng lên thiết bị](#bước-4-chạy-ứng-dụng-lên-thiết-bị)
4. [Danh sách tài khoản thử nghiệm có sẵn](#-4-danh-sách-tài-khoản-thử-nghiệm-có-sẵn)
5. [Quy trình trải nghiệm các tính năng chính](#-5-quy-trình-trải-nghiệm-các-tính-năng-chính)
   - [A. Dành cho Khách hàng: Đặt vé & Thanh toán QR 2 chiều](#a-dành-cho-khách-hàng-đặt-vé--thanh-toán-qr-2-chiều)
   - [B. Dành cho Nhà xe: Điều hành, Duyệt vé & CRUD Loại xe](#b-dành-cho-nhà-xe-điều-hành-duyệt-vé--crud-loại-xe)
6. [Hướng dẫn sửa Database & Thêm dữ liệu mới](#-6-hướng-dẫn-sửa-database--thêm-dữ-liệu-mới)
7. [Khắc phục các sự cố thường gặp (FAQ)](#-7-khắc-phục-các-sự-cố-thường-gặp-faq)

---

## 🏗️ 1. Kiến trúc & Công nghệ sử dụng

- **Frontend (Android Native)**:
  - Ngôn ngữ: **Java** (Android SDK API 24 - 34, tương thích Android 7.0 đến Android 14+).
  - Kiến trúc: Activity + Recycler Adapter + Model View Pattern.
  - Thư viện mạng: **Retrofit 2** + **OkHttp 3** + **Gson Converter**.
  - Giao diện: Material Design, CardView, CircleImageView, Custom Dialogs.
- **Backend (Python Server)**:
  - File máy chủ: `backend/server.py` viết bằng Python `http.server` & `sqlite3` thuần (không cần cài thêm framework nặng).
  - Web Dashboard: Tích hợp sẵn tại `http://localhost:8000/` để xem nhanh dữ liệu trực quan trên trình duyệt.
- **Cơ sở dữ liệu (Database)**:
  - SQLite Database: `database/vexe.db` (chứa dữ liệu hoạt động thực tế).
  - File SQL Script: `database/vexe_database.sql` (lưu trữ cấu trúc và dữ liệu mẫu đầy đủ).

---

## 💻 2. Yêu cầu môi trường cài đặt

1. **Python 3.10 trở lên**:
   - Tải tại: [python.org](https://www.python.org/downloads/)
   - *Lưu ý:* Khi cài đặt trên Windows, nhớ tích chọn **"Add python.exe to PATH"**.
2. **Android Studio**:
   - Khuyến nghị: Iguana, Jellyfish, Koala hoặc mới hơn.
   - JDK: **JDK 17** (Embedded JDK đi kèm trong Android Studio).
3. **Thiết bị chạy app**:
   - **Máy ảo (Emulator)**: Pixel 6/7/8 chạy Android 13 hoặc 14 (API 33/34).
   - Hoặc **Điện thoại thật**: Android 7.0 trở lên, bật *USB Debugging*.

---

## 🚀 3. Hướng dẫn cài đặt & Khởi chạy từng bước

### Bước 1: Khởi động Backend Server *(Bắt buộc chạy trước)*

1. Mở cửa sổ **Terminal / PowerShell** tại thư mục gốc dự án (`AppDatVeXe`).
2. Chạy lệnh:
   ```powershell
   python backend/server.py
   ```
3. Khi màn hình xuất hiện thông báo sau là Server đã sẵn sàng:
   ```text
   =================================================================
   🚀 VEXEAPP BACKEND SERVER & WEB DASHBOARD ĐÃ KHỞI CHẠY!
   🌐 Xem Web Quản Trị trên trình duyệt: http://localhost:8000/
   📱 Đối với Android Emulator: http://10.0.2.2:8000/
   📁 Cơ sở dữ liệu SQLite: ...\database\vexe.db
   =================================================================
   ```
   > 💡 Bạn có thể mở trình duyệt vào [http://localhost:8000/](http://localhost:8000/) để xem bảng điều khiển thống kê chuyến xe, nhà xe và danh sách vé!  
   > ⚠️ **Giữ nguyên cửa sổ terminal này, không đóng trong suốt quá trình test app.**

---

### Bước 2: Mở dự án trong Android Studio

1. Mở **Android Studio** -> chọn **File** > **Open...**.
2. Trỏ đến thư mục `AppDatVeXe` và nhấn **OK**.
3. Chờ Android Studio Gradle Sync tải xong dependencies.
4. *Kiểm tra phiên bản JDK:* Vào **File** > **Settings** > **Build, Execution, Deployment** > **Build Tools** > **Gradle** > Mục **Gradle JDK** chọn **Embedded JDK 17**.

---

### Bước 3: Cấu hình địa chỉ IP API

Mở file: `app/src/main/java/com/vexeapp/api/ApiClient.java`:

- **Nếu dùng Máy ảo Android Studio (Khuyên dùng)**:
  Giữ nguyên mặc định:
  ```java
  public static final String BASE_URL = "http://10.0.2.2:8000/";
  ```
  *(Địa chỉ `10.0.2.2` là IP đặc biệt của Android Emulator kết nối vào máy tính host).*

- **Nếu dùng Điện thoại thật cắm cáp**:
  1. Đảm bảo điện thoại và máy tính bắt **chung mạng Wi-Fi**.
  2. Gõ `ipconfig` trên Windows Terminal để xem IPv4 (ví dụ `192.168.1.15`).
  3. Đổi lại `BASE_URL`:
     ```java
     public static final String BASE_URL = "http://192.168.1.15:8000/";
     ```

---

### Bước 4: Chạy ứng dụng lên thiết bị

1. Trên thanh công cụ Android Studio, chọn thiết bị Emulator (hoặc điện thoại thật).
2. Nhấn nút **Run 'app' ▶️** (phím tắt `Shift + F10`).
3. Ứng dụng sẽ tự động mở lên màn hình **Đăng nhập / Đăng ký** đầu tiên.

---

## 🔑 4. Danh sách tài khoản thử nghiệm có sẵn

Hệ thống đã có sẵn tài khoản mẫu cho cả 2 vai trò:

| Phân hệ | Tài khoản / Số điện thoại | Mật khẩu | Nhà xe / Người dùng phụ trách | Ghi chú tuyến xe |
| :--- | :--- | :--- | :--- | :--- |
| **Nhà xe** | `trangan` | `123456` | **Tràng An Limousine** (`NX00001`) | Tuyến Hà Nội ⇄ Ninh Bình |
| **Nhà xe** | `vananh` | `123456` | **Vân Anh Limousine** (`NX00002`) | Tuyến Hà Nội ⇄ Thanh Hóa, Ninh Bình ⇄ Thanh Hóa |
| **Khách hàng** | `0912345678` | `123456` | Khách hàng: **Lê Hoàng Nam** | Đã có sẵn lịch sử vé demo |
| **Khách hàng** | `0987654321` | `123456` | Khách hàng: **Nguyễn Thu Hà** | Tài khoản khách hàng mẫu 2 |
| **Tài khoản mới** | Tự bấm **"Đăng ký"** | Tự nhập | Khách hàng tự do | Tự động tạo mã `KH...` và lưu vào DB |

---

## 📱 5. Quy trình trải nghiệm các tính năng chính

### A. Dành cho Khách hàng: Đặt vé & Thanh toán QR 2 chiều

1. **Khởi động ứng dụng**: App mở thẳng vào trang **Đăng nhập Khách hàng** (không bị hiển thị màn hình Home ảo).
2. **Đăng nhập**: Nhập SĐT `0912345678` | Mật khẩu `123456` -> Bấm **Đăng nhập**.
3. **Tìm kiếm chuyến xe chính xác**:
   - Điểm đi: **Hà Nội**
   - Điểm đến: **Ninh Bình** (hoặc **Thanh Hóa**)
   - Bấm **Tìm vé**: Danh sách chuyến xe trả về đúng tuyến xe bạn chọn:
     - Tuyến *Hà Nội - Ninh Bình*: Do nhà xe **Tràng An Limousine** phục vụ.
     - Tuyến *Hà Nội - Thanh Hóa*: Do nhà xe **Vân Anh Limousine** phục vụ.
4. **Chọn chuyến xe & Chọn ghế**:
   - Chọn chuyến mong muốn, vào sơ đồ ghế và bấm chọn các ghế trống (ghế chuyển sang màu cam, tự động tính tổng tiền).
   - Chọn điểm đón / điểm trả khách -> Bấm **Xác nhận đặt vé**.
5. **Thanh toán QR 2 chiều**:
   - Sau khi đặt vé thành công, vé được tạo ở trạng thái ban đầu: `Chờ thanh toán`.
   - Vào menu **Vé của tôi** (tab dưới): Vé hiển thị với nút bấm màu xanh dương **"Thanh toán"**.
   - Bấm nút **"Thanh toán"**: Popup mã QR thanh toán xuất hiện với đầy đủ thông tin: Mã vé, Tuyến đường, Ngày giờ khởi hành, Số ghế và Tổng tiền.
   - Bấm nút **"Tôi đã thanh toán"**: Vé lập tức chuyển trạng thái sang `Chờ xác nhận`. Nút bấm trên thẻ vé chuyển thành màu cam: **"Chờ nhà xe xác nhận"** (bị khóa, chống bấm lặp).

---

### B. Dành cho Nhà xe: Điều hành, Duyệt vé & CRUD Loại xe

1. **Đăng nhập nhà xe**:
   - Tại màn hình Đăng nhập, bấm dòng chữ: **"Bạn là nhà xe?"**.
   - Nhập: `trangan` (hoặc `vananh`) | Mật khẩu: `123456` -> Bấm **Đăng nhập**.
2. **Duyệt vé & Xác nhận hành khách lên chuyến**:
   - Vào **Trang chủ** hoặc **Chuyến xe** -> Chọn chuyến xe vừa có khách đặt.
   - **Đặc điểm quan trọng:** Tên khách hàng đặt vé **chưa xuất hiện** trong danh sách hành khách đi xe khi chưa thanh toán/chưa duyệt.
   - Trên màn hình Chi tiết chuyến sẽ xuất hiện riêng khu vực: **🔔 Vé chờ nhà xe xác nhận** với thẻ thông tin vé của khách hàng.
   - Nhà xe bấm nút **"✓ Xác nhận vé"**:
     - Vé được duyệt thành công sang trạng thái `Đã đặt` (Đã thanh toán).
     - Tên khách hàng lúc này mới **chính thức xuất hiện trong danh sách hành khách** trên chuyến xe!
     - Bên phía khách hàng, vé đổi trạng thái thành **"Đã xác nhận"**.
3. **Phân công & Đổi tài xế**:
   - Nút bấm điều hành trên chi tiết chuyến xe cho phép bấm **"Phân công tài xế"** hoặc **"Đổi tài xế"** trực tiếp sang màn hình phân công tài xế chuyên nghiệp.
4. **Quản lý & Thêm / Sửa / Xóa Loại xe (CRUD trực tiếp trên App)**:
   - Vào tab **Phương tiện** -> chọn **Quản lý loại xe**.
   - **Thêm loại xe mới:** Bấm nút **`+ Thêm loại xe`** ở góc trên -> Nhập tên loại xe (VD: `Limousine Cung Điện 24 phòng`), số chỗ ngồi (`24`), giá vé chuẩn (`260000`) -> Bấm **Lưu thông tin**.
   - **Sửa loại xe:** Bấm nút **`✏️ Sửa loại xe`** trên từng thẻ xe để cập nhật lại tên, số chỗ hoặc giá vé.
   - **Xóa loại xe:** Bấm nút **`🗑️ Xóa`** -> Hộp thoại cảnh báo xuất hiện xác nhận xóa sạch khỏi hệ thống.
   - Sau khi tạo loại xe mới, khi sang màn hình **Thêm phương tiện mới (`+`)**, loại xe mới sẽ tự động có trong danh sách lựa chọn!

---

## 🛠️ 6. Hướng dẫn sửa Database & Thêm dữ liệu mới

Khi bạn muốn thêm dữ liệu (ví dụ: thêm loại xe hoặc xe mới cho **Nhà xe Vân Anh** `NX00002` hay **Tràng An** `NX00001`), có 3 cách thực hiện:

### Cách 1: Thao tác trực tiếp trên giao diện App (Nhanh nhất)
1. Đăng nhập tài khoản nhà xe (`trangan` hoặc `vananh`).
2. Vào **Phương tiện** -> **Quản lý loại xe** -> bấm **`+ Thêm loại xe`** để tạo loại xe mới.
3. Quay lại **Phương tiện** -> bấm **`+`** để thêm xe mới: Nhập biển số, chọn loại xe vừa tạo. Xe mới tạo sẽ tự động gắn mã Nhà xe đang đăng nhập.

### Cách 2: Mở trực tiếp file SQLite Database (`database/vexe.db`)
File database chính nằm tại đường dẫn: `database/vexe.db`.
1. Cài đặt phần mềm miễn phí [DB Browser for SQLite](https://sqlitebrowser.org/).
2. Chọn **Open Database** -> Trỏ đến file `database/vexe.db`.
3. Chuyển sang tab **Execute SQL** và chạy lệnh:
   ```sql
   -- Thêm loại xe mới:
   INSERT INTO loaixe (LoaixeID, tenLoai, soCho, giaChuan) 
   VALUES ('LX00005', 'Limousine Royal 18 chỗ', 18, 230000);

   -- Thêm xe mới thuộc về Nhà xe Vân Anh (NhaxeID = NX00002):
   INSERT INTO xe (XeID, bienSo, Loaixe, Nhaxe, trangThai, soCho) 
   VALUES ('XE00009', '36B-088.99', 'LX00005', 'NX00002', 'Hoạt động', 18);
   ```
4. Nhấn **Write Changes** (Ctrl + S) để lưu lại. Khởi động lại app là dữ liệu cập nhật ngay lập tức.

### Cách 3: Sửa trong mã nguồn Backend (`backend/server.py`)
Mở file `backend/server.py`, tìm hàm `init_database`:
- **Thêm loại xe:** Tìm mảng `loaixe_data` (khoảng dòng 70) và bổ sung bản ghi mong muốn.
- **Thêm xe:** Tìm mảng `xe_data` (khoảng dòng 120), thêm dòng với mã nhà xe tương ứng (`NX00001` hoặc `NX00002`).
- **Thêm tuyến/chuyến xe:** Bổ sung vào mảng `tuyenxe_data` hoặc `chuyenxe_data`.

---

## ❓ 7. Khắc phục các sự cố thường gặp (FAQ)

#### 1. Android Studio báo lỗi XML Manifest hoặc đỏ màn hình khi Rebuild
- **Nguyên nhân:** Bộ nhớ đệm (build cache) của Android Studio lưu lại vết lỗi cũ.
- **Khắc phục:** 
  1. Trên menu Android Studio, chọn **Build** > **Clean Project**.
  2. Chọn tiếp **Build** > **Rebuild Project**.
  3. Bấm **Run 'app' ▶️** để chạy lại.

#### 2. App báo "Lỗi kết nối server!" khi bấm Đăng nhập hoặc Tìm vé
- **Khắc phục:**
  1. Kiểm tra cửa sổ dòng lệnh chạy `python backend/server.py` có đang hoạt động hay không (không được tắt).
  2. Nếu chạy trên máy ảo Android Studio, kiểm tra file `ApiClient.java` đã cấu hình `http://10.0.2.2:8000/`.
  3. Nếu chạy trên điện thoại thật, kiểm tra cả máy tính và điện thoại đã bắt chung 1 mạng Wi-Fi và cập nhật đúng địa chỉ IPv4 máy tính vào `ApiClient.java`.

#### 3. Muốn giữ lại dữ liệu vé và không bị reset khi khởi động lại server
- Kiểm tra cuối file `backend/server.py`:
  ```python
  init_database(force_reseed=False)
  ```
  Khi để `force_reseed=False`, toàn bộ vé khách đặt, tài khoản mới tạo và xe mới thêm sẽ được lưu trữ vĩnh viễn trong file SQLite `database/vexe.db`.

---

## 👨‍💻 Tác giả & Giấy phép
- Phát triển bởi **VeXeApp Team**.
- Dự án phục vụ mục đích học tập, nghiên cứu và phát triển phần mềm di động.
