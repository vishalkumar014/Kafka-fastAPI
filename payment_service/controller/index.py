from fastapi import status, Depends, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from kafka import KafkaProducer
import json

router = APIRouter()

# ✅ Lazy init — only connects when first used
_producer = None

def get_producer():
    global _producer
    if _producer is None:
        _producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            linger_ms=5,        # ✅ small batching (default-style optimization)
            retries=3           # ✅ retry if broker temporarily fails
        )
    return _producer


class APIPayload(BaseModel):
    name: str = Field(...)

def verify_token(data: APIPayload):
    return data


@router.post("/")
async def index(data: APIPayload = Depends(verify_token)):
    return JSONResponse({"status": "success"}, status_code=status.HTTP_200_OK)


@router.post("/order")
async def create_order(data: APIPayload):
    event = {
        "event": "PaymentDone",
        "user_id": "1",
        "product": data.name
    }

    try:
        producer = get_producer()

        # ✅ Send message
        future = producer.send("payment_topic", event)

        # ✅ Optional: wait for Kafka ACK (good for debugging)
        record_metadata = future.get(timeout=10)
        print("Sent to Kafka:", record_metadata.topic, record_metadata.partition)

        # ✅ Flush ensures delivery (can remove if you want pure batching)
        producer.flush()

        return {"status": "sent to kafka"}

    except Exception as e:
        return JSONResponse(
            {"status": "error", "detail": str(e)},
            status_code=500
        )