package com.vexeapp;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.vexeapp.adapters.VeResultAdapter;
import com.vexeapp.models.Seat;
import com.vexeapp.models.TripSearchResult;
import com.vexeapp.api.ApiClient;
import com.vexeapp.api.ApiService;
import com.vexeapp.utils.OSMRouteLibrary;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class VeResultsActivity extends AppCompatActivity {

    private RecyclerView rvVeResults;
    private VeResultAdapter adapter;
    private TextView tvRouteTitle, tvDateTitle, tvNoResult;
    private ImageView btnBack;
    private ProgressBar progressBar;
    private List<TripSearchResult> tripList = new ArrayList<>();
    private ApiService apiService;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ve_results);

        apiService = ApiClient.getClient().create(ApiService.class);

        initViews();

        Intent intent = getIntent();
        String origin = intent.getStringExtra("ORIGIN_KEY");
        String destination = intent.getStringExtra("DESTINATION_KEY");
        String searchDate = intent.getStringExtra("DATE_KEY");
        String searchTime = intent.getStringExtra("TIME_KEY");

        tvRouteTitle.setText(origin + " - " + destination);
        tvDateTitle.setText((searchDate == null || searchDate.isEmpty()) ? "Tất cả ngày" : searchDate);

        btnBack.setOnClickListener(v -> finish());

        setupRecyclerView();
        fetchTripsFromServer(origin, destination, searchDate, searchTime);
    }

    private void initViews() {
        rvVeResults = findViewById(R.id.rvVeResults);
        tvRouteTitle = findViewById(R.id.tvRouteTitle);
        tvDateTitle = findViewById(R.id.tvDateTitle);
        tvNoResult = findViewById(R.id.tvNoResult); 
        btnBack = findViewById(R.id.btnBack);
        progressBar = findViewById(R.id.progressBar); 
    }

    private void setupRecyclerView() {
        rvVeResults.setLayoutManager(new LinearLayoutManager(this));
        adapter = new VeResultAdapter(tripList, trip -> {
            Intent nextIntent = new Intent(VeResultsActivity.this, DatVeActivity.class);
            nextIntent.putExtra("selected_trip", trip);
            startActivity(nextIntent);
        });
        rvVeResults.setAdapter(adapter);
    }

    private void fetchTripsFromServer(String origin, String destination, String date, String time) {
        if (progressBar != null) progressBar.setVisibility(View.VISIBLE);
        tvNoResult.setVisibility(View.GONE);

        apiService.getChuyenXe().enqueue(new Callback<List<TripSearchResult>>() {
            @Override
            public void onResponse(Call<List<TripSearchResult>> call, Response<List<TripSearchResult>> response) {
                if (response.isSuccessful() && response.body() != null) {
                    List<TripSearchResult> allTrips = response.body();
                    fetchSeatsAndUpdateCounts(allTrips, origin, destination, date, time);
                } else {
                    if (progressBar != null) progressBar.setVisibility(View.GONE);
                    showNoResults();
                }
            }

            @Override
            public void onFailure(Call<List<TripSearchResult>> call, Throwable t) {
                if (progressBar != null) progressBar.setVisibility(View.GONE);
                showNoResults();
            }
        });
    }

    private void fetchSeatsAndUpdateCounts(List<TripSearchResult> allTrips, String origin, String destination, String date, String time) {
        apiService.getSeatsByTrip(null).enqueue(new Callback<List<Seat>>() {
            @Override
            public void onResponse(Call<List<Seat>> call, Response<List<Seat>> response) {
                if (progressBar != null) progressBar.setVisibility(View.GONE);
                
                if (response.isSuccessful() && response.body() != null) {
                    List<Seat> allSeats = response.body();
                    for (TripSearchResult trip : allTrips) {
                        int emptyCount = 0;
                        String tripId = trip.getId();
                        for (Seat seat : allSeats) {
                            if (tripId != null && tripId.equals(seat.getChuyenXe()) 
                                    && ("Còn trống".equalsIgnoreCase(seat.getStatus()) || "Trống".equalsIgnoreCase(seat.getStatus()))) {
                                emptyCount++;
                            }
                        }
                        trip.setSeats(emptyCount);
                    }
                }
                applySmartFilter(allTrips, origin, destination, date, time);
            }

            @Override
            public void onFailure(Call<List<Seat>> call, Throwable t) {
                if (progressBar != null) progressBar.setVisibility(View.GONE);
                applySmartFilter(allTrips, origin, destination, date, time);
            }
        });
    }

    private void applySmartFilter(List<TripSearchResult> allTrips, String sOrigin, String sDest, String sDate, String sTime) {
        tripList.clear();
        
        SimpleDateFormat sdfDate = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());
        SimpleDateFormat sdfTime = new SimpleDateFormat("HH:mm", Locale.getDefault());
        
        String nowStrDate = sdfDate.format(new Date());
        String nowStrTime = sdfTime.format(new Date());
        String formattedSearchDate = convertDateFormat(sDate);

        List<TripSearchResult> tier1 = new ArrayList<>(); // Đúng tuyến + Đúng ngày + Đúng giờ
        List<TripSearchResult> tier2 = new ArrayList<>(); // Đúng tuyến + Đúng ngày (mọi giờ)
        List<TripSearchResult> tier3 = new ArrayList<>(); // Đúng tuyến + Các ngày sau
        List<TripSearchResult> tier4 = new ArrayList<>(); // Đúng tuyến (Tất cả tương lai)

        for (TripSearchResult trip : allTrips) {
            if (trip.getStatus() != null && (trip.getStatus().equalsIgnoreCase("Hoàn thành") || trip.getStatus().equalsIgnoreCase("Đã hoàn thành") || trip.getStatus().equalsIgnoreCase("Đã hủy"))) {
                continue;
            }

            String tripDate = trip.getDate() != null ? trip.getDate() : "";
            String tripTime = trip.getTime() != null ? trip.getTime() : "00:00";

            // Bỏ qua chuyến trong quá khứ
            // Giữ các chuyến cùng ngày để thuận tiện test/demo bất kỳ lúc nào trong ngày
            if (tripDate.compareTo(nowStrDate) < 0) continue;

            if (checkRouteMatch(trip, sOrigin, sDest)) {
                boolean matchDate = (sDate == null || sDate.isEmpty()) || tripDate.equals(formattedSearchDate);
                boolean matchTime = (sTime == null || sTime.isEmpty()) || isWithinThreeHours(tripTime, sTime);

                if (matchDate) {
                    if (matchTime) tier1.add(trip);
                    tier2.add(trip);
                } else if (!sDate.isEmpty() && tripDate.compareTo(formattedSearchDate) > 0) {
                    tier3.add(trip);
                }
                tier4.add(trip);
            }
        }

        // Ưu tiên hiển thị theo cấp độ
        if (!tier1.isEmpty()) {
            tripList.addAll(tier1);
        } else if (!tier2.isEmpty() && sTime != null && !sTime.isEmpty()) {
            tripList.addAll(tier2);
            Toast.makeText(this, "Không có chuyến vào khung giờ " + sTime + ". Hiển thị các chuyến khác cùng ngày.", Toast.LENGTH_LONG).show();
        } else if (!tier3.isEmpty() && sDate != null && !sDate.isEmpty()) {
            tripList.addAll(tier3);
            Collections.sort(tripList, (t1, t2) -> t1.getDate().compareTo(t2.getDate()));
            Toast.makeText(this, "Ngày " + sDate + " không có chuyến. Hiển thị các ngày tiếp theo.", Toast.LENGTH_LONG).show();
        } else if (!tier4.isEmpty()) {
            tripList.addAll(tier4);
            Collections.sort(tripList, (t1, t2) -> t1.getDate().compareTo(t2.getDate()));
            Toast.makeText(this, "Không tìm thấy chuyến phù hợp yêu cầu. Hiển thị tất cả chuyến cùng tuyến.", Toast.LENGTH_LONG).show();
        }

        adapter.notifyDataSetChanged();
        if (tripList.isEmpty()) {
            showNoResults();
        } else {
            tvNoResult.setVisibility(View.GONE);
        }
    }

    private boolean checkRouteMatch(TripSearchResult trip, String sOrigin, String sDest) {
        String routeName = trip.getTuyenXeName();
        if (routeName == null) return sOrigin.equals("Tất cả") && sDest.equals("Tất cả");

        String cleanRoute = routeName.replace("Tuyến:", "").replace("Tuyến", "").trim();
        String searchOrigin = sOrigin.trim();
        String searchDest = sDest.trim();

        String normClean = OSMRouteLibrary.normalize(cleanRoute);
        String normOrigin = OSMRouteLibrary.normalize(searchOrigin);
        String normDest = OSMRouteLibrary.normalize(searchDest);

        if (cleanRoute.contains("-")) {
            String[] parts = cleanRoute.split("-");
            if (parts.length >= 2) {
                String normTOrigin = OSMRouteLibrary.normalize(parts[0].trim());
                String normTDest = OSMRouteLibrary.normalize(parts[1].trim());

                boolean originOk = sOrigin.equals("Tất cả") || normTOrigin.contains(normOrigin) || normOrigin.contains(normTOrigin);
                boolean destOk = sDest.equals("Tất cả") || normTDest.contains(normDest) || normDest.contains(normTDest);
                return originOk && destOk;
            }
        }

        if (!sOrigin.equals("Tất cả") && !sDest.equals("Tất cả")) {
            int originIdx = normClean.indexOf(normOrigin);
            int destIdx = normClean.indexOf(normDest);
            return originIdx != -1 && destIdx != -1 && originIdx < destIdx;
        }

        boolean matchOrigin = sOrigin.equals("Tất cả") || normClean.contains(normOrigin);
        boolean matchDest = sDest.equals("Tất cả") || normClean.contains(normDest);
        return matchOrigin && matchDest;
    }

    private void showNoResults() {
        if (tvNoResult != null) {
            tvNoResult.setVisibility(View.VISIBLE);
            tvNoResult.setText("Không tìm thấy chuyến phù hợp");
        }
    }

    private boolean isWithinThreeHours(String tripTime, String searchTime) {
        try {
            String[] tParts = tripTime.split(":");
            String[] sParts = searchTime.split(":");
            int tMin = Integer.parseInt(tParts[0]) * 60 + Integer.parseInt(tParts[1]);
            int sMin = Integer.parseInt(sParts[0]) * 60 + Integer.parseInt(sParts[1]);
            return Math.abs(tMin - sMin) <= 180;
        } catch (Exception e) { return true; }
    }

    private String convertDateFormat(String date) {
        if (date == null || date.isEmpty()) return "";
        try {
            String[] parts = date.split("/");
            if (parts.length == 3) return parts[2] + "-" + parts[1] + "-" + parts[0];
        } catch (Exception e) {}
        return date;
    }
}
