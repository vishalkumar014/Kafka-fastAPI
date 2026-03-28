# FastAPI Kafka Microservices

This project contains two FastAPI services connected through Kafka using Docker Compose:

- `payment_service` publishes payment events to Kafka
- `notification_service` consumes those events and simulates sending notifications

## Services

### Kafka

- Image: `confluentinc/cp-kafka:latest`
- Port: `9092`

### Payment Service

- Framework: FastAPI
- Container port mapping: `8001:8001`
- Publishes messages to Kafka topic: `payment_topic`

Endpoints:

- `POST /`
- `POST /order`

Example request:

```json
{
  "name": "Sample Product"
}
```

Behavior:

- `POST /` returns a success response
- `POST /order` publishes a `PaymentDone` event to Kafka

### Notification Service

- Framework: FastAPI
- Container port mapping: `8080:8080`
- Consumes messages from Kafka topic: `payment_topic`

Endpoint:

- `GET /`

Behavior:

- Starts a background Kafka consumer on application startup
- Prints received payment events to the container logs
- Simulates sending a notification when it receives a `PaymentDone` event

## Project Structure

```text
.
|-- docker-compose.yml
|-- payment_service/
|   |-- main.py
|   |-- controller/index.py
|   |-- requirements.txt
|   |-- Dockerfile
|   `-- entrypoint.sh
`-- notification_service/
    |-- main.py
    |-- requirements.txt
    |-- Dockerfile
    `-- entrypoint.sh
```

## Prerequisites

- Docker
- Docker Compose

## Run the Project

From the project root:

```bash
docker compose up --build
```

## Access the Services

- Payment service: `http://localhost:8001`
- Notification service: `http://localhost:8080`
- Kafka broker: `localhost:9092`

## Test the Flow

Send a payment event:

```bash
curl -X POST http://localhost:8001/order \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Laptop\"}"
```

Expected result:

- The payment service sends a Kafka message
- The notification service receives the event
- Notification logs appear in the notification container output

## Useful Endpoints

### Payment Service

```bash
POST http://localhost:8001/
POST http://localhost:8001/order
```

### Notification Service

```bash
GET http://localhost:8080/
```

## Notes

- Both services use `uvicorn` with `--reload`
- Docker Compose waits for Kafka health before starting the application services
- The payment service currently sends a hardcoded `user_id` value of `"1"` in the Kafka event
