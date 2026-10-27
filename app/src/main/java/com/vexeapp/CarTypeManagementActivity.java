package com.vexeapp;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.vexeapp.adapters.CarTypeAdapter;
import com.vexeapp.api.ApiClient;
import com.vexeapp.api.ApiService;
import com.vexeapp.models.Loaixe;

import java.util.ArrayList;
import java.util.List;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class CarTypeManagementActivity extends AppCompatActivity {

    private RecyclerView rvCarTypes;
    private CarTypeAdapter adapter;
    private List<Loaixe> carTypeList;
    private ImageView btnBack, btnProfile;
    private android.widget.Button btnAddCarType;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car_type_management);

        initViews();
        setupRecyclerView();
        fetchCarTypes(); 
        setupEvents();
        setupBottomNav();
    }

    private void initViews() {
        rvCarTypes = findViewById(R.id.rvCarTypes);
        btnBack = findViewById(R.id.btnBack);
        btnProfile = findViewById(R.id.btnProfile);
        if (btnProfile == null) btnProfile = findViewById(R.id.imgOpProfile);
        btnAddCarType = findViewById(R.id.btnAddCarType);
    }

    private void setupEvents() {
        if (btnBack != null) {
            btnBack.setOnClickListener(v -> finish());
        }
        if (btnProfile != null) {
            btnProfile.setOnClickListener(v -> {
                startActivity(new Intent(this, OperatorProfileActivity.class));
            });
        }
        if (btnAddCarType != null) {
            btnAddCarType.setOnClickListener(v -> showAddCarTypeDialog());
        }
    }

    private void setupRecyclerView() {
        carTypeList = new ArrayList<>();
        adapter = new CarTypeAdapter(carTypeList, this);
        rvCarTypes.setLayoutManager(new LinearLayoutManager(this));
        rvCarTypes.setAdapter(adapter);
    }

    private void showAddCarTypeDialog() {
        android.app.Dialog dialog = new android.app.Dialog(this);
        dialog.setContentView(R.layout.dialog_crud_car_type);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT));
        }

        android.widget.TextView tvTitle = dialog.findViewById(R.id.tvCrudDialogTitle);
        android.widget.EditText edtName = dialog.findViewById(R.id.edtCrudName);
        android.widget.EditText edtSeats = dialog.findViewById(R.id.edtCrudSeats);
        android.widget.EditText edtPrice = dialog.findViewById(R.id.edtCrudPrice);
        android.widget.Button btnSave = dialog.findViewById(R.id.btnSaveCrud);
        android.widget.Button btnCancel = dialog.findViewById(R.id.btnCancelCrud);
        android.widget.ImageView btnCloseTop = dialog.findViewById(R.id.btnCloseCrudTop);

        if (tvTitle != null) tvTitle.setText("Thêm loại xe mới");

        if (btnCloseTop != null) btnCloseTop.setOnClickListener(v -> dialog.dismiss());
        if (btnCancel != null) btnCancel.setOnClickListener(v -> dialog.dismiss());

        if (btnSave != null) {
            btnSave.setOnClickListener(v -> {
                String nameInput = edtName.getText().toString().trim();
                String seatsInput = edtSeats.getText().toString().trim();
                String priceInput = edtPrice.getText().toString().trim();

                if (nameInput.isEmpty() || seatsInput.isEmpty() || priceInput.isEmpty()) {
                    Toast.makeText(this, "Vui lòng nhập đầy đủ thông tin!", Toast.LENGTH_SHORT).show();
                    return;
                }

                int seats;
                try {
                    seats = Integer.parseInt(seatsInput);
                } catch (Exception e) {
                    Toast.makeText(this, "Số chỗ phải là số nguyên hợp lệ!", Toast.LENGTH_SHORT).show();
                    return;
                }

                Loaixe newCar = new Loaixe();
                newCar.setTenLoai(nameInput);
                newCar.setSoCho(seats);
                newCar.setGiaVe(priceInput);

                ApiService apiService = ApiClient.getClient().create(ApiService.class);
                apiService.createLoaixe(newCar).enqueue(new Callback<Loaixe>() {
                    @Override
                    public void onResponse(Call<Loaixe> call, Response<Loaixe> response) {
                        if (response.isSuccessful()) {
                            dialog.dismiss();
                            Toast.makeText(CarTypeManagementActivity.this, "Thêm loại xe mới thành công!", Toast.LENGTH_SHORT).show();
                            fetchCarTypes();
                        } else {
                            Toast.makeText(CarTypeManagementActivity.this, "Lỗi server: " + response.code(), Toast.LENGTH_SHORT).show();
                        }
                    }

                    @Override
                    public void onFailure(Call<Loaixe> call, Throwable t) {
                        Toast.makeText(CarTypeManagementActivity.this, "Lỗi kết nối", Toast.LENGTH_SHORT).show();
                    }
                });
            });
        }

        dialog.show();
    }

    private void fetchCarTypes() {
        ApiService apiService = ApiClient.getClient().create(ApiService.class);
        Log.d("CarType", "Bắt đầu tải danh sách loại xe từ server...");
        
        apiService.getLoaixe().enqueue(new Callback<List<Loaixe>>() {
            @Override
            public void onResponse(Call<List<Loaixe>> call, Response<List<Loaixe>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    carTypeList.clear();
                    carTypeList.addAll(response.body());
                    adapter.notifyDataSetChanged();
                    Log.d("CarType", "Tải thành công: " + carTypeList.size() + " loại xe");
                } else {
                    Log.e("CarType", "Server phản hồi lỗi: " + response.code());
                    Toast.makeText(CarTypeManagementActivity.this, "Không thể lấy dữ liệu từ server (Mã: " + response.code() + ")", Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<List<Loaixe>> call, Throwable t) {
                Log.e("CarType", "Lỗi kết nối: " + t.getMessage());
                Toast.makeText(CarTypeManagementActivity.this, "Lỗi kết nối: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void setupBottomNav() {
        // TRANG CHỦ
        View navHome = findViewById(R.id.nav_home_op_main);
        if (navHome != null) {
            navHome.setOnClickListener(v -> {
                Intent intent = new Intent(this, OperatorMainActivity.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
                startActivity(intent);
                finish();
            });
        }

        // TÀI XẾ
        View navDriver = findViewById(R.id.nav_driver_op);
        if (navDriver != null) {
            navDriver.setOnClickListener(v -> {
                startActivity(new Intent(this, DriverSelectionActivity.class));
            });
        }

        // PHƯƠNG TIỆN
        View navVehicle = findViewById(R.id.nav_vehicle_op);
        if (navVehicle != null) {
            navVehicle.setOnClickListener(v -> {
                startActivity(new Intent(this, PhuongTienManagementActivity.class));
            });
        }

        // CHUYẾN XE
        View navTrip = findViewById(R.id.nav_trip_op);
        if (navTrip != null) {
            navTrip.setOnClickListener(v -> {
                startActivity(new Intent(this, TripListActivity.class));
            });
        }

        // TUYẾN XE
        View navRoute = findViewById(R.id.nav_route_op);
        if (navRoute != null) {
            navRoute.setOnClickListener(v -> {
                startActivity(new Intent(this, QLTuyenxeActivity.class));
            });
        }
    }
}
