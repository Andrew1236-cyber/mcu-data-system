from rabbitmq_sync import RabbitMQSync

if __name__ == "__main__":
    print("🔄 Запуск синхронизации с RabbitMQ...")
    sync = RabbitMQSync()
    sync.start_sync_loop()