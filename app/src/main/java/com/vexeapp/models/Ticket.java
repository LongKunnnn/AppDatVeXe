package com.vexeapp.models;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.List;

public class Ticket implements Serializable {
    @SerializedName(value = "VeID", alternate = {"VeHuyID", "veID", "id"})
    private String veID;

    @SerializedName(value = "TenTuyen", alternate = {"tenTuyen", "route"})
    private String tenTuyen;

    @SerializedName(value = "TenNhaXe", alternate = {"tenNhaXe", "nhaXeName"})
    private String tenNhaXe;

    @SerializedName(value = "NgayKhoiHanh", alternate = {"ngayKhoiHanh", "date"})
    private String ngayKhoiHanh;

    @SerializedName(value = "GioDi", alternate = {"gioDi", "time"})
    private String gioDi;

    @SerializedName(value = "SoLuongGhe", alternate = {"soLuongGhe", "seatCount"})
    private int soLuongGhe;

    @SerializedName(value = "DanhSachGhe", alternate = {"danhSachGhe", "seats"})
    private Object danhSachGhe;

    @SerializedName(value = "TongTien", alternate = {"tongTien", "totalPrice"})
    private double tongTien;

    @SerializedName(value = "TrangThai", alternate = {"trangThai", "status"})
    private String trangThai;

    @SerializedName(value = "TrangThaiThanhToan", alternate = {"trangThaiThanhToan", "paymentStatus"})
    private String trangThaiThanhToan;

    @SerializedName(value = "KhachHang", alternate = {"khachHang", "khachHangID", "kh_id"})
    private String khachHangID;

    @SerializedName(value = "ChuyenXe", alternate = {"Chuyenxe", "chuyenXe", "tripId"})
    private String chuyenXeID;

    public String getVeID() { return veID; }
    public String getTenTuyen() { return tenTuyen != null ? tenTuyen : "N/A"; }
    public String getTenNhaXe() { return tenNhaXe != null ? tenNhaXe : "Tràng An Limousine"; }
    public String getNgayKhoiHanh() { return ngayKhoiHanh; }
    public String getGioDi() { return gioDi; }
    public int getSoLuongGhe() { return soLuongGhe; }
    
    public double getTongTien() { return tongTien; }
    public String getTrangThai() { return trangThai != null ? trangThai : "Đã đặt"; }
    public String getTrangThaiThanhToan() { return trangThaiThanhToan != null ? trangThaiThanhToan : "Chưa thanh toán"; }
    public String getKhachHangID() { return khachHangID; }
    public String getChuyenXeID() { return chuyenXeID; }

    public void setTenTuyen(String tenTuyen) { this.tenTuyen = tenTuyen; }
    public void setTenNhaXe(String tenNhaXe) { this.tenNhaXe = tenNhaXe; }
    public void setNgayKhoiHanh(String ngayKhoiHanh) { this.ngayKhoiHanh = ngayKhoiHanh; }
    public void setGioDi(String gioDi) { this.gioDi = gioDi; }

    public String getOwnerId() {
        return (khachHangID != null) ? khachHangID.trim() : "";
    }

    public String getFormattedSeats() {
        if (danhSachGhe == null) return "N/A";
        if (danhSachGhe instanceof String) {
            return (String) danhSachGhe;
        }
        if (danhSachGhe instanceof List) {
            List<String> list = (List<String>) danhSachGhe;
            if (list.isEmpty()) return "N/A";
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < list.size(); i++) {
                sb.append(list.get(i));
                if (i < list.size() - 1) sb.append(", ");
            }
            return sb.toString();
        }
        return "N/A";
    }

    public List<String> getDanhSachGhe() {
        if (danhSachGhe instanceof List) return (List<String>) danhSachGhe;
        return null;
    }
}
