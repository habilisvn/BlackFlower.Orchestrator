import json
from confluent_kafka import (  # type: ignore
    Consumer,  # type: ignore
    KafkaError,  # type: ignore
    KafkaException,  # type: ignore
    admin
)


def create_topic_if_not_exists(topic_name: str):
    # Admin client configuration
    admin_client = admin.AdminClient({
        'bootstrap.servers': 'localhost:9092'
    })

    # Check if topic exists
    metadata = admin_client.list_topics(timeout=5)  # type: ignore
    if topic_name not in metadata.topics:  # type: ignore
        # Create topic if it doesn't exist
        new_topic = admin.NewTopic(  # type: ignore
            topic_name,
            num_partitions=1,
            replication_factor=1
        )

        try:
            futures = admin_client.create_topics([new_topic])  # type: ignore
            for topic, future in futures.items():  # type: ignore
                future.result()  # type: ignore # Wait for topic creation
            print(f"Topic {topic_name} created successfully")
        except KafkaException as e:  # type: ignore
            print(f"Failed to create topic: {e}")
            raise


def test_kafka_consumer(topic_name: str = 'fastapi-logs'):
    # Create topic if it doesn't exist
    create_topic_if_not_exists(topic_name)

    # Consumer configuration
    conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'fastapi-consumer',
        'auto.offset.reset': 'earliest'
    }

    # Create Consumer instance
    consumer = Consumer(conf)  # type: ignore

    # Subscribe to topic
    consumer.subscribe([topic_name])  # type: ignore

    try:
        # Poll for messages
        while True:
            # timeout in seconds
            msg = consumer.poll(timeout=1.0)  # type: ignore

            if msg is None:
                continue
            if msg.error():  # type: ignore
                if (msg.error().code() ==  # type: ignore
                        KafkaError._PARTITION_EOF):  # type: ignore
                    print('Reached end of partition')
                else:
                    print(f'Error: {msg.error()}')  # type: ignore
                continue

            # Decode and parse the message
            try:
                value = json.loads(msg.value().decode('utf-8'))  # type: ignore
                print(f"Received message: {value}")
                print(f"Topic: {msg.topic()}")  # type: ignore
                print(f"Partition: {msg.partition()}")  # type: ignore
                print(f"Offset: {msg.offset()}")  # type: ignore
                print(f"Timestamp: {msg.timestamp()}")  # type: ignore
                print("---")

                # You can add assertions here to verify the message content
                assert isinstance(
                    value, dict), "Message should be a dictionary"

            except json.JSONDecodeError as e:
                print(f"Failed to decode message: {e}")
                continue

    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()  # type: ignore


if __name__ == "__main__":
    test_kafka_consumer(topic_name='fastapi-logs')
