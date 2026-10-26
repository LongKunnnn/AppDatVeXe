package com.vexeapp.adapters;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;
import com.vexeapp.R;
import com.vexeapp.models.Passenger;
import java.util.List;

public class PassengerAdapter extends RecyclerView.Adapter<PassengerAdapter.PassengerViewHolder> {
    private List<Passenger> passengerList;

    public PassengerAdapter(List<Passenger> passengerList) {
        this.passengerList = passengerList;
    }

    @NonNull
    @Override
    public PassengerViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_passenger, parent, false);
        return new PassengerViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull PassengerViewHolder holder, int position) {
        Passenger passenger = passengerList.get(position);
        holder.tvPassengerName.setText(passenger.getName());
        holder.tvPassengerPhone.setText("SĐT: " + passenger.getPhone());
        holder.tvPickup.setText("Điểm đón: " + passenger.getPickupPoint());
        holder.tvDropoff.setText("Điểm trả: " + passenger.getDropoffPoint());
        holder.tvSeatNumber.setText(passenger.getSeatNumber());
    }

    @Override
    public int getItemCount() {
        return passengerList.size();
    }

    static class PassengerViewHolder extends RecyclerView.ViewHolder {
        TextView tvPassengerName, tvPassengerPhone, tvPickup, tvDropoff, tvSeatNumber;

        public PassengerViewHolder(@NonNull View itemView) {
            super(itemView);
            tvPassengerName = itemView.findViewById(R.id.tvPassengerName);
            tvPassengerPhone = itemView.findViewById(R.id.tvPassengerPhone);
            tvPickup = itemView.findViewById(R.id.tvPickup);
            tvDropoff = itemView.findViewById(R.id.tvDropoff);
            tvSeatNumber = itemView.findViewById(R.id.tvSeatNumber);
        }
    }
}
