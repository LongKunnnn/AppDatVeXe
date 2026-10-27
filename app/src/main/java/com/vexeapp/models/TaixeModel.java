package com.vexeapp.models;

import com.google.gson.annotations.SerializedName;

public class TaixeModel {
    @SerializedName(value = "TaixeID", alternate = {"TaiXeID", "taixeID", "id"})
    private String taixeID;
    
    @SerializedName(value = "HoTen", alternate = {"hoTen", "name"})
    private String hoTen;

    @SerializedName(value = "SoDienThoai", alternate = {"soDienThoai", "phone"})
    private String soDienThoai;

    @SerializedName(value = "HinhAnhURL", alternate = {"hinhAnhURL", "AnhDaiDien", "anhDaiDien"})
    private String hinhAnhURL;
    
    @SerializedName(value = "SoBangLai", alternate = {"soBangLai"})
    private String soBangLai;
    
    @SerializedName(value = "soCCCD", alternate = {"SoCCCD", "cccd"})
    private String soCCCD;
    
    @SerializedName(value = "LoaiBangLai", alternate = {"loaiBangLai"})
    private String loaiBangLai;
    
    @SerializedName(value = "NgayHetHanBangLai", alternate = {"ngayHetHanBangLai"})
    private String ngayHetHanBangLai;

    public String getTaixeID() { return taixeID; }
    public void setTaixeID(String taixeID) { this.taixeID = taixeID; }
    public String getHoTen() { return hoTen; }
    public void setHoTen(String hoTen) { this.hoTen = hoTen; }
    public String getSoDienThoai() { return soDienThoai; }
    public void setSoDienThoai(String soDienThoai) { this.soDienThoai = soDienThoai; }
    public String getHinhAnhURL() { return hinhAnhURL; }
    public void setHinhAnhURL(String hinhAnhURL) { this.hinhAnhURL = hinhAnhURL; }
    public String getSoBangLai() { return soBangLai; }
    public void setSoBangLai(String soBangLai) { this.soBangLai = soBangLai; }
    public String getSoCCCD() { return soCCCD; }
    public void setSoCCCD(String soCCCD) { this.soCCCD = soCCCD; }
    public String getLoaiBangLai() { return loaiBangLai; }
    public void setLoaiBangLai(String loaiBangLai) { this.loaiBangLai = loaiBangLai; }
    public String getNgayHetHanBangLai() { return ngayHetHanBangLai; }
    public void setNgayHetHanBangLai(String ngayHetHanBangLai) { this.ngayHetHanBangLai = ngayHetHanBangLai; }
}
