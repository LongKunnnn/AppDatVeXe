with open("app/src/main/java/com/vexeapp/api/ApiService.java", "r", encoding="utf-8") as f:
    content = f.read()

target = """    @PUT("api/loaixe/{id}/")
    Call<Loaixe> updateLoaixe(@Path("id") String id, @Body Loaixe loaixe);"""

replacement = """    @POST("api/loaixe/")
    Call<Loaixe> createLoaixe(@Body Loaixe loaixe);

    @PUT("api/loaixe/{id}/")
    Call<Loaixe> updateLoaixe(@Path("id") String id, @Body Loaixe loaixe);

    @DELETE("api/loaixe/{id}/")
    Call<Void> deleteLoaixe(@Path("id") String id);

    @POST("api/thanh-toan-ve/")
    Call<Void> thanhToanVe(@Body Map<String, Object> data);

    @POST("api/xac-nhan-ve/")
    Call<Void> xacNhanVe(@Body Map<String, Object> data);"""

assert target in content, "target not found in ApiService.java"
content = content.replace(target, replacement, 1)

with open("app/src/main/java/com/vexeapp/api/ApiService.java", "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: ApiService.java updated!")

