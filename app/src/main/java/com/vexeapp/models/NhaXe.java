package com.vexeapp.models;

import com.google.gson.annotations.SerializedName;
import java.io.Serializable;

public class NhaXe implements Serializable {
    @SerializedName(value = "NhaxeID", alternate = {"nhaxeID", "id", "Nhaxe"})
    private String id;

    @SerializedName(value = "Tennhaxe", alternate = {"tenNhaXe", "tennhaxe", "BusName", "busName"})
    private String busName;

    @SerializedName(value = "TenNguoiDaiDien", alternate = {"nguoiDaiDien", "tenNguoiDaiDien", "representative"})
    private String representative;

    @SerializedName(value = "Email", alternate = {"email"})
    private String email;

    @SerializedName(value = "AnhDaiDien", alternate = {"logo", "AnhDaiDienURL", "bannerUrl"})
    private String bannerUrl;

    @SerializedName(value = "DiaChiTruSo", alternate = {"diaChi", "diaChiTruSo", "address"})
    private String address;

    @SerializedName(value = "SoDienThoai", alternate = {"soDienThoai", "phone"})
    private String phone;

    public String getId() { return id != null ? id : ""; }
    public void setId(String id) { this.id = id; }

    public String getBusName() { return busName != null ? busName : "Tràng An Limousine"; }
    public void setBusName(String busName) { this.busName = busName; }

    public String getEmail() { return email != null ? email : ""; }
    public void setEmail(String email) { this.email = email; }

    public String getBannerUrl() { return bannerUrl != null ? bannerUrl : ""; }
    public void setBannerUrl(String bannerUrl) { this.bannerUrl = bannerUrl; }

    public String getAddress() { return address != null ? address : "Hà Nội"; }
    public void setAddress(String address) { this.address = address; }

    public String getPhone() { return phone != null ? phone : "19001000"; }
    public void setPhone(String phone) { this.phone = phone; }

    public String getRepresentative() { return representative != null ? representative : "Giám đốc"; }
    public void setRepresentative(String representative) { this.representative = representative; }
}
