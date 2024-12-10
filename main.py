import threading
import time

from get_data import GetData


if __name__ == '__main__':

    data_get = GetData()
    data_get.create_topic()
    producer = data_get.create_producer()
    consumer = data_get.create_consumer()

    consumer_thread = threading.Thread(target=data_get.receive_message,
                                       args=(consumer,), daemon=True)

    consumer_thread.start()
    sin_thread = threading.Thread(target=data_get.write_sin_data)
    sin_thread.start()

    opcua_thread = threading.Thread(target=data_get.write_opcua_data)
    opcua_thread.start()

    for i in range(5):
        msg = {"id": i, "message": f"Hello Kafka! Message {i}"}
        print(f"sending message: {msg}")
        data_get.send_message(producer, msg)
        time.sleep(1)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("finishing...")

    # data_get.write_sin_data()
