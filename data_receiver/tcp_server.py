import socket
import threading
import logging
from database import DatabaseManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TCPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.db = DatabaseManager()
        self.running = True
    
    def handle_client(self, client_socket, address):
        """Обработка подключения клиента"""
        try:
            data = client_socket.recv(1024).decode('utf-8').strip()
            logging.info(f"📨 Получены данные от {address}: {data}")
            
            # Парсим данные по формату: устройство:данные:временная_метка
            if data.count(':') >= 2:
                parts = data.split(':', 2)
                device_id = parts[0]
                data_value = parts[1]
                timestamp = parts[2]
                
                # Сохраняем в базу
                self.db.save_data(device_id, data_value, timestamp)
                
                # Отправляем подтверждение
                client_socket.send("ACK".encode())
            else:
                logging.warning(f"⚠️ Неверный формат данных: {data}")
                client_socket.send("ERROR: Invalid format".encode())
                
        except Exception as e:
            logging.error(f"❌ Ошибка обработки клиента: {e}")
        finally:
            client_socket.close()
    
    def start(self):
        """Запуск TCP сервера"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            logging.info(f"🚀 TCP сервер запущен на {self.host}:{self.port}")
            
            while self.running:
                client_socket, address = server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            logging.error(f"❌ Ошибка сервера: {e}")
        finally:
            server_socket.close()
    
    def stop(self):
        """Остановка сервера"""
        self.running = False

if __name__ == "__main__":
    server = TCPServer()
    server.start()