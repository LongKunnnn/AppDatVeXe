package com.vexeapp.api;

public class LoginResponse {
    private String token;
    private String username;
    private String error;
    // Thêm các trường khác tùy thuộc vào response thực tế từ Django của bạn

    public String getToken() { return token; }
    public String getUsername() { return username; }
    public String getError() { return error; }
}
