package com.vexeapp.models;

import com.google.gson.annotations.SerializedName;

public class Loaixe {
    @SerializedName(value = "LoaixeID", alternate = {"loaixeID", "id"})
    private String loaixeID;

    @SerializedName(value = "tenLoai", alternate = {"TenLoai", "name"})
    private String tenLoai;

    @SerializedName(value = "NgayCapNhatGia", alternate = {"ngayCapNhatGia"})
    private String ngayCapNhatGia;

    @SerializedName(value = "SoCho", alternate = {"soCho", "seats"})
    private int soCho;

    @SerializedName(value = "SoDoGheNgoiURL", alternate = {"soDoGheNgoiURL"})
    private String soDoGheNgoiURL;

    @SerializedName(value = "GiaVe", alternate = {"giaVe", "giaChuan", "price"})
    private String giaVe;

    public Loaixe() {}

    public Loaixe(String loaixeID, String ngayCapNhatGia, int soCho, String soDoGheNgoiURL, String giaVe) {
        this.loaixeID = loaixeID;
        this.ngayCapNhatGia = ngayCapNhatGia;
        this.soCho = soCho;
        this.soDoGheNgoiURL = soDoGheNgoiURL;
        this.giaVe = giaVe;
    }

    public String getLoaixeID() { return loaixeID; }
    public void setLoaixeID(String loaixeID) { this.loaixeID = loaixeID; }

    public String getTenLoai() { return tenLoai != null ? tenLoai : ("Xe " + soCho + " chỗ"); }
    public void setTenLoai(String tenLoai) { this.tenLoai = tenLoai; }

    public String getNgayCapNhatGia() { return ngayCapNhatGia; }
    public void setNgayCapNhatGia(String ngayCapNhatGia) { this.ngayCapNhatGia = ngayCapNhatGia; }

    public int getSoCho() { return soCho > 0 ? soCho : 34; }
    public void setSoCho(int soCho) { this.soCho = soCho; }

    public String getSoDoGheNgoiURL() { return soDoGheNgoiURL; }
    public void setSoDoGheNgoiURL(String soDoGheNgoiURL) { this.soDoGheNgoiURL = soDoGheNgoiURL; }

    public String getGiaVe() { return (giaVe != null && !giaVe.isEmpty()) ? giaVe : "150000"; }
    public void setGiaVe(String giaVe) { this.giaVe = giaVe; }

    public double getGiaVeDouble() {
        try {
            return Double.parseDouble(getGiaVe());
        } catch (Exception e) {
            return 150000;
        }
    }
}
