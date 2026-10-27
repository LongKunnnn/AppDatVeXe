package com.vexeapp.adapters;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.os.Handler;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.vexeapp.R;
import com.vexeapp.api.ApiClient;
import com.vexeapp.api.ApiService;
import com.vexeapp.models.Loaixe;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class CarTypeAdapter extends RecyclerView.Adapter<CarTypeAdapter.CarTypeViewHolder> {

    private List<Loaixe> carList;
    private Context context;

    public CarTypeAdapter(List<Loaixe> carList, Context context) {
        this.carList = carList;
        this.context = context;
    }

    private String getDisplayName(Loaixe car) {
        if (car.getTenLoai() != null && !car.getTenLoai().isEmpty()) {
            return car.getTenLoai();
        }
        switch (car.getSoCho()) {
            case 4: return "Loại xe A";
            case 7: return "Loại xe B";
            case 9: return "Loại xe C";
            default: return "Loại xe " + car.getSoCho() + " chỗ";
        }
    }

    private int getColorBySeats(int soCho) {
        switch (soCho) {
            case 4: return Color.parseColor("#13B5F6"); // Xanh dương
            case 7: return Color.parseColor("#81C784"); // Xanh lá
            case 9: return Color.parseColor("#BA68C8"); // Tím
            case 16: return Color.parseColor("#FFA726"); // Cam
            default: return Color.parseColor("#0091D5");
        }
    }

    @NonNull
    @Override
    public CarTypeViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.item_car_type, parent, false);
        return new CarTypeViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull CarTypeViewHolder holder, int position) {
        Loaixe car = carList.get(position);
        String displayName = getDisplayName(car);
        int themeColor = getColorBySeats(car.getSoCho());

        holder.tvName.setText(displayName);
        if (displayName.length() > 0) {
            String initial = displayName.substring(displayName.length() - 1);
            holder.tvIcon.setText(initial.matches("[A-Za-z0-9]") ? initial : "X");
        }

        // Cập nhật màu sắc
        holder.viewHeader.setBackgroundColor(themeColor);
        holder.tvIcon.setBackgroundTintList(ColorStateList.valueOf(themeColor));
        holder.btnEdit.setBackgroundTintList(ColorStateList.valueOf(themeColor));

        holder.tvSeats.setText("• " + car.getSoCho() + " chỗ");

        try {
            double gia = Double.parseDouble(car.getGiaVe());
            holder.tvPrice.setText(String.format(Locale.getDefault(), "%,.0f đ", gia));
        } catch (Exception e) {
            holder.tvPrice.setText(car.getGiaVe() + " đ");
        }

        holder.tvDate.setText(car.getNgayCapNhatGia() != null ? car.getNgayCapNhatGia() : "Chưa cập nhật");
        holder.btnEdit.setOnClickListener(v -> showEditDialog(car, holder.getAdapterPosition()));
        if (holder.btnDelete != null) {
            holder.btnDelete.setOnClickListener(v -> showDeleteConfirmDialog(car, holder.getAdapterPosition()));
        }
    }

    private void showEditDialog(Loaixe car, int position) {
        Dialog dialog = new Dialog(context);
        dialog.setContentView(R.layout.dialog_crud_car_type);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        }

        TextView tvTitle = dialog.findViewById(R.id.tvCrudDialogTitle);
        EditText edtName = dialog.findViewById(R.id.edtCrudName);
        EditText edtSeats = dialog.findViewById(R.id.edtCrudSeats);
        EditText edtPrice = dialog.findViewById(R.id.edtCrudPrice);
        Button btnSave = dialog.findViewById(R.id.btnSaveCrud);
        Button btnCancel = dialog.findViewById(R.id.btnCancelCrud);
        ImageView btnCloseTop = dialog.findViewById(R.id.btnCloseCrudTop);

        if (tvTitle != null) tvTitle.setText("Chỉnh sửa loại xe");
        if (edtName != null) edtName.setText(car.getTenLoai());
        if (edtSeats != null) edtSeats.setText(String.valueOf(car.getSoCho()));
        if (edtPrice != null) edtPrice.setText(car.getGiaVe());

        if (btnCloseTop != null) btnCloseTop.setOnClickListener(v -> dialog.dismiss());
        if (btnCancel != null) btnCancel.setOnClickListener(v -> dialog.dismiss());

        if (btnSave != null) {
            btnSave.setOnClickListener(v -> {
                String nameInput = edtName.getText().toString().trim();
                String seatsInput = edtSeats.getText().toString().trim();
                String priceInput = edtPrice.getText().toString().trim();

                if (nameInput.isEmpty() || seatsInput.isEmpty() || priceInput.isEmpty()) {
                    Toast.makeText(context, "Vui lòng nhập đầy đủ thông tin!", Toast.LENGTH_SHORT).show();
                    return;
                }

                int seats;
                try {
                    seats = Integer.parseInt(seatsInput);
                } catch (Exception e) {
                    Toast.makeText(context, "Số chỗ phải là số nguyên hợp lệ!", Toast.LENGTH_SHORT).show();
                    return;
                }

                car.setTenLoai(nameInput);
                car.setSoCho(seats);
                car.setGiaVe(priceInput);
                String currentDate = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(new Date());
                car.setNgayCapNhatGia(currentDate);

                ApiService apiService = ApiClient.getClient().create(ApiService.class);
                apiService.updateLoaixe(car.getLoaixeID(), car).enqueue(new Callback<Loaixe>() {
                    @Override
                    public void onResponse(Call<Loaixe> call, Response<Loaixe> response) {
                        if (response.isSuccessful()) {
                            notifyItemChanged(position);
                            dialog.dismiss();
                            showSuccessDialog("Cập nhật loại xe thành công");
                        } else {
                            Toast.makeText(context, "Lỗi server: " + response.code(), Toast.LENGTH_SHORT).show();
                        }
                    }

                    @Override
                    public void onFailure(Call<Loaixe> call, Throwable t) {
                        Toast.makeText(context, "Lỗi kết nối", Toast.LENGTH_SHORT).show();
                    }
                });
            });
        }

        dialog.show();
    }

    private void showDeleteConfirmDialog(Loaixe car, int position) {
        new AlertDialog.Builder(context)
                .setTitle("Xác nhận xóa loại xe")
                .setMessage("Bạn có chắc chắn muốn xóa '" + getDisplayName(car) + "' không?")
                .setPositiveButton("Xóa", (dialog, which) -> {
                    ApiService apiService = ApiClient.getClient().create(ApiService.class);
                    apiService.deleteLoaixe(car.getLoaixeID()).enqueue(new Callback<Void>() {
                        @Override
                        public void onResponse(Call<Void> call, Response<Void> response) {
                            if (position >= 0 && position < carList.size()) {
                                carList.remove(position);
                                notifyItemRemoved(position);
                                notifyItemRangeChanged(position, carList.size());
                            }
                            showSuccessDialog("Đã xóa loại xe thành công");
                        }

                        @Override
                        public void onFailure(Call<Void> call, Throwable t) {
                            Toast.makeText(context, "Lỗi kết nối khi xóa!", Toast.LENGTH_SHORT).show();
                        }
                    });
                })
                .setNegativeButton("Hủy", null)
                .show();
    }

    private void showSuccessDialog(String message) {
        Dialog successDialog = new Dialog(this.context);
        successDialog.setContentView(R.layout.dialog_success);
        if (successDialog.getWindow() != null) {
            successDialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        }
        TextView tvMessage = successDialog.findViewById(R.id.tvSuccessMessage);
        if (tvMessage != null) tvMessage.setText(message);
        successDialog.show();
        new Handler().postDelayed(successDialog::dismiss, 2000);
    }

    @Override
    public int getItemCount() {
        return carList != null ? carList.size() : 0;
    }

    public static class CarTypeViewHolder extends RecyclerView.ViewHolder {
        TextView tvName, tvSeats, tvPrice, tvDate, tvIcon;
        View viewHeader;
        Button btnEdit, btnDelete;

        public CarTypeViewHolder(@NonNull View itemView) {
            super(itemView);
            tvName = itemView.findViewById(R.id.tvCarTypeName);
            tvSeats = itemView.findViewById(R.id.tvSeats);
            tvPrice = itemView.findViewById(R.id.tvPrice);
            tvDate = itemView.findViewById(R.id.tvLastUpdate);
            tvIcon = itemView.findViewById(R.id.tvIcon);
            btnEdit = itemView.findViewById(R.id.btnUpdatePrice);
            btnDelete = itemView.findViewById(R.id.btnDeleteCarType);
            viewHeader = itemView.findViewById(R.id.viewHeaderColor);
        }
    }
}
