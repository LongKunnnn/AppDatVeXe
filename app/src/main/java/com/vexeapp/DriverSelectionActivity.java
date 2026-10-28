package com.vexeapp;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.provider.MediaStore;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;
import com.vexeapp.adapters.DriverAdapter;
import com.vexeapp.api.ApiClient;
import com.vexeapp.api.ApiService;
import com.vexeapp.models.ChiTietTaiXeModel;
import com.vexeapp.models.Driver;
import com.vexeapp.models.TaixeModel;
import com.vexeapp.models.UserModel;

import java.io.ByteArrayOutputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Locale;
import java.util.regex.Pattern;

import de.hdodenhof.circleimageview.CircleImageView;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class DriverSelectionActivity extends AppCompatActivity implements DriverAdapter.OnDriverListener {

    private RecyclerView rvDrivers;
    private DriverAdapter adapter;
    private List<Driver> driverList = new ArrayList<>();
    private ApiService apiService;
    private ImageView btnBack;
    private Button btnCreateAccount;
    private LinearLayout layoutScheduleMonitoring;

    private CircleImageView currentDialogImg;
    private String selectedImageBase64 = "";

    private final ActivityResultLauncher<String> pickImageLauncher = registerForActivityResult(
            new ActivityResultContracts.GetContent(),
            uri -> {
                if (uri != null) {
                    if (currentDialogImg != null) {
                        currentDialogImg.setImageURI(uri);
                    }
                    selectedImageBase64 = encodeImageToBase64(uri);
                }
            }
    );

    private final ActivityResultLauncher<Intent> createDriverLauncher = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
            result -> loadRealData()
    );

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_driver_selection);

        apiService = ApiClient.getClient().create(ApiService.class);
        initViews();

        btnBack.setOnClickListener(v -> finish());
        btnCreateAccount.setOnClickListener(v -> {
            Intent intent = new Intent(this, CreateDriverAccountActivity.class);
            createDriverLauncher.launch(intent);
        });

        layoutScheduleMonitoring.setOnClickListener(v -> {
            Intent intent = new Intent(this, DriverScheduleMonitoringActivity.class);
            startActivity(intent);
        });

        setupBottomNavigation();
        loadRealData();
    }

    private void initViews() {
        rvDrivers = findViewById(R.id.rvDrivers);
        btnBack = findViewById(R.id.btnBack);
        btnCreateAccount = findViewById(R.id.btnCreateAccount);
        layoutScheduleMonitoring = findViewById(R.id.layoutScheduleMonitoring);

        rvDrivers.setLayoutManager(new LinearLayoutManager(this));
        adapter = new DriverAdapter(driverList, this);
        rvDrivers.setAdapter(adapter);
    }

    private void setupBottomNavigation() {
        // Trang chủ -> OperatorMainActivity
        View navHome = findViewById(R.id.nav_home_op_main);
        if (navHome != null) {
            navHome.setOnClickListener(v -> {
                Intent intent = new Intent(this, OperatorMainActivity.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                startActivity(intent);
            });
        }

        // Phương tiện -> PhuongTienManagementActivity
        View navVehicle = findViewById(R.id.nav_vehicle_op);
        if (navVehicle != null) {
            navVehicle.setOnClickListener(v -> {
                Intent intent = new Intent(this, PhuongTienManagementActivity.class);
                startActivity(intent);
            });
        }

        // Chuyến xe -> TripListActivity
        View navTrip = findViewById(R.id.nav_trip_op);
        if (navTrip != null) {
            navTrip.setOnClickListener(v -> startActivity(new Intent(this, TripListActivity.class)));
        }

        // Tuyến xe -> QLTuyenxeActivity
        View navRoute = findViewById(R.id.nav_route_op);
        if (navRoute != null) {
            navRoute.setOnClickListener(v -> startActivity(new Intent(this, QLTuyenxeActivity.class)));
        }
    }

    private void loadRealData() {
        android.content.SharedPreferences pref = getSharedPreferences("UserPrefs", MODE_PRIVATE);
        String currentOpUid = pref.getString("nhaxe_id", null);
        if (currentOpUid == null || currentOpUid.isEmpty() || "null".equalsIgnoreCase(currentOpUid)) {
            currentOpUid = pref.getString("op_uid", "NX00001");
        }
        final String targetOp = currentOpUid;

        apiService.getChiTietTaiXe().enqueue(new Callback<List<Map<String, Object>>>() {
            @Override
            public void onResponse(Call<List<Map<String, Object>>> call, Response<List<Map<String, Object>>> response) {
                if (response.isSuccessful() && response.body() != null && !response.body().isEmpty()) {
                    driverList.clear();
                    for (Map<String, Object> map : response.body()) {
                        String nxe = findVal(map, "Nhaxe", "nhaxe", "NhaxeID", "nhaxe_id");
                        if (!nxe.isEmpty() && !nxe.equalsIgnoreCase(targetOp)) {
                            continue; // Bỏ qua tài xế của nhà xe khác
                        }
                        String id = findVal(map, "TaiXe", "Taixe", "TaiXeID", "TaixeID", "id");
                        String name = findVal(map, "HoTen", "hoten", "name");
                        String phone = findVal(map, "SoDienThoai", "sodienthoai", "phone");
                        String avatar = findVal(map, "AnhDaiDien", "HinhAnhURL", "avatar");
                        if (phone.isEmpty()) phone = "Chưa cập nhật";
                        if (!id.isEmpty() || !name.isEmpty()) {
                            driverList.add(new Driver(id.isEmpty() ? "TX00001" : id, name.isEmpty() ? id : name, phone, avatar));
                        }
                    }
                    adapter.notifyDataSetChanged();
                } else {
                    fallbackLoadDrivers();
                }
            }

            @Override
            public void onFailure(Call<List<Map<String, Object>>> call, Throwable t) {
                fallbackLoadDrivers();
            }
        });
    }

    private void fallbackLoadDrivers() {
        android.content.SharedPreferences pref = getSharedPreferences("UserPrefs", MODE_PRIVATE);
        String currentOpUid = pref.getString("nhaxe_id", null);
        if (currentOpUid == null || currentOpUid.isEmpty() || "null".equalsIgnoreCase(currentOpUid)) {
            currentOpUid = pref.getString("op_uid", "NX00001");
        }
        final String targetOp = currentOpUid;

        apiService.getDriversRaw().enqueue(new Callback<List<Map<String, Object>>>() {
            @Override
            public void onResponse(Call<List<Map<String, Object>>> call, Response<List<Map<String, Object>>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    driverList.clear();
                    for (Map<String, Object> map : response.body()) {
                        String nxe = findVal(map, "Nhaxe", "nhaxe", "NhaxeID");
                        if (!nxe.isEmpty() && !nxe.equalsIgnoreCase(targetOp)) {
                            continue;
                        }
                        String id = findVal(map, "TaiXeID", "TaixeID", "TaiXe", "id");
                        String name = findVal(map, "HoTen", "hoten");
                        String phone = findVal(map, "SoDienThoai", "phone");
                        String avatar = findVal(map, "AnhDaiDien", "HinhAnhURL");
                        driverList.add(new Driver(id, name, phone, avatar));
                    }
                    adapter.notifyDataSetChanged();
                }
            }
            @Override public void onFailure(Call<List<Map<String, Object>>> call, Throwable t) {}
        });
    }

    private String findVal(Map<String, Object> map, String... keys) {
        if (map == null) return "";
        for (String k : keys) {
            for (Map.Entry<String, Object> e : map.entrySet()) {
                if (e.getKey().equalsIgnoreCase(k) && e.getValue() != null) return e.getValue().toString();
            }
        }
        return "";
    }

    @Override
    public void onDriverClick(Driver driver) {
        showDriverDetailDialog(driver);
    }

    @Override
    public void onDriverDelete(Driver driver) {
        showDeleteConfirmDialog(driver);
    }

    private void showDriverDetailDialog(Driver driver) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        View view = LayoutInflater.from(this).inflate(R.layout.dialog_driver_detail, null);

        TextView tvTitle = view.findViewById(R.id.tvDialogTitle);
        EditText edtName = view.findViewById(R.id.edtName);
        EditText edtPhone = view.findViewById(R.id.edtPhone);
        EditText edtCCCD = view.findViewById(R.id.edtCCCD);
        EditText edtLicense = view.findViewById(R.id.edtLicense);
        EditText edtType = view.findViewById(R.id.edtType);
        EditText edtExpiry = view.findViewById(R.id.edtExpiry);
        Button btnAction = view.findViewById(R.id.btnAction);
        Button btnDialogCancel = view.findViewById(R.id.btnDialogCancel);
        ImageView btnDialogClose = view.findViewById(R.id.btnDialogClose);
        
        currentDialogImg = view.findViewById(R.id.imgDialogDriver);
        TextView btnChangeImage = view.findViewById(R.id.btnChangeImage);

        tvTitle.setText("Thông tin tài xế");
        edtName.setText(driver.getName());
        edtPhone.setText(driver.getPhone());
        selectedImageBase64 = "";

        final TaixeModel[] currentTaixe = {null};
        final ChiTietTaiXeModel[] currentChiTiet = {null};
        final UserModel[] currentUser = {null};

        apiService.getTaixeList("Get").enqueue(new Callback<List<TaixeModel>>() {
            @Override
            public void onResponse(Call<List<TaixeModel>> call, Response<List<TaixeModel>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    for (TaixeModel m : response.body()) {
                        if (m != null && m.getTaixeID() != null && m.getTaixeID().equalsIgnoreCase(driver.getId())) {
                            currentTaixe[0] = m;
                            edtCCCD.setText(m.getSoCCCD());
                            edtLicense.setText(m.getSoBangLai());
                            edtType.setText(m.getLoaiBangLai());
                            String expiryDate = m.getNgayHetHanBangLai();
                            if (expiryDate != null && expiryDate.contains("T")) expiryDate = expiryDate.split("T")[0];
                            edtExpiry.setText(expiryDate);
                            
                            if (m.getHinhAnhURL() != null && !m.getHinhAnhURL().isEmpty()) {
                                Glide.with(DriverSelectionActivity.this).load(m.getHinhAnhURL()).placeholder(R.drawable.account_circle).into(currentDialogImg);
                            }
                            break;
                        }
                    }
                }
            }
            @Override public void onFailure(Call<List<TaixeModel>> call, Throwable t) {}
        });

        apiService.getChiTietTaiXeList("Get").enqueue(new Callback<List<ChiTietTaiXeModel>>() {
            @Override
            public void onResponse(Call<List<ChiTietTaiXeModel>> call, Response<List<ChiTietTaiXeModel>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    for (ChiTietTaiXeModel ct : response.body()) {
                        if (ct != null && ct.getTaixe() != null && ct.getTaixe().equalsIgnoreCase(driver.getId())) {
                            currentChiTiet[0] = ct;
                            break;
                        }
                    }
                }
            }
            @Override public void onFailure(Call<List<ChiTietTaiXeModel>> call, Throwable t) {}
        });

        apiService.getUsers("Get").enqueue(new Callback<List<UserModel>>() {
            @Override
            public void onResponse(Call<List<UserModel>> call, Response<List<UserModel>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    for (UserModel u : response.body()) {
                        if (u != null && u.getTaixe() != null && u.getTaixe().equalsIgnoreCase(driver.getId())) {
                            currentUser[0] = u;
                            break;
                        }
                    }
                }
            }
            @Override public void onFailure(Call<List<UserModel>> call, Throwable t) {}
        });

        setAllFieldsDisabled(view);
        btnAction.setText("Sửa thông tin");
        btnChangeImage.setVisibility(View.GONE);

        AlertDialog dialog = builder.setView(view).create();
        if (dialog.getWindow() != null) dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);

        btnDialogClose.setOnClickListener(v -> dialog.dismiss());
        btnDialogCancel.setOnClickListener(v -> dialog.dismiss());
        btnChangeImage.setOnClickListener(v -> pickImageLauncher.launch("image/*"));

        btnAction.setOnClickListener(v -> {
            if (btnAction.getText().toString().equals("Sửa thông tin")) {
                tvTitle.setText("Sửa thông tin tài xế");
                enableEditFields(view);
                btnAction.setText("Lưu thay đổi");
                btnChangeImage.setVisibility(View.VISIBLE);
            } else {
                if (validateEditInput(view)) {
                    handleFullUpdate(view, driver, dialog, currentTaixe[0], currentChiTiet[0], currentUser[0]);
                }
            }
        });

        dialog.show();
    }

    private boolean validateEditInput(View view) {
        EditText edtName = view.findViewById(R.id.edtName);
        EditText edtPhone = view.findViewById(R.id.edtPhone);
        EditText edtLicense = view.findViewById(R.id.edtLicense);
        EditText edtType = view.findViewById(R.id.edtType);
        EditText edtExpiry = view.findViewById(R.id.edtExpiry);

        boolean isValid = true;

        if (edtName.getText().toString().trim().isEmpty()) {
            edtName.setError("Vui lòng nhập Họ tên tài xế.");
            isValid = false;
        }

        String phone = edtPhone.getText().toString().trim();
        if (phone.isEmpty()) {
            edtPhone.setError("Vui lòng nhập Số điện thoại.");
            isValid = false;
        } else if (!Pattern.compile("^\\d{10}$").matcher(phone).matches()) {
            edtPhone.setError("Số điện thoại phải có 10 ký tự số.");
            isValid = false;
        }

        if (edtLicense.getText().toString().trim().isEmpty()) {
            edtLicense.setError("Vui lòng nhập Số bằng lái.");
            isValid = false;
        }

        if (edtType.getText().toString().trim().isEmpty()) {
            edtType.setError("Vui lòng nhập Loại bằng lái.");
            isValid = false;
        }

        String expiryDate = edtExpiry.getText().toString().trim();
        if (expiryDate.isEmpty()) {
            edtExpiry.setError("Vui lòng nhập Ngày hết hạn.");
            isValid = false;
        } else {
            try {
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());
                Date date = sdf.parse(expiryDate);
                if (date != null && date.before(new Date())) {
                    edtExpiry.setError("Ngày hết hạn phải lớn hơn hiện tại.");
                    isValid = false;
                }
            } catch (Exception e) {
                isValid = false;
            }
        }

        return isValid;
    }

    private void enableEditFields(View view) {
        int[] ids = {R.id.edtName, R.id.edtPhone, R.id.edtLicense, R.id.edtType, R.id.edtExpiry};
        for (int id : ids) {
            View v = view.findViewById(id);
            if (v != null) { v.setEnabled(true); v.setAlpha(1.0f); }
        }
        View cccd = view.findViewById(R.id.edtCCCD);
        if (cccd != null) { cccd.setEnabled(false); cccd.setAlpha(0.5f); }
    }

    private void handleFullUpdate(View view, Driver driver, AlertDialog dialog, TaixeModel tx, ChiTietTaiXeModel ct, UserModel u) {
        if (tx == null) { Toast.makeText(this, "Đang tải dữ liệu, vui lòng đợi", Toast.LENGTH_SHORT).show(); return; }

        EditText edtName = view.findViewById(R.id.edtName);
        EditText edtPhone = view.findViewById(R.id.edtPhone);
        EditText edtLicense = view.findViewById(R.id.edtLicense);
        EditText edtType = view.findViewById(R.id.edtType);
        EditText edtExpiry = view.findViewById(R.id.edtExpiry);

        tx.setSoBangLai(edtLicense.getText().toString());
        tx.setLoaiBangLai(edtType.getText().toString());
        tx.setNgayHetHanBangLai(edtExpiry.getText().toString());
        if (!selectedImageBase64.isEmpty()) {
            tx.setHinhAnhURL(selectedImageBase64);
        }

        apiService.updateTaixe(driver.getId(), tx).enqueue(new Callback<TaixeModel>() {
            @Override
            public void onResponse(Call<TaixeModel> call, Response<TaixeModel> response) {
                if (response.isSuccessful()) {
                    if (ct != null) {
                        ct.setHoTen(edtName.getText().toString());
                        apiService.updateChiTietTaiXe(ct.getId().toString(), ct).enqueue(new Callback<ChiTietTaiXeModel>() {
                            @Override public void onResponse(Call<ChiTietTaiXeModel> call, Response<ChiTietTaiXeModel> res) {}
                            @Override public void onFailure(Call<ChiTietTaiXeModel> call, Throwable t) {}
                        });
                    }
                    if (u != null) {
                        u.setSoDienThoai(edtPhone.getText().toString());
                        apiService.updateUser(u.getUserID(), u).enqueue(new Callback<UserModel>() {
                            @Override public void onResponse(Call<UserModel> call, Response<UserModel> res) {}
                            @Override public void onFailure(Call<UserModel> call, Throwable t) {}
                        });
                    }
                    dialog.dismiss();
                    showUpdateSuccessPopup();
                    new Handler().postDelayed(() -> loadRealData(), 500);
                } else {
                    Toast.makeText(DriverSelectionActivity.this, "Server từ chối cập nhật dữ liệu.", Toast.LENGTH_LONG).show();
                }
            }
            @Override public void onFailure(Call<TaixeModel> call, Throwable t) { Toast.makeText(DriverSelectionActivity.this, "Lỗi kết nối", Toast.LENGTH_SHORT).show(); }
        });
    }

    private String encodeImageToBase64(Uri imageUri) {
        try {
            Bitmap bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), imageUri);
            Bitmap resizedBitmap = Bitmap.createScaledBitmap(bitmap, 200, 200, true);
            ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
            resizedBitmap.compress(Bitmap.CompressFormat.JPEG, 50, outputStream);
            byte[] byteArray = outputStream.toByteArray();
            return "data:image/jpeg;base64," + Base64.encodeToString(byteArray, Base64.DEFAULT);
        } catch (Exception e) {
            return "";
        }
    }

    private void showUpdateSuccessPopup() {
        View dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_update_driver_success, null);
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setView(dialogView);
        final AlertDialog dialog = builder.create();
        if (dialog.getWindow() != null) dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        dialog.show();
        new Handler().postDelayed(() -> { if (dialog.isShowing()) dialog.dismiss(); }, 2000);
    }

    private void showDeleteConfirmDialog(Driver driver) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        View view = LayoutInflater.from(this).inflate(R.layout.dialog_confirm_delete, null);
        TextView tvTitle = view.findViewById(R.id.tvDialogTitle);
        TextView tvMsg = view.findViewById(R.id.tvDialogMessage);
        Button btnNo = view.findViewById(R.id.btnNo);
        Button btnYes = view.findViewById(R.id.btnYes);
        tvTitle.setText("Xác nhận xóa tài xế");
        tvMsg.setText("Bạn có chắc chắn muốn xóa tài khoản\ncủa tài xế " + driver.getName() + "?\nHành động này không thể hoàn tác");
        final AlertDialog dialog = builder.setView(view).create();
        if (dialog.getWindow() != null) dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        btnNo.setOnClickListener(v -> dialog.dismiss());
        btnYes.setOnClickListener(v -> {
            apiService.deleteTaixe(driver.getId()).enqueue(new Callback<Void>() {
                @Override public void onResponse(Call<Void> call, Response<Void> response) {
                    if (response.isSuccessful()) {
                        dialog.dismiss();
                        showDeleteSuccessPopup();
                        loadRealData();
                    }
                }
                @Override public void onFailure(Call<Void> call, Throwable t) { Toast.makeText(DriverSelectionActivity.this, "Lỗi khi xóa", Toast.LENGTH_SHORT).show(); }
            });
        });
        dialog.show();
    }

    private void showDeleteSuccessPopup() {
        View dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_delete_driver_success, null);
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setView(dialogView);
        final AlertDialog dialog = builder.create();
        if (dialog.getWindow() != null) dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        dialog.show();
        new Handler().postDelayed(() -> { if (dialog.isShowing()) dialog.dismiss(); }, 2000);
    }

    private void setAllFieldsDisabled(View v) {
        int[] ids = {R.id.edtName, R.id.edtPhone, R.id.edtCCCD, R.id.edtLicense, R.id.edtType, R.id.edtExpiry};
        for (int id : ids) {
            View view = v.findViewById(id);
            if (view != null) { view.setEnabled(false); view.setAlpha(0.8f); }
        }
    }
}
