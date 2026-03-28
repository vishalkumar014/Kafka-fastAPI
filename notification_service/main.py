from fastapi import FastAPI
from kafka import KafkaConsumer
import json
from threading import Thread

app = FastAPI()

def consume_payments():

    try:
        print("Notification service listening...")

        consumer = KafkaConsumer(
            "payment_topic",
            bootstrap_servers="kafka:9092",
            auto_offset_reset="earliest",
            group_id="notification-group",
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )

        # ✅ Default Kafka consumption (batch + internal polling)
        for msg in consumer:
            data = msg.value
            print("Received Payment:", data)

            if data.get("event") == "PaymentDone":
                print(f"Sending email to user {data.get('user_id')} for {data.get('product')}")
    except Exception as e:
        print(str(e),'erro')

@app.on_event("startup")
def start_consumer():
    try:
        print("Kafka consumer thread started 01")
        thread = Thread(target=consume_payments, daemon=True)
        thread.start()
        print("Kafka consumer thread started")
    except Exception as e:
        print(str(e),'erro')


@app.get("/")
def health():
    return {"status": "notification service running"}