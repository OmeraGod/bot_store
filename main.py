import time
import mysql.connector
import requests

TOKEN = "8573938089:AAESVqhpd0Sz7dyhDZMaEyOndMNbcr1lI64"
CHAT_ID = "1761351658"

def check_expired_products():
    db = mysql.connector.connect(
        host="DB_HOST",
        user="DB_USER",
        password="DB_PASS",
        database="DB_NAME"
    )
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products WHERE expiry_date <= CURDATE()")
    rows = cursor.fetchall()

    if len(rows) == 0:
        return

    for row in rows:
        message = f"⚠️ Sản phẩm hết hạn:\n- Tên: {row['name']}\n- Hết hạn: {row['expiry_date']}"
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                     params={"chat_id": CHAT_ID, "text": message})

    cursor.close()
    db.close()


if __name__ == "__main__":
    while True:
        check_expired_products()
        time.sleep(3600)  # kiểm tra mỗi 1 giờ
