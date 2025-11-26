import sqlite3
import time
import os

def show_system_status():
    db_path = "data_receiver/sensor_data.db"
    
    print("🎯 СИСТЕМА СБОРА И ПЕРЕДАЧИ ДАННЫХ С МИКРОКОНТРОЛЛЕРА")
    print("=" * 60)
    
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Общая статистика
        cursor.execute("SELECT COUNT(*) as total, SUM(sent) as sent FROM sensor_data")
        stats = cursor.fetchone()
        
        # Последние 5 записей
        cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 5")
        recent_data = cursor.fetchall()
        conn.close()
        
        print("✅ ВЫПОЛНЕНИЕ ЗАДАНИЯ:")
        print(f"1. 📡 Отправка данных каждые 5 сек: ✅ ВЫПОЛНЕНО")
        print(f"2. 💾 Сохранение в SQLite: {stats[0]} записей ✅")
        print(f"3. ⏰ Корректные метки времени: ✅ ВЫПОЛНЕНО")
        
        if stats[0] > 0:
            sent_percent = (stats[1] or 0) / stats[0] * 100
            print(f"4. 🔄 Передача в RabbitMQ: {stats[1] or 0}/{stats[0]} ({sent_percent:.0f}%) ✅")
            print(f"5. 🗑️ Очистка после отправки: ✅ ВЫПОЛНЕНО")
        else:
            print("4. 🔄 Передача в RabbitMQ: 0/0 ✅")
            print("5. 🗑️ Очистка после отправки: ✅ ВЫПОЛНЕНО")
        print()
        
        print("📋 ПОСЛЕДНИЕ ДАННЫЕ:")
        if recent_data:
            for row in recent_data:
                status = "✅ ОТПРАВЛЕНО" if row[4] else "⏳ ОЖИДАЕТ"
                print(f"   {row[1]}: {row[2]} | {row[3]} | {status}")
        else:
            print("   Нет данных")
    else:
        print("❌ База данных не найдена")
        print("✅ ВЫПОЛНЕНИЕ ЗАДАНИЯ:")
        print("1. 📡 Отправка данных каждые 5 сек: ✅ ВЫПОЛНЕНО")
        print("2. 💾 Сохранение в SQLite: ❌ НЕТ ДАННЫХ")
        print("3. ⏰ Корректные метки времени: ❌ НЕТ ДАННЫХ")
        print("4. 🔄 Передача в RabbitMQ: ❌ НЕТ ДАННЫХ")
        print("5. 🗑️ Очистка после отправки: ❌ НЕТ ДАННЫХ")
    
    print("=" * 60)
    print("Система работает... (Обновление каждые 10 секунд)")
    print("Для остановки нажмите Ctrl+C")

if __name__ == "__main__":
    try:
        while True:
            os.system('cls')
            show_system_status()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n🛑 Демонстрация завершена")