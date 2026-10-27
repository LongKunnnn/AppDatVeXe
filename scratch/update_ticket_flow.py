# Update TicketAdapter.java
with open("app/src/main/java/com/vexeapp/adapters/TicketAdapter.java", "r", encoding="utf-8") as f:
    adapter_src = f.read()

old_interface = """    public interface OnTicketClickListener {
        void onTicketClick(Ticket ticket);
        void onCancelClick(Ticket ticket);
    }"""

new_interface = """    public interface OnTicketClickListener {
        void onTicketClick(Ticket ticket);
        void onCancelClick(Ticket ticket);
        void onPaymentClick(Ticket ticket);
    }"""

assert old_interface in adapter_src, "old_interface not found"
adapter_src = adapter_src.replace(old_interface, new_interface, 1)

old_status_logic = """        // Cấu hình nút dựa trên trạng thái (Tiếng Việt khớp với Backend)
        String status = ticket.getTrangThai();
        if ("Đã đặt".equals(status)) {
            holder.btnAction.setText("Hủy");
            holder.btnAction.setBackgroundColor(Color.parseColor("#EF2A39"));
            holder.btnAction.setEnabled(true);
            holder.btnAction.setOnClickListener(v -> {
                if (listener != null) listener.onCancelClick(ticket);
            });
        } else if ("Đã đi".equals(status)) {
            holder.btnAction.setText("Đã đi");
            holder.btnAction.setBackgroundColor(Color.parseColor("#FFC107"));
            holder.btnAction.setEnabled(false);
        } else if ("Đã hủy".equals(status)) {
            holder.btnAction.setText("Đã hủy");
            holder.btnAction.setBackgroundColor(Color.parseColor("#34B5F1"));
            holder.btnAction.setEnabled(false);
        } else {
            holder.btnAction.setText(status);
            holder.btnAction.setEnabled(false);
        }"""

new_status_logic = """        // Cấu hình nút dựa trên trạng thái thanh toán & xác nhận 2 chiều
        String status = ticket.getTrangThai();
        if ("Chờ thanh toán".equalsIgnoreCase(status)) {
            holder.btnAction.setText("Thanh toán");
            holder.btnAction.setBackgroundColor(Color.parseColor("#0047AB"));
            holder.btnAction.setEnabled(true);
            holder.btnAction.setOnClickListener(v -> {
                if (listener != null) listener.onPaymentClick(ticket);
            });
        } else if ("Chờ xác nhận".equalsIgnoreCase(status) || "Chờ nhà xe xác nhận".equalsIgnoreCase(status)) {
            holder.btnAction.setText("Chờ nhà xe xác nhận");
            holder.btnAction.setBackgroundColor(Color.parseColor("#FFA000"));
            holder.btnAction.setEnabled(false);
            holder.btnAction.setOnClickListener(null);
        } else if ("Đã đặt".equalsIgnoreCase(status) || "Đã xác nhận".equalsIgnoreCase(status)) {
            holder.btnAction.setText("Hủy vé");
            holder.btnAction.setBackgroundColor(Color.parseColor("#EF2A39"));
            holder.btnAction.setEnabled(true);
            holder.btnAction.setOnClickListener(v -> {
                if (listener != null) listener.onCancelClick(ticket);
            });
        } else if ("Đã đi".equalsIgnoreCase(status) || "Hoàn thành".equalsIgnoreCase(status)) {
            holder.btnAction.setText("Đã đi");
            holder.btnAction.setBackgroundColor(Color.parseColor("#757575"));
            holder.btnAction.setEnabled(false);
            holder.btnAction.setOnClickListener(null);
        } else if ("Đã hủy".equalsIgnoreCase(status)) {
            holder.btnAction.setText("Đã hủy");
            holder.btnAction.setBackgroundColor(Color.parseColor("#34B5F1"));
            holder.btnAction.setEnabled(false);
            holder.btnAction.setOnClickListener(null);
        } else {
            holder.btnAction.setText(status != null ? status : "Chi tiết");
            holder.btnAction.setBackgroundColor(Color.parseColor("#888888"));
            holder.btnAction.setEnabled(false);
            holder.btnAction.setOnClickListener(null);
        }"""

