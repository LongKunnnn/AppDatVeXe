package com.vexeapp.models;

import com.google.gson.annotations.SerializedName;

public class Seat {
    @SerializedName(value = "gheID", alternate = {"GheID", "id"})
    private String id;
    
    @SerializedName(value = "soGhe", alternate = {"SoGhe", "seatCode"})
    private String seatCode;
    
    @SerializedName(value = "trangThai", alternate = {"TrangThai", "status"})
    private String status;

    @SerializedName(value = "ChuyenXe", alternate = {"Chuyenxe", "chuyenXe", "chuyen_xe"})
    private String chuyenXe;

    @SerializedName(value = "VeID", alternate = {"veID", "ticketId"})
    private String ticketId;

    public String getId() { return id; }
    public String getSeatCode() { return seatCode; }
    public String getStatus() { return status; }
    public String getChuyenXe() { return chuyenXe; }
    public String getTicketId() { return ticketId; }
    
    public void setStatus(String status) { this.status = status; }
    public void setTicketId(String ticketId) { this.ticketId = ticketId; }
}
