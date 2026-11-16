
import json
import sys
import pika

RABBITMQ_HOST = "localhost"
EXCHANGE = "rapido-dispatch"


def main():
    if len(sys.argv) != 3:
        print('Usage: python driver.py NAME "ROUTING_PATTERN"')
        sys.exit(1)

    name = sys.argv[1]
    routing_pattern = sys.argv[2]

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True,
    )

    # Exclusive, auto-delete queue: private to this driver process.
    result = channel.queue_declare(
        queue="",
        exclusive=True,
        auto_delete=True,
    )
    queue_name = result.method.queue

    channel.queue_bind(
        exchange=EXCHANGE,
        queue=queue_name,
        routing_key=routing_pattern,
    )

    def callback(ch, method, properties, body):
        try:
            event = json.loads(body)

            if not event.get("zone"):
                print(f"[{name}] Rejected: Missing zone")
                ch.basic_nack(
                    delivery_tag=method.delivery_tag,
                    requeue=False,
                )
                return

            print(
                f"[{name}] Received: "
                f"{event['city']}.{event['zone']}.{event['type']} | "
                f"Event ID: {event['id']} | "
                f"Timestamp: {event['ts']}"
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"[{name}] Invalid message: {error}")
            ch.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False,
            )

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False,
    )

    print(f"Driver: {name}")
    print(f"Routing pattern: {routing_pattern}")
    print(f"Private queue: {queue_name}")
    print("Listening for events. Press CTRL+C to stop.")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(f"\nDriver {name} stopped.")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
