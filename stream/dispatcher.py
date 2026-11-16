
import itertools
import json
import time
import uuid
from datetime import datetime, timezone

import pika

RABBITMQ_HOST = "localhost"
EXCHANGE = "rapido-dispatch"
PUBLISH_INTERVAL = 2

# Routing key, event type, and zone
events = [
    ("bangalore.koramangala.food", "food", "koramangala"),
    ("bangalore.indiranagar.ride", "ride", "indiranagar"),
    ("bangalore.whitefield.ride", "ride", "whitefield"),
    ("chennai.tnagar.food", "food", "tnagar"),
    ("chennai.whitefield.ride", "ride", "whitefield"),
    ("bangalore.koramangala", "unknown", None),
]


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True
    )

    event_cycle = itertools.cycle(events)

    print("Rapido dispatcher started. Publishing every 2 seconds.")

    try:
        while True:
            routing_key, event_type, zone = next(event_cycle)

            event = {
                "event_id": str(uuid.uuid4()),
                "event_type": event_type,
                "routing_key": routing_key,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "zone": zone,
            }

            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=json.dumps(event),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    content_type="application/json"
                )
            )

            print(
                f"Published: {routing_key} | "
                f"Zone: {zone} | "
                f"Event ID: {event['event_id']}"
            )

            time.sleep(PUBLISH_INTERVAL)

    except KeyboardInterrupt:
        print("\nDispatcher stopped.")

    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
