package com.vexeapp;

import com.vexeapp.api.ApiClient;
import com.vexeapp.api.ApiService;

public class RetrofitClient {
    public static ApiService getApiService() {
        return ApiClient.getClient().create(ApiService.class);
    }
}