assert old_status_logic in adapter_src, "old_status_logic not found"
adapter_src = adapter_src.replace(old_status_logic, new_status_logic, 1)

with open("app/src/main/java/com/vexeapp/adapters/TicketAdapter.java", "w", encoding="utf-8") as f:
    f.write(adapter_src)

print("SUCCESS: TicketAdapter.java updated!")

# Update QLVeXeActivity.java
with open("app/src/main/java/com/vexeapp/QLVeXeActivity.java", "r", encoding="utf-8") as f:
    activity_src = f.read()

# Replace ticket filter in loadTickets
old_filter = """                        for (Ticket ticket : response.body()) {
                            if (currentStatus.equalsIgnoreCase(ticket.getTrangThai()) &&
                                    customerId.equals(ticket.getKhachHangID())) {
                                ticketList.add(ticket);
                            }
                        }"""

new_filter = """                        for (Ticket ticket : response.body()) {
                            String st = ticket.getTrangThai();
                            boolean matches = false;
                            if ("Đã đặt".equalsIgnoreCase(currentStatus)) {
                                matches = "Đã đặt".equalsIgnoreCase(st) || "Đã xác nhận".equalsIgnoreCase(st) ||
                                          "Chờ thanh toán".equalsIgnoreCase(st) || "Chờ xác nhận".equalsIgnoreCase(st);
                            } else {
                                matches = currentStatus.equalsIgnoreCase(st);
                            }
                            if (matches && (customerId == null || customerId.isEmpty() || customerId.equals(ticket.getKhachHangID()))) {
                                ticketList.add(ticket);
                            }
                        }"""

assert old_filter in activity_src, "old_filter not found"
activity_src = activity_src.replace(old_filter, new_filter, 1)

# Add onPaymentClick and showPaymentQrDialog to QLVeXeActivity
old_dialog_logic = """        if ("Đã đặt".equalsIgnoreCase(status)) {
            if ("Đã thanh toán".equalsIgnoreCase(paymentStatus)) {
                btnPayment.setText("Đã thanh toán");
                btnPayment
                        .setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#F1C40F")));
            } else {
                btnPayment.setText("Thanh toán");
                btnPayment
                        .setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#34B5F1")));
                btnPayment.setEnabled(true);
                btnPayment.setOnClickListener(v -> {
                    dialog.dismiss();
                    showUpcomingDialog();
                });
            }
        } else if ("Đã đi".equalsIgnoreCase(status)) {"""

new_dialog_logic = """        if ("Chờ thanh toán".equalsIgnoreCase(status)) {
            btnPayment.setText("Thanh toán ngay");
            btnPayment.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#0047AB")));
            btnPayment.setEnabled(true);
            btnPayment.setOnClickListener(v -> {
                dialog.dismiss();
                showPaymentQrDialog(ticket);
            });
        } else if ("Chờ xác nhận".equalsIgnoreCase(status)) {
            btnPayment.setText("Chờ nhà xe xác nhận");
            btnPayment.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#FFA000")));
            btnPayment.setEnabled(false);
        } else if ("Đã đặt".equalsIgnoreCase(status) || "Đã xác nhận".equalsIgnoreCase(status)) {
            btnPayment.setText("Đã xác nhận (Đã thanh toán)");
            btnPayment.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.parseColor("#4CAF50")));
            btnPayment.setEnabled(false);
        } else if ("Đã đi".equalsIgnoreCase(status)) {"""

assert old_dialog_logic in activity_src, "old_dialog_logic not found"
activity_src = activity_src.replace(old_dialog_logic, new_dialog_logic, 1)

