package com.vexeapp.models;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class Trip implements Serializable {
    @SerializedName(value = "ChuyenXeID", alternate = {"ChuyenxeID", "chuyenXeId", "id"})
    private String id;

    @SerializedName(value = "NgayKhoiHanh", alternate = {"ngayKhoiHanh", "date"})
    private String date;

    @SerializedName(value = "GioDi", alternate = {"gioDi", "time", "startTime"})
    private String startTime;

    @SerializedName(value = "GioDen", alternate = {"gioDen", "endTime"})
    private String endTime;

    @SerializedName(value = "TrangThai", alternate = {"trangThai", "status"})
    private String status;

    @SerializedName(value = "Xe", alternate = {"xe", "XeID", "xeID"})
    private String xe; 

    @SerializedName(value = "TuyenXe", alternate = {"Tuyenxe", "tuyenXeID", "tuyen", "TuyenxeID"})
    private String tuyen; 

    @SerializedName(value = "Taixe", alternate = {"TaiXe", "TaiXeID", "taixe", "taiXeID"})
    private String taiXeID;

    @SerializedName(value = "TenTaiXe", alternate = {"tenTaiXe", "driverName"})
    private String tenTaiXe;

    @SerializedName(value = "BienSo", alternate = {"bienSo", "bienSoXe", "BienSoXe", "plateNumber"})
    private String bienSo;

    @SerializedName(value = "DiemDi", alternate = {"diemDi", "startPoint"})
    private String diemDi;

    @SerializedName(value = "DiemDen", alternate = {"diemDen", "endPoint"})
    private String diemDen;

    @SerializedName(value = "TenTuyen", alternate = {"tenTuyen", "tuyenXeName", "routeName"})
    private String tenTuyen;

    @SerializedName(value = "LoaiXe", alternate = {"loaiXe", "carType", "loaiXeTen"})
    private String loaiXe;

    @SerializedName(value = "GiaVe", alternate = {"giaVe", "price"})
    private String giaVe;

    @SerializedName(value = "TenNhaXe", alternate = {"tenNhaXe", "nhaXeName"})
    private String tenNhaXe;

    @SerializedName(value = "SoChoTrong", alternate = {"soChoTrong", "soCho", "totalSeats", "availableSeats"})
    private Integer soChoTrong;

    @SerializedName(value = "ThoiGian", alternate = {"thoiGian", "thoiGianUocTinh", "duration"})
    private String duration;

    @SerializedName(value = "Nhaxe", alternate = {"nhaxe", "nhaXeId", "NhaxeID"})
    private String nhaXeId;

    private int seats = 4;
    private Driver assignedDriver;
    private List<Passenger> passengers = new ArrayList<>();

    public Trip() {}

    public Trip(String id, String tuyen, String date, String startTime, String status) {
        this.id = id;
        this.tuyen = tuyen;
        this.date = date;
        this.startTime = startTime;
        this.status = status;
    }

    public String getId() { return id != null ? id : ""; }
    public void setId(String id) { this.id = id; }

    public String getDate() { return date != null ? date : ""; }
    public void setDate(String date) { this.date = date; }

    public String getTime() { return startTime != null ? startTime : "00:00"; }
    public void setTime(String startTime) { this.startTime = startTime; }

    public String getEndTime() { return endTime != null ? endTime : (startTime != null ? startTime : ""); }
    public void setEndTime(String endTime) { this.endTime = endTime; }

    public String getStatus() { return status != null ? status : "Chưa hoàn thành"; }
    public void setStatus(String status) { this.status = status; }

    public String getXeID() { return xe != null ? xe : ""; }
    public void setXeID(String xe) { this.xe = xe; }

    public String getTuyenXeID() { return tuyen != null ? tuyen : ""; }
    public void setTuyenXeID(String tuyen) { this.tuyen = tuyen; }

    public String getTaiXeID() { return taiXeID != null ? taiXeID : ""; }
    public void setTaiXeID(String taiXeID) { this.taiXeID = taiXeID; }

    public String getNhaXeId() { return nhaXeId != null ? nhaXeId : ""; }
    public void setNhaXeId(String nhaXeId) { this.nhaXeId = nhaXeId; }

    public String getDuration() { return duration != null ? duration : "2h"; }
    public void setDuration(String duration) { this.duration = duration; }

    public String getRouteName() {
        return (tenTuyen != null && !tenTuyen.isEmpty()) ? tenTuyen : "Tuyến: " + getTuyenXeID();
    }

    public String getVehicleType() {
        return (loaiXe != null && !loaiXe.isEmpty()) ? loaiXe : "Xe: " + getXeID();
    }

    public void setRouteName(String routeName) { this.tenTuyen = routeName; }
    public void setVehicleType(String vehicleType) { this.loaiXe = vehicleType; }

    public String getPrice() { return giaVe != null ? giaVe : "0"; }
    public void setPrice(String price) { this.giaVe = price; }

    public String getTenTuyen() { return tenTuyen; }
    public void setTenTuyen(String tenTuyen) { this.tenTuyen = tenTuyen; }

    public String getLoaiXe() { return loaiXe; }
    public void setLoaiXe(String loaiXe) { this.loaiXe = loaiXe; }

    public String getGiaVe() { return giaVe; }
    public void setGiaVe(String giaVe) { this.giaVe = giaVe; }

    public String getTenNhaXe() { return (tenNhaXe != null && !tenNhaXe.isEmpty() && !tenNhaXe.equalsIgnoreCase("Nhà xe")) ? tenNhaXe : "Tràng An Limousine"; }
    public void setTenNhaXe(String tenNhaXe) { this.tenNhaXe = tenNhaXe; }

    public Integer getSoChoTrong() { return soChoTrong; }
    public void setSoChoTrong(Integer soChoTrong) { this.soChoTrong = soChoTrong; }

    public int getSeats() {
        if (soChoTrong != null) return soChoTrong;
        return seats;
    }
    public void setSeats(int seats) { 
        this.seats = seats; 
        this.soChoTrong = seats;
    }

    public String getTenTaiXe() { return tenTaiXe != null ? tenTaiXe : ""; }
    public void setTenTaiXe(String tenTaiXe) { this.tenTaiXe = tenTaiXe; }

    public String getBienSo() { return bienSo != null ? bienSo : ""; }
    public void setBienSo(String bienSo) { this.bienSo = bienSo; }

    public String getDiemDi() { return diemDi != null ? diemDi : ""; }
    public void setDiemDi(String diemDi) { this.diemDi = diemDi; }

    public String getDiemDen() { return diemDen != null ? diemDen : ""; }
    public void setDiemDen(String diemDen) { this.diemDen = diemDen; }

    public Driver getAssignedDriver() { return assignedDriver; }
    public void setAssignedDriver(Driver assignedDriver) { this.assignedDriver = assignedDriver; }

    public List<Passenger> getPassengers() { return passengers; }
    public void setPassengers(List<Passenger> passengers) { this.passengers = passengers; }
}
