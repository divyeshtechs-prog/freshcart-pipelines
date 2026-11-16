
import json
import pika

RABBITMQ_HOST = "localhost"

DRIVERS = {
    "ravi": "bangalore.koramangala.*",
    "priya": "bangalore.indiranagar.*",
    "arjun": "bangalore.*.ride",
    "meena": "bangalore.*.food",
    "karthik": "chennai.tnagar.food",
    "control": "bangalore.#",
}


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.exchange_declare(
        exchange="rapido-dispatch",
        exchange_type="topic",
        durable=True
    )

    for queue, routing_pattern in DRIVERS.items():
        channel.queue_declare(queue=queue, durable=True)
        channel.queue_bind(
            exchange="rapido-dispatch",
            queue=queue,
            routing_key=routing_pattern
        )

    def make_callback(queue_name):
        def callback(ch, method, properties, body):
            try:
                event = json.loads(body)

                if not event.get("zone"):
                    print(f"[{queue_name.upper()}] Rejected: Missing zone")
                    ch.basic_nack(
                        delivery_tag=method.delivery_tag,
                        requeue=False
                    )
                    return

                print(
                    f"[{queue_name.upper()}] Received: "
                    f"{event['routing_key']} | "
                    f"Zone: {event['zone']} | "
                    f"Event ID: {event['event_id']}"
                )

                ch.basic_ack(delivery_tag=method.delivery_tag)

            except (json.JSONDecodeError, KeyError) as error:
                print(f"[{queue_name.upper()}] Invalid message: {error}")
                ch.basic_nack(
                    delivery_tag=method.delivery_tag,
                    requeue=False
                )

        return callback

    # Register all consumers before starting consumption.
    for queue in DRIVERS:
        channel.basic_consume(
            queue=queue,
            on_message_callback=make_callback(queue),
            auto_ack=False
        )

    print("Driver consumers started. Press CTRL+C to stop.")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nConsumers stopped.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
