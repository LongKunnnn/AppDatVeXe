with open("app/src/main/java/com/vexeapp/TripDetailActivity.java", "r", encoding="utf-8") as f:
    src = f.read()

# 1. Add fields
old_fields = """    private MaterialButton btnAssign;
    private RecyclerView rvPassengers;
    private Trip trip;
    private List<Passenger> passengerList = new ArrayList<>();
    private PassengerAdapter adapter;"""

new_fields = """    private MaterialButton btnAssign;
    private RecyclerView rvPassengers;
    private Trip trip;
    private List<Passenger> passengerList = new ArrayList<>();
    private PassengerAdapter adapter;
    private LinearLayout layoutPendingTickets, containerPendingTickets;"""

assert old_fields in src, "old_fields not found"
src = src.replace(old_fields, new_fields, 1)

# 2. Add view bindings in initViews
old_inits = """        btnAssign = findViewById(R.id.btnAssign);
        rvPassengers = findViewById(R.id.rvPassengers);"""

new_inits = """        btnAssign = findViewById(R.id.btnAssign);
        rvPassengers = findViewById(R.id.rvPassengers);
        layoutPendingTickets = findViewById(R.id.layoutPendingTickets);
        containerPendingTickets = findViewById(R.id.containerPendingTickets);"""

assert old_inits in src, "old_inits not found"
src = src.replace(old_inits, new_inits, 1)

# 3. Replace btnAssign click listener
old_assign_click = """        btnAssign.setOnClickListener(v -> {
            String driverId = trip.getTaiXeID();
            Log.d("TripDetail", "Driver ID check: " + driverId);
            
            if (driverId == null || driverId.isEmpty() || driverId.equalsIgnoreCase("null") || driverId.equals("0")) {
                Log.d("TripDetail", "Navigating to AssignDriverActivity");
                Intent intent = new Intent(TripDetailActivity.this, AssignDriverActivity.class);
                intent.putExtra("tripId", trip.getId());
                startActivityForResult(intent, 500);
            } else {
                Log.d("TripDetail", "Navigating to TripRouteActivity");
                Intent intent = new Intent(TripDetailActivity.this, TripRouteActivity.class);
                intent.putExtra("trip_data", trip);
                startActivity(intent);
            }
        });"""

new_assign_click = """        btnAssign.setOnClickListener(v -> {
            Intent intent = new Intent(TripDetailActivity.this, AssignDriverActivity.class);
            intent.putExtra("tripId", trip.getId());
            startActivityForResult(intent, 500);
        });"""

assert old_assign_click in src, "old_assign_click not found"
src = src.replace(old_assign_click, new_assign_click, 1)

# 4. Replace updateButtonState
old_update_btn = """    private void updateButtonState() {
        String driverId = trip.getTaiXeID();
        if (driverId != null && !driverId.isEmpty() && !driverId.equalsIgnoreCase("null") && !driverId.equals("0")) {
            btnAssign.setText("Hiển thị lộ trình chuyến");
            btnAssign.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#4CAF50")));
        } else {
            btnAssign.setText("Phân công tài xế");
            btnAssign.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#00B0FF")));
        }
    }"""

new_update_btn = """    private void updateButtonState() {
        String driverId = trip.getTaiXeID();
        if (driverId != null && !driverId.isEmpty() && !driverId.equalsIgnoreCase("null") && !driverId.equals("0")) {
            btnAssign.setText("Đổi tài xế");
            btnAssign.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#4CAF50")));
        } else {
            btnAssign.setText("Phân công tài xế");
            btnAssign.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#00B0FF")));
        }
    }"""

assert old_update_btn in src, "old_update_btn not found"
src = src.replace(old_update_btn, new_update_btn, 1)

# 5. Replace fetchPassengersFromDB
old_fetch = """    private void fetchPassengersFromDB() {
        if (trip == null) return;

        apiService.getKhachHangList().enqueue(new Callback<List<Map<String, Object>>>() {
            @Override
            public void onResponse(Call<List<Map<String, Object>>> call, Response<List<Map<String, Object>>> resK) {
                final Map<String, String> khNames = new HashMap<>();
                if (resK.isSuccessful() && resK.body() != null) {
                    for (Map<String, Object> kh : resK.body()) {
                        String id = findVal(kh, "KhachHangID", "id");
                        String name = findVal(kh, "Hovaten", "TenKhachHang", "hoTen");
                        if (!id.isEmpty()) khNames.put(id, name);
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
                                    for (Map<String, Object> v : response.body()) {
                                        String ticketTripId = findVal(v, "ChuyenXe", "chuyenxe", "ChuyenXeID");
                                        if (!ticketTripId.equalsIgnoreCase(trip.getId())) continue;

                                        String veId = findVal(v, "VeID", "id", "ve_id", "VEID");
                                        String khId = findVal(v, "KhachHang", "khachhang", "KhachHangID");
                                        String name = khNames.getOrDefault(khId, "Hành khách");
                                        String phone = findVal(v, "SoDienThoai", "phone", "sdt");
                                        String pickup = findVal(v, "DiemDon", "pickup", "diem_don");
                                        String dropoff = findVal(v, "DiemTra", "dropoff", "diem_tra");

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
                                        passengerList.add(new Passenger(name, phone, pickup, dropoff, displaySeat));
                                    }
                                    adapter.notifyDataSetChanged();
                                    if (tvAvailableSeats != null) 
                                        tvAvailableSeats.setText("Ghế trống: " + (trip.getSeats() - passengerList.size()));
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
    }"""

new_fetch = """    private void fetchPassengersFromDB() {
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
    }"""

assert old_fetch in src, "old_fetch not found"
src = src.replace(old_fetch, new_fetch, 1)

with open("app/src/main/java/com/vexeapp/TripDetailActivity.java", "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: TripDetailActivity.java updated!")

