import threading
import time
import uuid
from kafka.admin import KafkaAdminClient

from get_data import GetData

if __name__ == '__main__':
    # Konfiguracja tematów i grup
    topics = ['test-topic', 'test-topic2', 'test-topic3', 'test-topic4']
    group_id = f"test-group-{uuid.uuid4()}"

    print(f"Użycie dynamicznej grupy: {group_id}")

    # Inicjalizacja klasy GetData
    data_get = GetData()

    # Inicjalizacja klienta Kafka Admin
    admin_client = KafkaAdminClient(
        bootstrap_servers=data_get.KAFKA_BROKER,
        client_id='topic-checker'
    )

    # Sprawdzenie i tworzenie tematów
    data_get.check_and_create_topics(admin_client, topics)

    # Tworzenie producentów
    producer1 = data_get.create_producer()
    producer2 = data_get.create_producer()

    # Tworzenie konsumentów
    consumers = [data_get.create_consumer(topic, group_id) for topic in topics]

    # Tworzenie wątków do wysyłania danych
    opcua_write_thread = threading.Thread(
        target=data_get.write_opcua_data,
        args=(producer1,),
        daemon=True
    )
    snap7_write_thread = threading.Thread(
        target=data_get.write_snap7_data,
        args=(producer2,),
        daemon=True
    )

    # Tworzenie wątków do odbierania danych
    consumer_threads = [
        threading.Thread(
            target=data_get.receive_message,
            args=(topic, consumer),
            daemon=True
        ) for topic, consumer in zip(topics, consumers)
    ]

    # Uruchamianie wątków do wysyłania danych
    opcua_write_thread.start()
    snap7_write_thread.start()

    # Uruchamianie wątków do odbierania danych
    for thread in consumer_threads:
        thread.start()

    # Opcjonalny wątek do danych sinusoidalnych (można wyłączyć, jeśli niepotrzebny)
    sin_thread = threading.Thread(target=data_get.write_sin_data, daemon=False)
    sin_thread.start()

    try:
        while True:
            print("Główna pętla działa. Wciśnij Ctrl+C, aby zakończyć.")
            time.sleep(5)

    except KeyboardInterrupt:
        print("Zamykanie programu...")

        data_get.running = False


        # Zamykanie producentów
        producer1.close()
        producer2.close()

        # Zamykanie klientów Kafka
        for consumer in consumers:
            consumer.close()

        admin_client.close()

        # Zamykanie połączenia z bazą danych i innymi usługami
        data_get.client.close()  # Zamykanie klienta InfluxDB
        if data_get.plc_snap7:
            data_get.plc_snap7.disconnect()
        if data_get.client_opcua:
            data_get.client_opcua.disconnect()

        print("Wszystkie procesy zostały zamknięte.")