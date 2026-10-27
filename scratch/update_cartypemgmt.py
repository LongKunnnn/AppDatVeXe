with open("app/src/main/java/com/vexeapp/CarTypeManagementActivity.java", "r", encoding="utf-8") as f:
    src = f.read()

old_fields = """    private RecyclerView rvCarTypes;
    private CarTypeAdapter adapter;
    private List<Loaixe> carTypeList;
    private ImageView btnBack, btnProfile;"""

new_fields = """    private RecyclerView rvCarTypes;
    private CarTypeAdapter adapter;
    private List<Loaixe> carTypeList;
    private ImageView btnBack, btnProfile;
    private android.widget.Button btnAddCarType;"""

assert old_fields in src, "old_fields not found"
src = src.replace(old_fields, new_fields, 1)

old_init = """        btnProfile = findViewById(R.id.btnProfile);
        if (btnProfile == null) btnProfile = findViewById(R.id.imgOpProfile);"""

new_init = """        btnProfile = findViewById(R.id.btnProfile);
        if (btnProfile == null) btnProfile = findViewById(R.id.imgOpProfile);
        btnAddCarType = findViewById(R.id.btnAddCarType);"""

assert old_init in src, "old_init not found"
src = src.replace(old_init, new_init, 1)

old_events = """        if (btnProfile != null) {
            btnProfile.setOnClickListener(v -> {
                startActivity(new Intent(this, OperatorProfileActivity.class));
            });
        }"""

new_events = """        if (btnProfile != null) {
            btnProfile.setOnClickListener(v -> {
                startActivity(new Intent(this, OperatorProfileActivity.class));
            });
        }
        if (btnAddCarType != null) {
            btnAddCarType.setOnClickListener(v -> showAddCarTypeDialog());
        }"""

assert old_events in src, "old_events not found"
src = src.replace(old_events, new_events, 1)

# Add showAddCarTypeDialog method
old_fetch = """    private void fetchCarTypes() {"""

new_add_method = """    private void showAddCarTypeDialog() {
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

    private void fetchCarTypes() {"""

assert old_fetch in src, "old_fetch not found"
src = src.replace(old_fetch, new_add_method, 1)

with open("app/src/main/java/com/vexeapp/CarTypeManagementActivity.java", "w", encoding="utf-8") as f:
    f.write(src)

print("SUCCESS: CarTypeManagementActivity.java updated!")

