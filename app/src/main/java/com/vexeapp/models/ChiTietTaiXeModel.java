package com.vexeapp.models;

import com.google.gson.annotations.SerializedName;

public class ChiTietTaiXeModel {
    @SerializedName(value = "id", alternate = {"ChiTietID", "chiTietId"})
    private String id;
    
    @SerializedName(value = "HoTen", alternate = {"hoTen", "name"})
    private String hoTen;
    
    @SerializedName(value = "Tennhaxe", alternate = {"tennhaxe", "tenNhaXe", "TenNhaXe"})
    private String tennhaxe;
    
    @SerializedName(value = "NgayBatDau", alternate = {"ngayBatDau"})
    private String ngayBatDau;
    
    @SerializedName(value = "NgayKetThuc", alternate = {"ngayKetThuc"})
    private String ngayKetThuc;
    
    @SerializedName(value = "Nhaxe", alternate = {"nhaxe", "nhaXe", "NhaxeID"})
    private String nhaxe;
    
    @SerializedName(value = "Taixe", alternate = {"taixe", "TaiXe", "TaiXeID", "taiXeID"})
    private String taixe;

    public String getId() { return id != null ? id : ""; }
    public void setId(String id) { this.id = id; }
    public String getHoTen() { return hoTen; }
    public void setHoTen(String hoTen) { this.hoTen = hoTen; }
    public String getTennhaxe() { return tennhaxe; }
    public void setTennhaxe(String tennhaxe) { this.tennhaxe = tennhaxe; }
    public String getNgayBatDau() { return ngayBatDau; }
    public void setNgayBatDau(String ngayBatDau) { this.ngayBatDau = ngayBatDau; }
    public String getNgayKetThuc() { return ngayKetThuc; }
    public void setNgayKetThuc(String ngayKetThuc) { this.ngayKetThuc = ngayKetThuc; }
    public String getNhaxe() { return nhaxe; }
    public void setNhaxe(String nhaxe) { this.nhaxe = nhaxe; }
    public String getTaixe() { return taixe; }
    public String getTaiXeID() { return taixe; }
    public void setTaixe(String taixe) { this.taixe = taixe; }
}
