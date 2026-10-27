package com.vexeapp.models;

import com.google.gson.annotations.SerializedName;

public class KhachHang {
    @SerializedName(value = "KhachHangID", alternate = {"khachHangID", "id", "KhachHang"})
    private String khachHangID;

    @SerializedName(value = "Hovaten", alternate = {"hoTen", "hovaten", "name"})
    private String hoTen;

    @SerializedName(value = "Email", alternate = {"email"})
    private String email;

    @SerializedName(value = "Ngaysinh", alternate = {"ngaysinh", "ngaySinh"})
    private String ngaySinh;

    @SerializedName(value = "soDienThoai", alternate = {"SoDienThoai", "phone"})
    private String soDienThoai;

    @SerializedName(value = "AnhDaiDienURL", alternate = {"anhDaiDienURL", "avatar"})
    private String anhDaiDienURL;

    @SerializedName(value = "NgayDangKy", alternate = {"ngayDangKy"})
    private String ngayDangKy;

    public String getKhachHangID() { return khachHangID != null ? khachHangID : ""; }
    public void setKhachHangID(String khachHangID) { this.khachHangID = khachHangID; }

    public String getHoTen() { return (hoTen != null && !hoTen.isEmpty()) ? hoTen : "Khách hàng"; }
    public void setHoTen(String hoTen) { this.hoTen = hoTen; }

    public String getEmail() { return email != null ? email : ""; }
    public void setEmail(String email) { this.email = email; }

    public String getNgaySinh() { return (ngaySinh != null && !ngaySinh.isEmpty()) ? ngaySinh : "Chưa cập nhật"; }
    public void setNgaySinh(String ngaySinh) { this.ngaySinh = ngaySinh; }

    public String getSoDienThoai() { return soDienThoai != null ? soDienThoai : ""; }
    public void setSoDienThoai(String soDienThoai) { this.soDienThoai = soDienThoai; }

    public String getAnhDaiDienURL() { return anhDaiDienURL != null ? anhDaiDienURL : ""; }
    public void setAnhDaiDienURL(String anhDaiDienURL) { this.anhDaiDienURL = anhDaiDienURL; }

    public String getNgayDangKy() { return ngayDangKy != null ? ngayDangKy : ""; }
}
