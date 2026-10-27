package com.vexeapp.models;

import com.google.gson.annotations.SerializedName;
import java.util.List;

public class BookingRequest {
    @SerializedName(value = "ve_id", alternate = {"VeID", "veId"})
    private String veId;

    @SerializedName(value = "chuyen_xe", alternate = {"ChuyenXe", "chuyenXe", "chuyen_xe_id"})
    private String chuyenXe;
    
    @SerializedName(value = "khach_hang", alternate = {"KhachHang", "khachHang", "so_dien_thoai"})
    private String khachHang; 
    
    @SerializedName(value = "danh_sach_ghe", alternate = {"DanhSachGhe", "danhSachGhe", "ghe_ids"})
    private List<String> danhSachGhe; 
    
    @SerializedName(value = "tong_tien", alternate = {"TongTien", "tongTien"})
    private long tongTien;
    
    @SerializedName(value = "diem_don", alternate = {"DiemDon", "diemDon"})
    private String diemDon;
    
    @SerializedName(value = "diem_tra", alternate = {"DiemTra", "diemTra"})
    private String diemTra;

    public BookingRequest(String veId, String chuyenXe, String khachHang, List<String> danhSachGhe, long tongTien, 
                          String diemDon, String diemTra) {
        this.veId = veId;
        this.chuyenXe = chuyenXe;
        this.khachHang = khachHang;
        this.danhSachGhe = danhSachGhe;
        this.tongTien = tongTien;
        this.diemDon = diemDon;
        this.diemTra = diemTra;
    }
}
