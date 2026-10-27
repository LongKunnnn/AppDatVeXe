# Update activity_car_type_management.xml
with open("app/src/main/res/layout/activity_car_type_management.xml", "r", encoding="utf-8") as f:
    xml_mgmt = f.read()

target_mgmt = """    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/rvCarTypes"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:padding="10dp"
        android:clipToPadding="false"
        app:layout_constraintBottom_toTopOf="@+id/bottom_nav"
        app:layout_constraintTop_toBottomOf="@+id/header" />"""

replacement_mgmt = """    <LinearLayout
        android:id="@+id/layoutActionHeader"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal"
        android:paddingHorizontal="15dp"
        android:paddingVertical="12dp"
        android:gravity="center_vertical"
        app:layout_constraintTop_toBottomOf="@+id/header">

        <TextView
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Quản lý loại xe"
            android:textColor="#1A1A1A"
            android:textSize="18sp"
            android:textStyle="bold" />

        <Button
            android:id="@+id/btnAddCarType"
            android:layout_width="wrap_content"
            android:layout_height="38dp"
            android:backgroundTint="#0091D5"
            android:text="+ Thêm loại xe"
            android:textAllCaps="false"
            android:textColor="#FFFFFF"
            android:textSize="13sp"
            android:textStyle="bold"
            app:cornerRadius="8dp" />
    </LinearLayout>

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/rvCarTypes"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:padding="10dp"
        android:clipToPadding="false"
        app:layout_constraintBottom_toTopOf="@+id/bottom_nav"
        app:layout_constraintTop_toBottomOf="@+id/layoutActionHeader" />"""

assert target_mgmt in xml_mgmt, "target_mgmt not found"
xml_mgmt = xml_mgmt.replace(target_mgmt, replacement_mgmt, 1)

with open("app/src/main/res/layout/activity_car_type_management.xml", "w", encoding="utf-8") as f:
    f.write(xml_mgmt)

print("SUCCESS: activity_car_type_management.xml updated!")

# Update item_car_type.xml
with open("app/src/main/res/layout/item_car_type.xml", "r", encoding="utf-8") as f:
    xml_item = f.read()

target_item = """            <Button
                android:id="@+id/btnUpdatePrice"
                android:layout_width="match_parent"
                android:layout_height="40dp"
                android:backgroundTint="#13B5F6"
                android:text="$  Cập nhật giá vé"
                android:textAllCaps="false"
                android:textColor="#FFFFFF"
                android:textSize="13sp"
                android:textStyle="bold"
                app:cornerRadius="8dp"
                android:insetTop="0dp"
                android:insetBottom="0dp"
                android:minHeight="0dp"/>"""

replacement_item = """            <LinearLayout
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:orientation="horizontal">

                <Button
                    android:id="@+id/btnUpdatePrice"
                    android:layout_width="0dp"
                    android:layout_height="40dp"
                    android:layout_weight="1"
                    android:layout_marginEnd="8dp"
                    android:backgroundTint="#13B5F6"
                    android:text="✏️  Sửa loại xe"
                    android:textAllCaps="false"
                    android:textColor="#FFFFFF"
                    android:textSize="13sp"
                    android:textStyle="bold"
                    app:cornerRadius="8dp"
                    android:insetTop="0dp"
                    android:insetBottom="0dp"
                    android:minHeight="0dp"/>

                <Button
                    android:id="@+id/btnDeleteCarType"
                    android:layout_width="wrap_content"
                    android:layout_height="40dp"
                    android:backgroundTint="#EF5350"
                    android:text="🗑️ Xóa"
                    android:textAllCaps="false"
                    android:textColor="#FFFFFF"
                    android:textSize="13sp"
                    android:textStyle="bold"
                    app:cornerRadius="8dp"
                    android:insetTop="0dp"
                    android:insetBottom="0dp"
                    android:minHeight="0dp"/>
            </LinearLayout>"""

assert target_item in xml_item, "target_item not found"
xml_item = xml_item.replace(target_item, replacement_item, 1)

with open("app/src/main/res/layout/item_car_type.xml", "w", encoding="utf-8") as f:
    f.write(xml_item)

print("SUCCESS: item_car_type.xml updated!")

