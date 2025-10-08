import mariadb

try:
    conn = mariadb.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Shivam12345",  # Matches your password
        auth_plugin="mysql_native_password"
    )
    print("Connection successful!")
    conn.close()
except mariadb.Error as e:
    print(f"Connection failed: {e}")