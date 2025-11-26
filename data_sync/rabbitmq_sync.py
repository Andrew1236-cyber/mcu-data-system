import json
import time
import logging
import sqlite3
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RabbitMQSync:
    def __init__(self, db_path="../data_receiver/sensor_data.db"):
        self.db_path = db_path
        self.sent_count = 0
        
    def send_to_rabbitmq(self, data):
        """Эмуляция отправки в RabbitMQ (без реального RabbitMQ)"""
        try:
            message = {
                'id': data[0],
                'device_id': data[1],
                'data_value': data[2],
                'timestamp': data[3],
                'sent_at': datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            }
            
            # Эмуляция успешной отправки
            logging.info(f"✅ [RABBITMQ ЭМУЛЯТОР] Данные отправлены: {data[1]}:{data[2]}")
            logging.info(f"📦 Сообщение: {json.dumps(message, ensure_ascii=False)}")
            
            self.sent_count += 1
            return True  # Всегда успех для демонстрации
            
        except Exception as e:
            logging.error(f"❌ Ошибка эмуляции RabbitMQ: {e}")
            return False
    
    def sync_data(self):
        """Синхронизация данных из SQLite в RabbitMQ"""
        try:
            # Получаем неотправленные данные
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id, device_id, data_value, timestamp FROM sensor_data WHERE sent = 0')
            unsent_data = cursor.fetchall()
            conn.close()
            
            logging.info(f"📊 Найдено {len(unsent_data)} неотправленных записей")
            
            success_count = 0
            for data in unsent_data:
                # Отправляем в RabbitMQ (эмуляция)
                if self.send_to_rabbitmq(data):
                    # Помечаем как отправленные
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute('UPDATE sensor_data SET sent = 1 WHERE id = ?', (data[0],))
                    conn.commit()
                    conn.close()
                    success_count += 1
                    logging.info(f"✅ Данные ID:{data[0]} успешно синхронизированы")
                else:
                    logging.warning(f"⚠️ Не удалось отправить данные ID:{data[0]}")
            
            logging.info(f"🎯 Синхронизация завершена. Успешно: {success_count}/{len(unsent_data)}")
            logging.info(f"📈 Всего отправлено: {self.sent_count} сообщений")
            return success_count
            
        except Exception as e:
            logging.error(f"❌ Ошибка синхронизации: {e}")
            return 0
    
    def start_sync_loop(self, interval=30):
        """Запуск цикла синхронизации каждые 30 секунд"""
        logging.info(f"🔄 Запуск цикла синхронизации каждые {interval} секунд")
        logging.info("📝 Режим: ЭМУЛЯЦИЯ RabbitMQ (без установки)")
        
        while True:
            try:
                self.sync_data()
                time.sleep(interval)
            except KeyboardInterrupt:
                logging.info("⏹️ Синхронизация остановлена")
                break
            except Exception as e:
                logging.error(f"❌ Ошибка в цикле синхронизации: {e}")
                time.sleep(interval)

if __name__ == "__main__":
    sync = RabbitMQSync()
    sync.start_sync_loop()