with open("app/src/main/res/layout/activity_trip_detail.xml", "r", encoding="utf-8") as f:
    xml = f.read()

target = """            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Danh sách hành khách"
                android:textColor="#000000"
                android:textSize="18sp"
                android:textStyle="bold"
                android:layout_marginTop="25dp"
                android:layout_marginBottom="15dp"/>"""

replacement = """            <!-- Khu vực vé chờ nhà xe xác nhận -->
            <LinearLayout
                android:id="@+id/layoutPendingTickets"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="vertical"
                android:layout_marginTop="20dp"
                android:background="#FFF8E1"
                android:padding="12dp"
                android:visibility="gone">

                <TextView
                    android:id="@+id/tvPendingTitle"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:text="🔔 Vé chờ nhà xe xác nhận"
                    android:textColor="#E65100"
                    android:textSize="16sp"
                    android:textStyle="bold"
                    android:layout_marginBottom="8dp"/>

                <LinearLayout
                    android:id="@+id/containerPendingTickets"
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical" />
            </LinearLayout>

            <TextView
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:text="Danh sách hành khách đã xác nhận"
                android:textColor="#000000"
                android:textSize="18sp"
                android:textStyle="bold"
                android:layout_marginTop="25dp"
                android:layout_marginBottom="15dp"/>"""

assert target in xml, "target not found in activity_trip_detail.xml"
xml = xml.replace(target, replacement, 1)

with open("app/src/main/res/layout/activity_trip_detail.xml", "w", encoding="utf-8") as f:
    f.write(xml)

print("SUCCESS: activity_trip_detail.xml updated!")

