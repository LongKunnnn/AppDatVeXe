package com.vexeapp.models;

public class VeResultModel {
    private String startTime, endTime, nhaXeName, price, emptySeats, carType;

    public VeResultModel(String startTime, String endTime, String nhaXeName, String price, String emptySeats, String carType) {
        this.startTime = startTime;
        this.endTime = endTime;
        this.nhaXeName = nhaXeName;
        this.price = price;
        this.emptySeats = emptySeats;
        this.carType = carType;
    }

    // Getters để Adapter lấy dữ liệu ra hiển thị
    public String getStartTime() { return startTime; }
    public String getEndTime() { return endTime; }
    public String getNhaXeName() { return nhaXeName; }
    public String getPrice() { return price; }
    public String getEmptySeats() { return emptySeats; }
    public String getCarType() { return carType; }
}
