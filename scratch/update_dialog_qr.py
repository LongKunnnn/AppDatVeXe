with open("app/src/main/res/layout/dialog_qr_payment.xml", "r", encoding="utf-8") as f:
    xml = f.read()

target = """        <Button
            android:id="@+id/btnQrCancel"
            android:layout_width="match_parent"
            android:layout_height="54dp"
            android:layout_marginTop="24dp"
            android:backgroundTint="#F5F5F5"
            android:text="Hủy"
            android:textAllCaps="false"
            android:textColor="@color/black"
            app:cornerRadius="27dp"/>"""

replacement = """        <Button
            android:id="@+id/btnConfirmPaid"
            android:layout_width="match_parent"
            android:layout_height="54dp"
            android:layout_marginTop="20dp"
            android:backgroundTint="#0047AB"
            android:text="Tôi đã thanh toán"
            android:textAllCaps="false"
            android:textColor="@color/white"
            android:textSize="16sp"
            android:textStyle="bold"
            app:cornerRadius="27dp"/>

        <Button
            android:id="@+id/btnQrCancel"
            android:layout_width="match_parent"
            android:layout_height="48dp"
            android:layout_marginTop="10dp"
            android:backgroundTint="#F5F5F5"
            android:text="Đóng"
            android:textAllCaps="false"
            android:textColor="@color/black"
            app:cornerRadius="24dp"/>"""

assert target in xml, "target not found in dialog_qr_payment.xml"
xml = xml.replace(target, replacement, 1)

with open("app/src/main/res/layout/dialog_qr_payment.xml", "w", encoding="utf-8") as f:
    f.write(xml)

print("SUCCESS: dialog_qr_payment.xml updated!")

