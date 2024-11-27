from confluent_kafka import Producer
import json
import time

def delivery_report(err, msg):
    """Callback invoked on message delivery success or failure"""
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def test_kafka_producer():
    # Producer configuration
    conf = {
        'bootstrap.servers': 'taolao:9092',
        'client.id': 'test_producer'
    }

    # Create Producer instance
    producer = Producer(conf)

    # Test message
    test_message = {
        'timestamp': time.time(),
        'message': 'Test message from Kafka producer',
        'status': 'testing'
    }

    try:
        # Produce message
        producer.produce(
            topic='fastapi-logs',
            value=json.dumps(test_message).encode('utf-8'),
            callback=delivery_report
        )

        # Wait for messages to be delivered
        producer.flush()

        print("Test message sent successfully")

    except Exception as e:
        print(f"Error producing message: {str(e)}")
    finally:
        producer.close()

if __name__ == "__main__":
    test_kafka_producer()
