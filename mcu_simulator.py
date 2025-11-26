import socket
import time
from datetime import datetime

def test_mcu():
    """Тестовый клиент для имитации STM32"""
    counter = 0
    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 8080))
            
            # Формат: устройство:данные:временная_метка
            data = f"STM32_001:TEMP_{25 + counter % 5}:{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}"
            
            client_socket.send(data.encode())
            response = client_socket.recv(1024).decode()
            print(f"✅ Отправлено: {data} | Ответ: {response}")
            
            client_socket.close()
            counter += 1
            time.sleep(5)  # Каждые 5 секунд
            
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            time.sleep(5)

if __name__ == "__main__":
    test_mcu()