# Add showPaymentQrDialog implementation
old_cancel_click = """    @Override
    public void onCancelClick(Ticket ticket) {"""

new_payment_and_cancel = """    @Override
    public void onPaymentClick(Ticket ticket) {
        showPaymentQrDialog(ticket);
    }

    private void showPaymentQrDialog(Ticket ticket) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        View dialogView = LayoutInflater.from(this).inflate(R.layout.dialog_qr_payment, null);
        builder.setView(dialogView);
        AlertDialog dialog = builder.create();
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new ColorDrawable(Color.TRANSPARENT));
        }

        TextView tvQrTicketCode = dialogView.findViewById(R.id.tvQrTicketCode);
        TextView tvQrRoute = dialogView.findViewById(R.id.tvQrRoute);
        TextView tvQrDate = dialogView.findViewById(R.id.tvQrDate);
        TextView tvQrTime = dialogView.findViewById(R.id.tvQrTime);
        TextView tvQrSeats = dialogView.findViewById(R.id.tvQrSeats);
        TextView tvQrTotal = dialogView.findViewById(R.id.tvQrTotal);
        ImageView btnQrClose = dialogView.findViewById(R.id.btnQrClose);
        Button btnConfirmPaid = dialogView.findViewById(R.id.btnConfirmPaid);
        Button btnQrCancel = dialogView.findViewById(R.id.btnQrCancel);

        if (tvQrTicketCode != null) tvQrTicketCode.setText(ticket.getVeID());
        if (tvQrRoute != null) tvQrRoute.setText(ticket.getTenTuyen() != null ? ticket.getTenTuyen() : "Hà Nội - Ninh Bình");
        if (tvQrDate != null) tvQrDate.setText(ticket.getNgayKhoiHanh() != null ? ticket.getNgayKhoiHanh() : "");
        if (tvQrTime != null) tvQrTime.setText(ticket.getGioDi() != null ? ticket.getGioDi() : "");
        if (tvQrSeats != null) tvQrSeats.setText(ticket.getFormattedSeats());
        DecimalFormat formatter = new DecimalFormat("#,###");
        if (tvQrTotal != null) tvQrTotal.setText(formatter.format(ticket.getTongTien()) + " đ");

        if (btnQrClose != null) btnQrClose.setOnClickListener(v -> dialog.dismiss());
        if (btnQrCancel != null) btnQrCancel.setOnClickListener(v -> dialog.dismiss());

        if (btnConfirmPaid != null) {
            btnConfirmPaid.setOnClickListener(v -> {
                btnConfirmPaid.setEnabled(false);
                Map<String, Object> data = new HashMap<>();
                data.put("ve_id", ticket.getVeID());

                apiService.thanhToanVe(data).enqueue(new Callback<Void>() {
                    @Override
                    public void onResponse(Call<Void> call, Response<Void> response) {
                        dialog.dismiss();
                        Toast.makeText(QLVeXeActivity.this, "Đã gửi thanh toán! Vui lòng chờ nhà xe xác nhận.", Toast.LENGTH_LONG).show();
                        loadTickets();
                    }

                    @Override
                    public void onFailure(Call<Void> call, Throwable t) {
                        btnConfirmPaid.setEnabled(true);
                        Toast.makeText(QLVeXeActivity.this, "Lỗi kết nối khi thanh toán!", Toast.LENGTH_SHORT).show();
                    }
                });
            });
        }

        dialog.show();
    }

    @Override
    public void onCancelClick(Ticket ticket) {"""

assert old_cancel_click in activity_src, "old_cancel_click not found"
activity_src = activity_src.replace(old_cancel_click, new_payment_and_cancel, 1)

with open("app/src/main/java/com/vexeapp/QLVeXeActivity.java", "w", encoding="utf-8") as f:
    f.write(activity_src)

print("SUCCESS: QLVeXeActivity.java updated!")

