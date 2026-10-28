package com.vexeapp;

import android.app.Dialog;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.vexeapp.adapters.PassengerAdapter;
import com.vexeapp.api.ApiClient;
import com.vexeapp.api.ApiService;
import com.vexeapp.models.Passenger;
import com.vexeapp.models.Route;
import com.vexeapp.models.Seat;
import com.vexeapp.models.Trip;
import com.google.android.material.button.MaterialButton;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class TripDetailActivity extends AppCompatActivity {

    private TextView tvRouteName, tvTime, tvTotalSeats, tvAvailableSeats, tvStatus, tvStatusOption, tvDuration;
    private MaterialButton btnAssign;
    private RecyclerView rvPassengers;
    private Trip trip;
    private List<Passenger> passengerList = new ArrayList<>();
    private PassengerAdapter adapter;
    private LinearLayout layoutPendingTickets, containerPendingTickets;
    private ImageView imgLogo, imgOpProfile;
    private ApiService apiService;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_trip_detail);
        apiService = ApiClient.getClient().create(ApiService.class);
        initViews();
        loadData();
        setupBottomNavigation();
    }

    private void initViews() {
        tvRouteName = findViewById(R.id.tvRouteName);
        tvTime = findViewById(R.id.tvTime);
        tvDuration = findViewById(R.id.tvDuration);
        tvTotalSeats = findViewById(R.id.tvTotalSeats);
        tvAvailableSeats = findViewById(R.id.tvAvailableSeats);
        tvStatus = findViewById(R.id.tvStatus);
        tvStatusOption = findViewById(R.id.tvStatusOption);
        btnAssign = findViewById(R.id.btnAssign);
        rvPassengers = findViewById(R.id.rvPassengers);
        layoutPendingTickets = findViewById(R.id.layoutPendingTickets);
        containerPendingTickets = findViewById(R.id.containerPendingTickets);
        imgLogo = findViewById(R.id.imgLogo);
        imgOpProfile = findViewById(R.id.imgOpProfile);

        rvPassengers.setLayoutManager(new LinearLayoutManager(this));
        adapter = new PassengerAdapter(passengerList);
        rvPassengers.setAdapter(adapter);

        if (imgLogo != null) imgLogo.setOnClickListener(v -> finish());

        if (imgOpProfile != null) {
            imgOpProfile.setOnClickListener(v -> {
                startActivity(new Intent(this, OperatorProfileActivity.class));
            });
        }

        if (tvStatus != null) {
            tvStatus.setOnClickListener(v -> {
                if (tvStatusOption != null) {
                    boolean isVisible = tvStatusOption.getVisibility() == View.VISIBLE;
                    tvStatusOption.setVisibility(isVisible ? View.GONE : View.VISIBLE);
                    
                    String current = tvStatus.getText().toString();
                    tvStatusOption.setText(current.equalsIgnoreCase("Hoàn thành") ? "Chưa hoàn thành" : "Hoàn thành");
                    updateStatusStyle(tvStatusOption, tvStatusOption.getText().toString());
                }
            });
        }

        if (tvStatusOption != null) {
            tvStatusOption.setOnClickListener(v -> {
                String nextStatus = tvStatusOption.getText().toString();
                showConfirmDialog(nextStatus);
            });
        }
    }

    private void showConfirmDialog(String nextStatus) {
        final Dialog dialog = new Dialog(this);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setContentView(R.layout.dialog_confirm_status);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        }

        Button btnCancel = dialog.findViewById(R.id.btnCancel);
        Button btnConfirm = dialog.findViewById(R.id.btnConfirm);

        btnCancel.setOnClickListener(v -> {
            dialog.dismiss();
            tvStatusOption.setVisibility(View.GONE);
        });

        btnConfirm.setOnClickListener(v -> {
            dialog.dismiss();
            tvStatusOption.setVisibility(View.GONE);
            updateTripStatusOnServer(nextStatus);
        });

        dialog.show();
    }

    private void updateTripStatusOnServer(String newStatus) {
        Map<String, Object> data = new HashMap<>();
        data.put("TrangThai", newStatus);

        apiService.patchTrip(trip.getId(), data).enqueue(new Callback<Void>() {
            @Override
            public void onResponse(Call<Void> call, Response<Void> response) {
                if (response.isSuccessful()) {
                    trip.setStatus(newStatus);
                    tvStatus.setText(newStatus.equalsIgnoreCase("Đã hoàn thành") ? "Hoàn thành" : newStatus);
                    updateStatusStyle(tvStatus, newStatus);
                    
                    if (newStatus.equalsIgnoreCase("Hoàn thành") || newStatus.equalsIgnoreCase("Đã hoàn thành")) {
                        updateAllTicketsToWaitingReview();
                    }
                    
                    Toast.makeText(TripDetailActivity.this, "Cập nhật thành công!", Toast.LENGTH_SHORT).show();
                    setResult(RESULT_OK);
                }
            }
            @Override public void onFailure(Call<Void> call, Throwable t) {}
        });
    }

    private void updateAllTicketsToWaitingReview() {
        apiService.getTicketsByTrip(trip.getId()).enqueue(new Callback<List<Map<String, Object>>>() {
            @Override
            public void onResponse(Call<List<Map<String, Object>>> call, Response<List<Map<String, Object>>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    for (Map<String, Object> ticket : response.body()) {
                        String veId = findVal(ticket, "VeID", "id", "VEID");
                        if (!veId.isEmpty()) {
                            Map<String, Object> patchData = new HashMap<>();
                            patchData.put("TrangThaiDanhGia", "Chờ đánh giá"); 
                            
                            apiService.patchTicket(veId, patchData).enqueue(new Callback<Void>() {
                                @Override public void onResponse(Call<Void> call, Response<Void> res) {}
                                @Override public void onFailure(Call<Void> call, Throwable t) {}
                            });
                        }
                    }
                }
            }
            @Override public void onFailure(Call<List<Map<String, Object>>> call, Throwable t) {}
        });
    }

    private void updateStatusStyle(TextView view, String status) {
        GradientDrawable gd = new GradientDrawable();
        gd.setCornerRadius(15);
        if (status != null && (status.equalsIgnoreCase("Hoàn thành") || status.equalsIgnoreCase("Đã hoàn thành"))) {
            gd.setColor(Color.parseColor("#E8F5E9"));
            view.setTextColor(Color.parseColor("#4CAF50"));
            view.setText("Hoàn thành");
        } else {
            gd.setColor(Color.parseColor("#FFF9C4"));
            view.setTextColor(Color.parseColor("#FBC02D"));
        }
        view.setBackground(gd);
    }

    private void loadData() {
        if (trip == null) {
            trip = (Trip) getIntent().getSerializableExtra("trip");
        }
        
        if (trip != null) {
            displayTripInfo();
            fetchTripDetailsFromServer(); 
            fetchPassengersFromDB();
            loadDurationFromRoute();
        }
    }

    private void loadDurationFromRoute() {
        apiService.getRoutesModel().enqueue(new Callback<List<Route>>() {
            @Override
            public void onResponse(Call<List<Route>> call, Response<List<Route>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    for (Route route : response.body()) {
                        if (route.getId().equalsIgnoreCase(trip.getTuyenXeID())) {
                            String time = route.getTime();
                            if (tvDuration != null) {
                                tvDuration.setText("Thời gian: " + (time != null ? time : "2h00"));
                            }
                            break;
                        }
                    }
                }
            }
            @Override public void onFailure(Call<List<Route>> call, Throwable t) {}
        });
    }

    private void fetchTripDetailsFromServer() {
        apiService.getTrips().enqueue(new Callback<List<Trip>>() {
            @Override
            public void onResponse(Call<List<Trip>> call, Response<List<Trip>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    for (Trip t : response.body()) {
                        if (t.getId().equalsIgnoreCase(trip.getId())) {
                            trip = t;
                            displayTripInfo();
                            break;
                        }
                    }
                }
            }
            @Override public void onFailure(Call<List<Trip>> call, Throwable t) {}
        });
    }

    private void displayTripInfo() {
        if (trip == null) return;
        tvRouteName.setText(trip.getRouteName());
        tvTime.setText("Giờ xuất phát: " + trip.getTime());
        tvTotalSeats.setText("Tổng số ghế: " + trip.getSeats());
        
        String s = trip.getStatus();
        tvStatus.setText((s != null && s.equalsIgnoreCase("Đã hoàn thành")) ? "Hoàn thành" : s);
        updateStatusStyle(tvStatus, tvStatus.getText().toString());
        
        updateButtonState();

        btnAssign.setOnClickListener(v -> {
            Intent intent = new Intent(TripDetailActivity.this, AssignDriverActivity.class);
            intent.putExtra("tripId", trip.getId());
            startActivityForResult(intent, 500);
        });
    }

    private void fetchPassengersFromDB() {
        if (trip == null) return;

        apiService.getKhachHangList().enqueue(new Callback<List<Map<String, Object>>>() {
            @Override
            public void onResponse(Call<List<Map<String, Object>>> call, Response<List<Map<String, Object>>> resK) {
                final Map<String, String> khNames = new HashMap<>();
                final Map<String, String> khPhones = new HashMap<>();
                if (resK.isSuccessful() && resK.body() != null) {
                    for (Map<String, Object> kh : resK.body()) {
                        String id = findVal(kh, "KhachHangID", "id");
                        String name = findVal(kh, "Hovaten", "TenKhachHang", "hoTen");
                        String phone = findVal(kh, "soDienThoai", "SoDienThoai", "phone");
                        if (!id.isEmpty()) {
                            khNames.put(id, name);
                            khPhones.put(id, phone);
                        }
                    }
                }

                apiService.getSeatsByTrip(trip.getId()).enqueue(new Callback<List<Seat>>() {
                    @Override
                    public void onResponse(Call<List<Seat>> call, Response<List<Seat>> resG) {
                        final List<Seat> allSeatsRaw = (resG.body() != null) ? resG.body() : new ArrayList<>();

                        apiService.getTicketsByTrip(trip.getId()).enqueue(new Callback<List<Map<String, Object>>>() {
                            @Override
                            public void onResponse(Call<List<Map<String, Object>>> call, Response<List<Map<String, Object>>> response) {
                                if (response.isSuccessful() && response.body() != null) {
                                    passengerList.clear();
                                    if (containerPendingTickets != null) {
                                        containerPendingTickets.removeAllViews();
                                    }
                                    int pendingCount = 0;

                                    for (Map<String, Object> v : response.body()) {
                                        String ticketTripId = findVal(v, "ChuyenXe", "chuyenxe", "ChuyenXeID");
                                        if (!ticketTripId.equalsIgnoreCase(trip.getId())) continue;

                                        String veId = findVal(v, "VeID", "id", "ve_id", "VEID");
                                        String khId = findVal(v, "KhachHang", "khachhang", "KhachHangID");
                                        String name = khNames.getOrDefault(khId, "Hành khách");
                                        String phone = findVal(v, "SoDienThoai", "phone", "sdt");
                                        if (phone.isEmpty()) phone = khPhones.getOrDefault(khId, "Chưa cập nhật");
                                        String pickup = findVal(v, "DiemDon", "pickup", "diem_don");
                                        String dropoff = findVal(v, "DiemTra", "dropoff", "diem_tra");
                                        String status = findVal(v, "TrangThai", "trangThai", "status");

                                        List<String> seatCodes = new ArrayList<>();
                                        for (Seat s : allSeatsRaw) {
                                            String sVeId = s.getTicketId();
                                            if (sVeId != null && sVeId.equalsIgnoreCase(veId)) {
                                                String seatCode = s.getSeatCode();
                                                if (!seatCode.isEmpty()) seatCodes.add(seatCode);
                                            }
                                        }

                                        if (seatCodes.isEmpty()) {
                                            String direct = findVal(v, "DanhSachGhe", "danh_sach_ghe", "SOGHE", "soGhe");
                                            if (!direct.isEmpty()) seatCodes.add(direct);
                                        }

                                        String displaySeat = (seatCodes.isEmpty()) ? "??" : android.text.TextUtils.join(", ", seatCodes);

                                        // XỬ LÝ VÉ CHỜ NHÀ XE XÁC NHẬN
                                        if ("Chờ xác nhận".equalsIgnoreCase(status) || "Chờ nhà xe xác nhận".equalsIgnoreCase(status)) {
                                            pendingCount++;
                                            addPendingTicketView(veId, name, phone, displaySeat);
                                        } 
                                        // CHỈ HIỂN THỊ TRÊN DANH SÁCH CHUYẾN SAU KHI ĐÃ ĐẶT/XÁC NHẬN THÀNH CÔNG
                                        else if ("Đã đặt".equalsIgnoreCase(status) || "Đã xác nhận".equalsIgnoreCase(status) || "Đã đi".equalsIgnoreCase(status) || "Hoàn thành".equalsIgnoreCase(status)) {
                                            passengerList.add(new Passenger(name, phone, pickup, dropoff, displaySeat));
                                        }
                                    }

                                    if (layoutPendingTickets != null) {
                                        layoutPendingTickets.setVisibility(pendingCount > 0 ? View.VISIBLE : View.GONE);
                                    }

                                    adapter.notifyDataSetChanged();
                                    if (tvAvailableSeats != null) 
                                        tvAvailableSeats.setText("Ghế trống: " + Math.max(0, trip.getSeats() - passengerList.size()));
                                }
                            }
                            @Override public void onFailure(Call<List<Map<String, Object>>> call, Throwable t) {}
                        });
                    }
                    @Override public void onFailure(Call<List<Seat>> call, Throwable t) {}
                });
            }
            @Override public void onFailure(Call<List<Map<String, Object>>> call, Throwable t) {}
        });
    }

    private void addPendingTicketView(final String veId, final String name, final String phone, final String seats) {
        if (containerPendingTickets == null) return;

        androidx.cardview.widget.CardView card = new androidx.cardview.widget.CardView(this);
        LinearLayout.LayoutParams cardParams = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        cardParams.setMargins(0, 0, 0, 16);
        card.setLayoutParams(cardParams);
        card.setCardElevation(4);
        card.setRadius(12);
        card.setCardBackgroundColor(Color.WHITE);

        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(24, 20, 24, 20);

        TextView tvTitle = new TextView(this);
        tvTitle.setText("Khách: " + name + " (" + phone + ")");
        tvTitle.setTextColor(Color.parseColor("#1A1A1A"));
        tvTitle.setTextSize(15);
        tvTitle.setTypeface(null, android.graphics.Typeface.BOLD);
        layout.addView(tvTitle);

        TextView tvDetails = new TextView(this);
        tvDetails.setText("Mã vé: " + veId + " | Ghế: " + seats);
        tvDetails.setTextColor(Color.parseColor("#666666"));
        tvDetails.setTextSize(13);
        tvDetails.setPadding(0, 4, 0, 12);
        layout.addView(tvDetails);

        Button btnConfirm = new Button(this);
        btnConfirm.setText("✓ Xác nhận vé");
        btnConfirm.setTextColor(Color.WHITE);
        btnConfirm.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#2E7D32")));
        btnConfirm.setOnClickListener(v -> {
            btnConfirm.setEnabled(false);
            Map<String, Object> data = new HashMap<>();
            data.put("ve_id", veId);

            apiService.xacNhanVe(data).enqueue(new Callback<Void>() {
                @Override
                public void onResponse(Call<Void> call, Response<Void> response) {
                    Toast.makeText(TripDetailActivity.this, "Đã xác nhận vé " + veId + " thành công!", Toast.LENGTH_SHORT).show();
                    fetchPassengersFromDB();
                }

                @Override
                public void onFailure(Call<Void> call, Throwable t) {
                    btnConfirm.setEnabled(true);
                    Toast.makeText(TripDetailActivity.this, "Lỗi kết nối khi xác nhận vé", Toast.LENGTH_SHORT).show();
                }
            });
        });
        layout.addView(btnConfirm);

        card.addView(layout);
        containerPendingTickets.addView(card);
    }

    private void updateButtonState() {
        String driverId = trip.getTaiXeID();
        if (driverId != null && !driverId.isEmpty() && !driverId.equalsIgnoreCase("null") && !driverId.equals("0")) {
            btnAssign.setText("Đổi tài xế");
            btnAssign.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#4CAF50")));
        } else {
            btnAssign.setText("Phân công tài xế");
            btnAssign.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#00B0FF")));
        }
    }

    private String findVal(Object obj, String... keys) {
        if (obj == null) return "";
        if (obj instanceof String) return (String) obj;
        if (obj instanceof Map) {
            Map<String, Object> map = (Map<String, Object>) obj;
            for (String k : keys) {
                Object val = map.get(k);
                if (val == null) {
                    for (String key : map.keySet()) {
                        if (key.equalsIgnoreCase(k)) {
                            val = map.get(key);
                            break;
                        }
                    }
                }
                if (val != null) {
                    if (val instanceof Map || val instanceof List) {
                        String deep = findVal(val, "id", "VeID", "ve_id", "VEID", "gheID", "soGhe", "SOGHE", "KhachHangID");
                        if (!deep.isEmpty()) return deep;
                    }
                    return val.toString();
                }
            }
        }
        if (obj instanceof List) {
            List<?> list = (List<?>) obj;
            if (!list.isEmpty()) return findVal(list.get(0), keys);
        }
        return "";
    }

    private void setupBottomNavigation() {
        findViewById(R.id.nav_home_op_main).setOnClickListener(v -> {
            startActivity(new Intent(this, OperatorMainActivity.class).setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP));
            finish();
        });
        findViewById(R.id.nav_driver_op).setOnClickListener(v -> {
            startActivity(new Intent(this, DriverSelectionActivity.class));
            finish();
        });
        findViewById(R.id.nav_vehicle_op).setOnClickListener(v -> {
            startActivity(new Intent(this, PhuongTienManagementActivity.class));
            finish();
        });
        findViewById(R.id.nav_trip_op).setOnClickListener(v -> {
            startActivity(new Intent(this, TripListActivity.class));
            finish();
        });
        findViewById(R.id.nav_route_op).setOnClickListener(v -> {
            startActivity(new Intent(this, QLTuyenxeActivity.class));
            finish();
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if ((requestCode == 500 || requestCode == 102) && resultCode == RESULT_OK) {
            loadData();
        }
    }
}
