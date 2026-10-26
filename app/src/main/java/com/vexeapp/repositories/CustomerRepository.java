package com.vexeapp.repositories;

import com.vexeapp.models.KhachHang;
import com.vexeapp.api.ApiService;
import com.vexeapp.RetrofitClient;
import java.util.Map;
import retrofit2.Call;

public class CustomerRepository {
    private ApiService apiService;

    public CustomerRepository() {
        this.apiService = RetrofitClient.getApiService();
    }

    public Call<KhachHang> register(Map<String, String> body) {
        return apiService.register(body);
    }

    public Call<KhachHang> login(Map<String, String> body) {
        return apiService.loginWithMap(body);
    }

    public Call<KhachHang> getProfile(String id) {
        return apiService.getProfile(id);
    }

    public Call<KhachHang> updateProfile(String id, KhachHang khachHang) {
        return apiService.updateProfile(id, khachHang);
    }
}
