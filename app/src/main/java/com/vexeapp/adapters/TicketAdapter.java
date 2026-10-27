package com.vexeapp.adapters;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.vexeapp.R;
import com.vexeapp.models.Ticket;

import java.util.List;

public class TicketAdapter extends RecyclerView.Adapter<TicketAdapter.TicketViewHolder> {

    private List<Ticket> ticketList;
    private Context context;
    private OnTicketClickListener listener;

    public interface OnTicketClickListener {
        void onTicketClick(Ticket ticket);
        void onCancelClick(Ticket ticket);
        void onPaymentClick(Ticket ticket);
    }

    public TicketAdapter(Context context, List<Ticket> ticketList, OnTicketClickListener listener) {
        this.context = context;
        this.ticketList = ticketList;
        this.listener = listener;
    }

    @NonNull
    @Override
    public TicketViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.item_ticket, parent, false);
        return new TicketViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull TicketViewHolder holder, int position) {
        Ticket ticket = ticketList.get(position);
        
        // Định dạng lại thời gian: chỉ lấy hh:mm (bỏ giây)
        String rawTime = ticket.getGioDi();
        if (rawTime != null && rawTime.contains(":") && rawTime.split(":").length >= 2) {
            String[] parts = rawTime.split(":");
            holder.tvTime.setText(parts[0] + ":" + parts[1]);
        } else {
            holder.tvTime.setText(rawTime);
        }

        holder.tvDate.setText(ticket.getNgayKhoiHanh());
        holder.tvRoute.setText(ticket.getTenTuyen());
        holder.tvCar.setText(ticket.getTenNhaXe());
        holder.tvSeatCount.setText("Số lượng ghế: " + String.format("%02d", ticket.getSoLuongGhe()));
        holder.tvSeats.setText("Mã số ghế: " + ticket.getFormattedSeats());

        // Cấu hình nút dựa trên trạng thái thanh toán & xác nhận 2 chiều
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
        }

        holder.itemView.setOnClickListener(v -> listener.onTicketClick(ticket));
    }

    @Override
    public int getItemCount() {
        return ticketList != null ? ticketList.size() : 0;
    }

    public static class TicketViewHolder extends RecyclerView.ViewHolder {
        TextView tvTime, tvDate, tvRoute, tvCar, tvSeatCount, tvSeats;
        Button btnAction;

        public TicketViewHolder(@NonNull View itemView) {
            super(itemView);
            tvTime = itemView.findViewById(R.id.tvTime);
            tvDate = itemView.findViewById(R.id.tvDate);
            tvRoute = itemView.findViewById(R.id.tvRoute);
            tvCar = itemView.findViewById(R.id.tvCar);
            tvSeatCount = itemView.findViewById(R.id.tvSeatCount);
            tvSeats = itemView.findViewById(R.id.tvSeats);
            btnAction = itemView.findViewById(R.id.btnAction);
        }
    }
}
