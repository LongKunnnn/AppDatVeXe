package com.vexeapp.api;

import okhttp3.OkHttpClient;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import java.util.concurrent.TimeUnit;

public class ApiClient {
    // =========================================================================
    // CẤU HÌNH ĐỊA CHỈ BACKEND SERVER (BASE_URL):
    // 1. Chạy Server Python trên máy tính & test trên MÁY ẢO Android Emulator:
    //    public static final String BASE_URL = "http://10.0.2.2:8000/";
    //
    // 2. Chạy Server Python trên máy tính & test trên ĐIỆN THOẠI THẬT (cùng Wi-Fi):
    //    public static final String BASE_URL = "http://<IP_MÁY_TÍNH>:8000/"; (VD: http://192.168.1.15:8000/)
    //
    // 3. Sử dụng Cloud Server Render (Server online cũ):
    //    public static final String BASE_URL = "https://api-vexeapp.onrender.com/";
    // =========================================================================
    
    // Đã cấu hình sẵn để kết nối Server Python cục bộ trên máy ảo Android Emulator:
    public static final String BASE_URL = "http://10.0.2.2:8000/";
    
    private static Retrofit retrofit = null;

    public static Retrofit getClient() {
        if (retrofit == null) {
            OkHttpClient okHttpClient = new OkHttpClient.Builder()
                    .connectTimeout(30, TimeUnit.SECONDS)
                    .readTimeout(30, TimeUnit.SECONDS)
                    .writeTimeout(30, TimeUnit.SECONDS)
                    .build();

            retrofit = new Retrofit.Builder()
                    .baseUrl(BASE_URL)
                    .client(okHttpClient)
                    .addConverterFactory(GsonConverterFactory.create())
                    .build();
        }
        return retrofit;
    }
}
