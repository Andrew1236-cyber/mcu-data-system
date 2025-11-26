import sqlite3

def check_database():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    
    print("📊 СОДЕРЖИМОЕ БАЗЫ ДАННЫХ:")
    cursor.execute("SELECT * FROM sensor_data")
    rows = cursor.fetchall()
    
    if rows:
        for row in rows:
            status = "ОТПРАВЛЕНО" if row[4] else "ОЖИДАЕТ"
            print(f"ID: {row[0]}, Устройство: {row[1]}, Данные: {row[2]}, Время: {row[3]}, Статус: {status}")
    else:
        print("❌ В базе данных нет записей")
    
    conn.close()

if __name__ == "__main__":
    check_database()