
import json
import random
import time
import uuid
from datetime import datetime, timezone

import pika

RABBITMQ_HOST = "localhost"
EXCHANGE = "rapido-dispatch"
PUBLISH_INTERVAL = 2

CITIES = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "whitefield"],
}

EVENT_TYPES = ["ride", "food"]


def generate_event(count):
    city = random.choice(list(CITIES.keys()))
    zone = random.choice(CITIES[city])
    event_type = random.choice(EVENT_TYPES)

    # Keep a valid routing key, but omit zone from the payload every 10th event.
    routing_key = f"{city}.{zone}.{event_type}"

    event_zone = None if count % 10 == 0 else zone

    event = {
        "id": str(uuid.uuid4()),
        "city": city,
        "zone": event_zone,
        "type": event_type,
        "ts": datetime.now(timezone.utc).isoformat(),
    }

    return routing_key, event

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True,
    )

    count = 0
    print("Rapido dispatcher started. Publishing every 2 seconds.")

    try:
        while True:
            count += 1
            routing_key, event = generate_event(count)

            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=json.dumps(event),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json",
                ),
            )

            print(
                f"Published: {routing_key} | "
                f"Event ID: {event['id']} | "
                f"Zone: {event['zone']}"
            )

            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("\nDispatcher stopped.")

    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
