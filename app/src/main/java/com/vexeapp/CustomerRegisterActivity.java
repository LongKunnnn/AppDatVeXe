package com.vexeapp;

import android.app.DatePickerDialog;
import android.app.Dialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;

import com.vexeapp.api.ApiClient;
import com.vexeapp.api.ApiService;
import com.vexeapp.models.UserModel;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.Calendar;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class CustomerRegisterActivity extends AppCompatActivity {

    private EditText edtPhoneInput, edtFullName, edtDob, edtPassword, edtConfirmPassword;
    private TextView tvFileName;
    private Button btnSelectFile, btnFinish, btnCancel;
    
    private String selectedImageBase64 = "";
    private ApiService apiService;

    private final ActivityResultLauncher<Intent> pickImageLauncher =
            registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    Uri uri = result.getData().getData();
                    if (uri != null) {
                        selectedImageBase64 = encodeImageToBase64(uri);
                        tvFileName.setText("Đã chọn ảnh thành công");
                    }
                }
            });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_customer_register);

        apiService = ApiClient.getClient().create(ApiService.class);
        initViews();
        setupEvents();
    }

    private void initViews() {
        edtFullName = findViewById(R.id.edtFullName);
        edtPhoneInput = findViewById(R.id.edtPhoneInput);
        edtPassword = findViewById(R.id.edtPassword);
        edtConfirmPassword = findViewById(R.id.edtConfirmPassword);
        edtDob = findViewById(R.id.edtDob);
        tvFileName = findViewById(R.id.tvFileName);
        btnSelectFile = findViewById(R.id.btnSelectFile);
        btnFinish = findViewById(R.id.btnFinish);
        btnCancel = findViewById(R.id.btnCancel);
    }

    private void setupEvents() {
        edtDob.setOnClickListener(v -> showDatePicker());

        btnSelectFile.setOnClickListener(v -> {
            Intent intent = new Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
            pickImageLauncher.launch(intent);
        });

        btnFinish.setOnClickListener(v -> handleRegister());
        btnCancel.setOnClickListener(v -> finish());
        findViewById(R.id.btnBack).setOnClickListener(v -> finish());
    }

    private void showDatePicker() {
        Calendar cal = Calendar.getInstance();
        DatePickerDialog dp = new DatePickerDialog(this, (view, year, month, dayOfMonth) -> {
            String selected = String.format("%04d-%02d-%02d", year, (month + 1), dayOfMonth);
            edtDob.setText(selected);
        }, cal.get(Calendar.YEAR) - 20, cal.get(Calendar.MONTH), cal.get(Calendar.DAY_OF_MONTH));
        dp.show();
    }

    private String encodeImageToBase64(Uri uri) {
        try {
            InputStream is = getContentResolver().openInputStream(uri);
            Bitmap bitmap = BitmapFactory.decodeStream(is);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.JPEG, 40, baos);
            byte[] bytes = baos.toByteArray();
            return "data:image/jpeg;base64," + Base64.encodeToString(bytes, Base64.DEFAULT);
        } catch (Exception e) {
            return "";
        }
    }

    private void handleRegister() {
        String name = edtFullName.getText().toString().trim();
        String phone = edtPhoneInput.getText().toString().trim();
        String pass = edtPassword.getText().toString().trim();
        String confirmPass = edtConfirmPassword.getText().toString().trim();
        String dob = edtDob.getText().toString().trim();

        if (name.isEmpty() || phone.isEmpty() || pass.isEmpty()) {
            Toast.makeText(this, "Vui lòng nhập đầy đủ thông tin bắt buộc!", Toast.LENGTH_SHORT).show();
            return;
        }

        if (phone.length() < 9) {
            Toast.makeText(this, "Số điện thoại không hợp lệ!", Toast.LENGTH_SHORT).show();
            return;
        }

        if (pass.length() < 6) {
            Toast.makeText(this, "Mật khẩu phải từ 6 ký tự trở lên!", Toast.LENGTH_SHORT).show();
            return;
        }

        if (!pass.equals(confirmPass)) {
            Toast.makeText(this, "Xác nhận mật khẩu không khớp!", Toast.LENGTH_SHORT).show();
            return;
        }

        if (dob.isEmpty()) {
            dob = "2000-01-01";
        }

        final String finalDob = dob;
        btnFinish.setEnabled(false);

        apiService.getUsers("Get").enqueue(new Callback<List<UserModel>>() {
            @Override
            public void onResponse(Call<List<UserModel>> call, Response<List<UserModel>> res) {
                int maxNum = 0;
                boolean phoneExists = false;
                if (res.isSuccessful() && res.body() != null) {
                    for (UserModel u : res.body()) {
                        if (phone.equals(u.getSoDienThoai()) || phone.equals(u.getTenDangNhap())) {
                            phoneExists = true;
                            break;
                        }
                        try {
                            String id = u.getUserID();
                            if (id != null && id.startsWith("US")) {
                                String numOnly = id.substring(2);
                                int n = Integer.parseInt(numOnly);
                                if (n > maxNum) maxNum = n;
                            }
                        } catch (Exception e) {}
                    }
                }
                
                if (phoneExists) {
                    Toast.makeText(CustomerRegisterActivity.this, "Số điện thoại này đã được đăng ký!", Toast.LENGTH_LONG).show();
                    btnFinish.setEnabled(true);
                    return;
                }
                
                String nextUsId = String.format("US%05d", maxNum + 1);
                String nextKhId = String.format("KH%05d", maxNum + 1);
                
                createKhachHangProfile(nextUsId, nextKhId, name, finalDob, phone, pass);
            }

            @Override
            public void onFailure(Call<List<UserModel>> call, Throwable t) {
                createKhachHangProfile("US00001", "KH00001", name, finalDob, phone, pass);
            }
        });
    }

    private void createKhachHangProfile(final String usId, final String khId, final String name, String dob, final String phone, final String password) {
        Map<String, String> prof = new HashMap<>();
        prof.put("KhachHangID", khId);
        prof.put("Hovaten", name);
        prof.put("Ngaysinh", dob);
        prof.put("soDienThoai", phone);
        prof.put("AnhDaiDienURL", selectedImageBase64);
        prof.put("Email", "user" + phone + "@vexeapp.com");

        apiService.createKhachHangProfile(prof).enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                createAuthAccount(usId, khId, phone, name, password);
            }
            @Override public void onFailure(Call<Void> call, Throwable t) {
                createAuthAccount(usId, khId, phone, name, password);
            }
        });
    }

    private void createAuthAccount(final String usId, final String khId, final String phone, final String name, final String password) {
        Map<String, String> auth = new HashMap<>();
        auth.put("UserID", usId);
        auth.put("TenDangNhap", phone);
        auth.put("MatKhau", password); 
        auth.put("SoDienThoai", phone);
        auth.put("Vaitro", "KhachHang");
        auth.put("Hovaten", name);
        auth.put("KhachHangID", khId);

        apiService.registerAuth(auth).enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                btnFinish.setEnabled(true);
                showSuccessPopup(name, phone);
            }
            @Override public void onFailure(Call<Void> call, Throwable t) {
                btnFinish.setEnabled(true);
                showSuccessPopup(name, phone);
            }
        });
    }

    private void showSuccessPopup(String name, String phone) {
        final Dialog dialog = new Dialog(this);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setContentView(R.layout.dialog_success);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        }

        TextView tvMsg = dialog.findViewById(R.id.tvMessage);
        if (tvMsg != null) {
            tvMsg.setText("Đăng ký thành công!\nChào mừng " + name + "\nBạn có thể đăng nhập ngay.");
        }

        dialog.setCancelable(true);
        dialog.setCanceledOnTouchOutside(true);
        dialog.setOnDismissListener(d -> finish());
        dialog.show();

        new Handler(Looper.getMainLooper()).postDelayed(() -> {
            if (dialog.isShowing()) {
                dialog.dismiss();
            }
        }, 2200);
    }
}
