package com.vexeapp;

import android.app.DatePickerDialog;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.Typeface;
import android.os.Bundle;
import android.os.Handler;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.vexeapp.api.ApiClient;
import com.vexeapp.api.ApiService;
import com.vexeapp.models.ChiTietTaiXeModel;
import com.vexeapp.models.Trip;
import com.vexeapp.models.VehicleManaged;
import com.google.android.material.tabs.TabLayout;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.HashMap;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class DriverScheduleMonitoringActivity extends AppCompatActivity {

    private TextView tvCurrentMonth, tvWeekRange, tvFromDate, tvToDate, tvEmptyMessage;
    private View layoutFilter;
    private LinearLayout layoutScheduleGrid;
    private Spinner spinnerDriver, spinnerStatus;
    private Calendar currentWeekCalendar;
    private ApiService apiService;
    private List<Trip> allTrips = new ArrayList<>();
    private List<ChiTietTaiXeModel> drivers = new ArrayList<>();

    private final SimpleDateFormat monthYearFormat = new SimpleDateFormat("'tháng' M 'năm' yyyy", new Locale("vi", "VN"));
    private final SimpleDateFormat rangeFormat = new SimpleDateFormat("dd-MM", Locale.getDefault());
    private final SimpleDateFormat apiDateFormat = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());
    private final SimpleDateFormat dayFormat = new SimpleDateFormat("dd", Locale.getDefault());

    private final Handler autoRefreshHandler = new Handler();
    private final Runnable autoRefreshRunnable = new Runnable() {
        @Override
        public void run() {
            loadData();
            autoRefreshHandler.postDelayed(this, 60000); // 60 seconds
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_driver_schedule_monitoring);

        apiService = ApiClient.getClient().create(ApiService.class);
        currentWeekCalendar = Calendar.getInstance();
        currentWeekCalendar.setFirstDayOfWeek(Calendar.MONDAY);
        currentWeekCalendar.set(Calendar.DAY_OF_WEEK, Calendar.MONDAY);

        initViews();
        setupListeners();
        updateWeekDisplay();
        loadData();

        autoRefreshHandler.postDelayed(autoRefreshRunnable, 60000);
    }

    private void initViews() {
        tvCurrentMonth = findViewById(R.id.tvCurrentMonth);
        tvWeekRange = findViewById(R.id.tvWeekRange);
        tvFromDate = findViewById(R.id.tvFromDate);
        tvToDate = findViewById(R.id.tvToDate);
        tvEmptyMessage = findViewById(R.id.tvEmptyMessage);
        layoutFilter = findViewById(R.id.layoutFilter);
        layoutScheduleGrid = findViewById(R.id.layoutScheduleGrid);
        spinnerDriver = findViewById(R.id.spinnerDriver);
        spinnerStatus = findViewById(R.id.spinnerStatus);

        findViewById(R.id.btnBack).setOnClickListener(v -> finish());

        String[] statuses = {"Tất cả", "Hoàn thành", "Chưa hoàn thành"};
        ArrayAdapter<String> statusAdapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, statuses);
        spinnerStatus.setAdapter(statusAdapter);
    }

    private void setupListeners() {
        findViewById(R.id.btnPrevWeek).setOnClickListener(v -> {
            currentWeekCalendar.add(Calendar.WEEK_OF_YEAR, -1);
            updateWeekDisplay();
            renderSchedule();
        });

        findViewById(R.id.btnNextWeek).setOnClickListener(v -> {
            currentWeekCalendar.add(Calendar.WEEK_OF_YEAR, 1);
            updateWeekDisplay();
            renderSchedule();
        });

        findViewById(R.id.btnToday).setOnClickListener(v -> {
            Calendar c = Calendar.getInstance();
            new DatePickerDialog(this, (view, year, month, day) -> {
                currentWeekCalendar.set(year, month, day);
                currentWeekCalendar.setFirstDayOfWeek(Calendar.MONDAY);
                currentWeekCalendar.set(Calendar.DAY_OF_WEEK, Calendar.MONDAY);
                updateWeekDisplay();
                renderSchedule();
            }, c.get(Calendar.YEAR), c.get(Calendar.MONTH), c.get(Calendar.DAY_OF_MONTH)).show();
        });

        findViewById(R.id.btnFilter).setOnClickListener(v -> {
            layoutFilter.setVisibility(layoutFilter.getVisibility() == View.GONE ? View.VISIBLE : View.GONE);
        });

        findViewById(R.id.btnSearch).setOnClickListener(v -> loadData());

        tvFromDate.setOnClickListener(v -> showDatePicker(tvFromDate));
        tvToDate.setOnClickListener(v -> showDatePicker(tvToDate));
    }

    private void updateWeekDisplay() {
        tvCurrentMonth.setText(monthYearFormat.format(currentWeekCalendar.getTime()));
        Calendar end = (Calendar) currentWeekCalendar.clone();
        end.add(Calendar.DAY_OF_WEEK, 6);
        String range = rangeFormat.format(currentWeekCalendar.getTime()) + " - " + rangeFormat.format(end.getTime());
        tvWeekRange.setText(range);
    }

    private void loadData() {
        apiService.getChiTietTaiXeList("Get").enqueue(new Callback<List<ChiTietTaiXeModel>>() {
            @Override
            public void onResponse(Call<List<ChiTietTaiXeModel>> call, Response<List<ChiTietTaiXeModel>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    drivers = response.body();
                    setupDriverSpinner();
                }
            }
            @Override public void onFailure(Call<List<ChiTietTaiXeModel>> call, Throwable t) {}
        });

        apiService.getTrips().enqueue(new Callback<List<Trip>>() {
            @Override
            public void onResponse(Call<List<Trip>> call, Response<List<Trip>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    allTrips = response.body();
                    renderSchedule();
                }
            }
            @Override public void onFailure(Call<List<Trip>> call, Throwable t) {}
        });
    }

    private void setupDriverSpinner() {
        String currentSelection = spinnerDriver.getSelectedItem() != null ? 
                spinnerDriver.getSelectedItem().toString() : "Tất cả tài xế";
        List<String> names = new ArrayList<>();
        names.add("Tất cả tài xế");
        for (ChiTietTaiXeModel d : drivers) {
            if (d.getHoTen() != null) names.add(d.getHoTen());
        }
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, names);
        spinnerDriver.setAdapter(adapter);
        int pos = names.indexOf(currentSelection);
        if (pos >= 0) spinnerDriver.setSelection(pos);
    }

    private void renderSchedule() {
        if (layoutScheduleGrid == null) return;
        layoutScheduleGrid.removeAllViews();
        int totalTripsFound = 0;

        String selectedDriverName = spinnerDriver.getSelectedItem() != null ? spinnerDriver.getSelectedItem().toString() : "Tất cả tài xế";
        String selectedStatus = spinnerStatus.getSelectedItem() != null ? spinnerStatus.getSelectedItem().toString() : "Tất cả";
        String fromDateStr = tvFromDate.getText().toString();
        String toDateStr = tvToDate.getText().toString();

        String selectedDriverId = null;
        if (!"Tất cả tài xế".equals(selectedDriverName)) {
            for (ChiTietTaiXeModel d : drivers) {
                if (selectedDriverName.equalsIgnoreCase(d.getHoTen())) {
                    selectedDriverId = d.getTaixe();
                    break;
                }
            }
        }

        Calendar cal = (Calendar) currentWeekCalendar.clone();
        String[] dayLabels = {"Th 2", "Th 3", "Th 4", "Th 5", "Th 6", "Th 7", "CN"};

        for (int i = 0; i < 7; i++) {
            View column = LayoutInflater.from(this).inflate(R.layout.item_schedule_column, layoutScheduleGrid, false);
            TextView tvDayLabel = column.findViewById(R.id.tvDayLabel);
            TextView tvDayNum = column.findViewById(R.id.tvDayNum);
            LinearLayout layoutItems = column.findViewById(R.id.layoutDayItems);

            tvDayLabel.setText(dayLabels[i]);
            tvDayNum.setText(dayFormat.format(cal.getTime()));

            String dateStr = apiDateFormat.format(cal.getTime());
            boolean hasTrip = false;

            for (Trip trip : allTrips) {
                if (trip.getTaiXeID() == null || trip.getTaiXeID().isEmpty()) continue;
                if (selectedDriverId != null && !selectedDriverId.equalsIgnoreCase(trip.getTaiXeID())) continue;
                if (!"Tất cả".equals(selectedStatus)) {
                    boolean isHoanThanh = "Hoàn thành".equalsIgnoreCase(trip.getStatus());
                    if ("Hoàn thành".equals(selectedStatus) && !isHoanThanh) continue;
                    if ("Chưa hoàn thành".equals(selectedStatus) && isHoanThanh) continue;
                }
                if (!fromDateStr.equals("mm/dd/yyyy") && dateStr.compareTo(fromDateStr) < 0) continue;
                if (!toDateStr.equals("mm/dd/yyyy") && dateStr.compareTo(toDateStr) > 0) continue;

                if (trip.getDate().startsWith(dateStr)) {
                    hasTrip = true;
                    totalTripsFound++;
                    addTripToView(layoutItems, trip);
                }
            }
            if (!hasTrip) {
                TextView tvEmpty = new TextView(this);
                tvEmpty.setText("Không\ncó lịch");
                tvEmpty.setTextSize(10);
                tvEmpty.setTextColor(Color.LTGRAY);
                tvEmpty.setGravity(Gravity.CENTER);
                layoutItems.addView(tvEmpty);
            }
            layoutScheduleGrid.addView(column);
            cal.add(Calendar.DAY_OF_YEAR, 1);
        }
        if (tvEmptyMessage != null) {
            tvEmptyMessage.setVisibility(totalTripsFound == 0 ? View.VISIBLE : View.GONE);
        }
    }

    private void addTripToView(LinearLayout parent, Trip trip) {
        View view = LayoutInflater.from(this).inflate(R.layout.item_schedule_trip_box, parent, false);
        TextView tvLoc = view.findViewById(R.id.tvLocation);
        TextView tvTime = view.findViewById(R.id.tvTime);
        tvLoc.setText(trip.getRouteName().replace("Tuyến: ", ""));
        tvTime.setText(trip.getTime());
        if ("Hoàn thành".equalsIgnoreCase(trip.getStatus())) {
            view.setBackgroundColor(Color.parseColor("#4CAF50"));
        } else {
            view.setBackgroundColor(Color.parseColor("#FFEB3B"));
        }
        view.setOnClickListener(v -> showTripDetailEnhanced(trip));
        parent.addView(view);
    }

    private void showTripDetailEnhanced(Trip trip) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        View view = LayoutInflater.from(this).inflate(R.layout.dialog_trip_monitoring_detail, null);

        TextView tvTitle = view.findViewById(R.id.tvDetailTitle);
        TextView tvRoute = view.findViewById(R.id.tvDetailRoute);
        TextView tvDateTime = view.findViewById(R.id.tvDetailDateTime);
        TextView tvDriver = view.findViewById(R.id.tvDetailDriver);
        TextView tvTripStatus = view.findViewById(R.id.tvDetailTripStatus);

        TabLayout tabLayout = view.findViewById(R.id.tabLayoutDetail);
        LinearLayout layoutTabVehicle = view.findViewById(R.id.layoutTabVehicle);
        LinearLayout layoutTabRoute = view.findViewById(R.id.layoutTabRoute);

        TextView tvTripId = view.findViewById(R.id.tvTripId);
        TextView tvPlate = view.findViewById(R.id.tvVehiclePlate);
        TextView tvSeats = view.findViewById(R.id.tvVehicleSeats);
        TextView tvType = view.findViewById(R.id.tvVehicleType);
        TextView tvPrice = view.findViewById(R.id.tvTripPrice);
        TextView tvVehicleStatus = view.findViewById(R.id.tvVehicleStatus);

        TextView tvRouteStartEnd = view.findViewById(R.id.tvRouteStartEnd);
        TextView tvRouteEstimatedTime = view.findViewById(R.id.tvRouteEstimatedTime);
        RecyclerView rvRoutePoints = view.findViewById(R.id.rvRoutePoints);
        TextView tvNoTickets = view.findViewById(R.id.tvNoTickets);
        View btnOpenFull = view.findViewById(R.id.btnOpenFullTripDetail);

        tvTitle.setText("Chi tiết chuyến xe");
        tvRoute.setText(trip.getRouteName());

        String timeStr = trip.getTime();
        String endTimeStr = trip.getEndTime();
        if (endTimeStr != null && !endTimeStr.isEmpty() && !endTimeStr.equals(timeStr)) {
            timeStr += " - " + endTimeStr;
        }
        tvDateTime.setText("Khởi hành: " + timeStr + " (" + trip.getDate() + ")");

        // Driver name
        String driverName = trip.getTenTaiXe();
        if (driverName == null || driverName.isEmpty()) {
            if (trip.getTaiXeID() != null && !trip.getTaiXeID().isEmpty()) {
                for (ChiTietTaiXeModel d : drivers) {
                    if (trip.getTaiXeID().equalsIgnoreCase(d.getTaixe())) {
                        driverName = d.getHoTen();
                        break;
                    }
                }
            }
        }
        if (driverName == null || driverName.isEmpty()) {
            driverName = (trip.getTaiXeID() != null && !trip.getTaiXeID().isEmpty()) ? trip.getTaiXeID() : "Chưa phân công";
        }
        tvDriver.setText("Tài xế: " + driverName);

        // Status pill
        boolean isDone = "Hoàn thành".equalsIgnoreCase(trip.getStatus()) || "Đã hoàn thành".equalsIgnoreCase(trip.getStatus());
        tvTripStatus.setText(isDone ? "Hoàn thành" : "Chưa hoàn thành");
        tvTripStatus.setTextColor(Color.parseColor(isDone ? "#2E7D32" : "#F57F17"));
        tvTripStatus.setBackgroundColor(Color.parseColor(isDone ? "#E8F5E9" : "#FFF9C4"));

        // Vehicle info tab
        tvTripId.setText(trip.getId());
        tvPlate.setText((trip.getBienSo() != null && !trip.getBienSo().isEmpty()) ? trip.getBienSo() : trip.getXeID());
        tvType.setText(trip.getVehicleType());
        tvSeats.setText(trip.getSeats() + " chỗ ngồi");

        String priceStr = trip.getPrice();
        try {
            long p = Long.parseLong(priceStr.replaceAll("[^0-9]", ""));
            priceStr = String.format(Locale.getDefault(), "%,d đ", p);
        } catch (Exception ignored) {}
        tvPrice.setText(priceStr);
        tvVehicleStatus.setText("Đang hoạt động");

        // Route info tab
        String startPoint = trip.getDiemDi();
        String endPoint = trip.getDiemDen();
        if (startPoint == null || startPoint.isEmpty()) {
            tvRouteStartEnd.setText("Lộ trình: " + trip.getRouteName().replace("Tuyến: ", ""));
        } else {
            tvRouteStartEnd.setText("Lộ trình: " + startPoint + " ➔ " + endPoint);
        }
        tvRouteEstimatedTime.setText("Thời gian dự kiến: " + trip.getDuration());

        // Default: Tab 0 (Thông tin xe)
        layoutTabVehicle.setVisibility(View.VISIBLE);
        layoutTabRoute.setVisibility(View.GONE);
        if (tabLayout.getTabAt(0) != null) {
            tabLayout.getTabAt(0).select();
        }

        // Fetch vehicle details from API
        apiService.getVehicles().enqueue(new Callback<List<VehicleManaged>>() {
            @Override
            public void onResponse(Call<List<VehicleManaged>> call, Response<List<VehicleManaged>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    for (VehicleManaged v : response.body()) {
                        if (v.getXeID() != null && v.getXeID().equalsIgnoreCase(trip.getXeID())) {
                            if (v.getBienSoXe() != null && !v.getBienSoXe().equals("N/A")) {
                                tvPlate.setText(v.getBienSoXe());
                            }
                            if (v.getSoGhe() != null) {
                                tvSeats.setText(v.getSoGhe() + " chỗ ngồi");
                            }
                            tvVehicleStatus.setText(v.getTrangThai());
                            if (v.getLoaiXeIDStr() != null && !v.getLoaiXeIDStr().equals("N/A")) {
                                tvType.setText(v.getLoaiXeIDStr());
                            }
                            break;
                        }
                    }
                }
            }
            @Override public void onFailure(Call<List<VehicleManaged>> call, Throwable t) {}
        });

        // Setup route points
        rvRoutePoints.setLayoutManager(new LinearLayoutManager(this));
        apiService.getTicketsByTrip(trip.getId()).enqueue(new Callback<List<Map<String, Object>>>() {
            @Override
            public void onResponse(Call<List<Map<String, Object>>> call, Response<List<Map<String, Object>>> response) {
                if (response.isSuccessful() && response.body() != null && !response.body().isEmpty()) {
                    List<Map<String, String>> allPoints = new ArrayList<>();
                    for (Map<String, Object> ticket : response.body()) {
                        String don = (String) ticket.get("DiemDon");
                        if (don == null) don = (String) ticket.get("diemDon");
                        String tra = (String) ticket.get("DiemTra");
                        if (tra == null) tra = (String) ticket.get("diemTra");

                        if (don != null && !don.isEmpty()) {
                            Map<String, String> m = new HashMap<>();
                            m.put("name", don);
                            m.put("type", "Điểm đón (Khách đặt)");
                            allPoints.add(m);
                        }
                        if (tra != null && !tra.isEmpty()) {
                            Map<String, String> m = new HashMap<>();
                            m.put("name", tra);
                            m.put("type", "Điểm trả (Khách đặt)");
                            allPoints.add(m);
                        }
                    }
                    if (!allPoints.isEmpty()) {
                        tvNoTickets.setVisibility(View.GONE);
                        rvRoutePoints.setVisibility(View.VISIBLE);
                        rvRoutePoints.setAdapter(new RoutePointAdapter(allPoints));
                    } else {
                        tvNoTickets.setVisibility(View.VISIBLE);
                        rvRoutePoints.setVisibility(View.GONE);
                    }
                } else {
                    tvNoTickets.setVisibility(View.VISIBLE);
                    rvRoutePoints.setVisibility(View.GONE);
                }
            }
            @Override public void onFailure(Call<List<Map<String, Object>>> call, Throwable t) {
                tvNoTickets.setVisibility(View.VISIBLE);
                rvRoutePoints.setVisibility(View.GONE);
            }
        });

        tabLayout.addOnTabSelectedListener(new TabLayout.OnTabSelectedListener() {
            @Override
            public void onTabSelected(TabLayout.Tab tab) {
                View tabView = ((ViewGroup) tabLayout.getChildAt(0)).getChildAt(tab.getPosition());
                tabView.animate().scaleX(1.05f).scaleY(1.05f).setDuration(150).start();
                if (tab.getPosition() == 1) { // Lộ trình
                    layoutTabRoute.setVisibility(View.VISIBLE);
                    layoutTabVehicle.setVisibility(View.GONE);
                } else { // Thông tin xe
                    layoutTabRoute.setVisibility(View.GONE);
                    layoutTabVehicle.setVisibility(View.VISIBLE);
                }
            }
            @Override
            public void onTabUnselected(TabLayout.Tab tab) {
                View tabView = ((ViewGroup) tabLayout.getChildAt(0)).getChildAt(tab.getPosition());
                tabView.animate().scaleX(1.0f).scaleY(1.0f).setDuration(150).start();
            }
            @Override public void onTabReselected(TabLayout.Tab tab) {}
        });

        AlertDialog dialog = builder.setView(view).create();
        if (dialog.getWindow() != null) dialog.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        view.findViewById(R.id.btnCloseDialog).setOnClickListener(v -> dialog.dismiss());

        if (btnOpenFull != null) {
            btnOpenFull.setOnClickListener(v -> {
                dialog.dismiss();
                Intent intent = new Intent(DriverScheduleMonitoringActivity.this, TripDetailActivity.class);
                intent.putExtra("trip", trip);
                startActivity(intent);
            });
        }

        dialog.show();
    }

    private static class RoutePointAdapter extends RecyclerView.Adapter<RoutePointAdapter.VH> {
        private final List<Map<String, String>> list;
        public RoutePointAdapter(List<Map<String, String>> list) { this.list = list; }
        @NonNull @Override public VH onCreateViewHolder(@NonNull ViewGroup p, int t) {
            return new VH(LayoutInflater.from(p.getContext()).inflate(R.layout.item_route_point, p, false));
        }
        @Override public void onBindViewHolder(@NonNull VH h, int p) {
            h.t1.setText(list.get(p).get("name"));
            h.t2.setText(list.get(p).get("type"));
        }
        @Override public int getItemCount() { return list.size(); }
        static class VH extends RecyclerView.ViewHolder {
            TextView t1, t2;
            VH(View v) { super(v); t1 = v.findViewById(R.id.tvPointName); t2 = v.findViewById(R.id.tvPointType); }
        }
    }

    private void showDatePicker(TextView target) {
        Calendar c = Calendar.getInstance();
        new DatePickerDialog(this, (view, year, month, day) -> {
            String date = String.format(Locale.getDefault(), "%04d-%02d-%02d", year, month + 1, day);
            target.setText(date);
        }, c.get(Calendar.YEAR), c.get(Calendar.MONTH), c.get(Calendar.DAY_OF_MONTH)).show();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        autoRefreshHandler.removeCallbacks(autoRefreshRunnable);
    }
}
