import sqlite3
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, db_path="sensor_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT NOT NULL,
                    data_value TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    sent INTEGER DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            conn.close()
            logging.info("✅ База данных инициализирована")
        except Exception as e:
            logging.error(f"❌ Ошибка инициализации БД: {e}")
    
    def save_data(self, device_id, data_value, timestamp):
        """Сохранение данных в SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sensor_data (device_id, data_value, timestamp)
                VALUES (?, ?, ?)
            ''', (device_id, data_value, timestamp))
            conn.commit()
            conn.close()
            logging.info(f"✅ Данные сохранены: {device_id}:{data_value}:{timestamp}")
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка сохранения: {e}")
            return False
    
    def get_unsent_data(self):
        """Получение неотправленных данных"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, device_id, data_value, timestamp 
                FROM sensor_data 
                WHERE sent = 0
            ''')
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            logging.error(f"❌ Ошибка получения данных: {e}")
            return []
    
    def mark_as_sent(self, record_id):
        """Пометить данные как отправленные"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE sensor_data SET sent = 1 WHERE id = ?
            ''', (record_id,))
            conn.commit()
            conn.close()
            logging.info(f"✅ Данные {record_id} помечены как отправленные")
            return True
        except Exception as e:
            logging.error(f"❌ Ошибка обновления: {e}")
            return False