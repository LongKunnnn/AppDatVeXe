package com.vexeapp.models;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.Map;

public class VehicleManaged implements Serializable {
    @SerializedName(value = "XeID", alternate = {"xeID", "id", "Xe"}) 
    private String XeID;

    @SerializedName(value = "BienSoXe", alternate = {"bienSo", "BienSo", "plateNumber"}) 
    private String BienSoXe;

    @SerializedName(value = "TrangThai", alternate = {"trangThai", "status", "Status"}) 
    private String TrangThai;

    @SerializedName(value = "SoGhe", alternate = {"soCho", "soGhe", "totalSeats", "seats"}) 
    private Integer SoGhe;

    @SerializedName(value = "Loaixe", alternate = {"loaixe", "loaiXe", "LoaiXe", "carType"}) 
    private Object Loaixe; 

    @SerializedName(value = "Nhaxe", alternate = {"nhaxe", "nhaXe", "NhaxeID", "nhaXeId"}) 
    private Object Nhaxe;

    public VehicleManaged() {}

    public String getXeID() { return XeID != null ? XeID : ""; }
    public void setXeID(String xeID) { this.XeID = xeID; }

    public String getBienSoXe() { return BienSoXe != null ? BienSoXe : "N/A"; }
    public void setBienSoXe(String bienSoXe) { this.BienSoXe = bienSoXe; }

    public String getTrangThai() { return TrangThai != null ? TrangThai : "Đang hoạt động"; }
    public void setTrangThai(String trangThai) { this.TrangThai = trangThai; }

    public Integer getSoGhe() { return SoGhe; }
    public void setSoGhe(Integer soGhe) { this.SoGhe = soGhe; }

    public Object getLoaixe() { return Loaixe; }
    public void setLoaixe(Object loaixe) { this.Loaixe = loaixe; }

    public Object getNhaxe() { return Nhaxe; }
    public void setNhaxe(Object nhaxe) { this.Nhaxe = nhaxe; }

    public String getLoaiXeIDStr() {
        if (Loaixe == null) return "N/A";
        if (Loaixe instanceof String) return (String) Loaixe;
        if (Loaixe instanceof Map) {
            Map<?, ?> map = (Map<?, ?>) Loaixe;
            Object name = map.get("TenLoai");
            if (name == null) name = map.get("tenLoai");
            if (name != null) return String.valueOf(name);
            Object id = map.get("LoaixeID");
            if (id == null) id = map.get("id");
            return id != null ? String.valueOf(id) : "N/A";
        }
        return String.valueOf(Loaixe);
    }
    
    public Integer getSoChoFromLoaiXe() {
        if (Loaixe instanceof Map) {
            Map<?, ?> map = (Map<?, ?>) Loaixe;
            Object soCho = map.get("SoCho");
            if (soCho == null) soCho = map.get("soCho");
            if (soCho instanceof Number) return ((Number) soCho).intValue();
        }
        return SoGhe; // Fallback về SoGhe của bảng Xe
    }
}
