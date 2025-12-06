import time
import mysql.connector
import requests
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

def check_expired_products():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE expiry_date <= CURDATE()")
    rows = cursor.fetchall()

    if len(rows) == 0:
        return

    for row in rows:
        message = f"⚠️ Sản phẩm hết hạn:\n- Tên: {row['name']}\n- Hết hạn: {row['expiry_date']}"
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": message}
        )

    cursor.close()
    db.close()


if __name__ == "__main__":
    print("DB_HOST =", DB_HOST)  # DEBUG quan trọng
    while True:
        check_expired_products()
        time.sleep(3600)
