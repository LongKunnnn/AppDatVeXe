with open("app/src/main/AndroidManifest.xml", "r", encoding="utf-8") as f:
    xml = f.read()

old_main = """        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>"""

new_main = """        <activity
            android:name=".MainActivity"
            android:exported="false" />"""

old_login = """        <activity
            android:name=".LoginActivity"
            android:exported="false" />"""

new_login = """        <activity
            android:name=".LoginActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>"""

assert old_main in xml, "old_main not found"
assert old_login in xml, "old_login not found"

xml = xml.replace(old_main, new_main, 1)
xml = xml.replace(old_login, new_login, 1)

with open("app/src/main/AndroidManifest.xml", "w", encoding="utf-8") as f:
    f.write(xml)

print("SUCCESS: AndroidManifest.xml updated to make LoginActivity the launcher!")

