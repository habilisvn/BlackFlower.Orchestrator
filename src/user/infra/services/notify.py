import json
import aio_pika

from user.domain.entities import UserEntity


async def notify_user_created(user: UserEntity) -> None:
    """
    Send a message to RabbitMQ when a user is created.

    Args:
        user: The user entity that was created
    """
    # Connect to RabbitMQ
    connection = await aio_pika.connect_robust(
        "amqp://rabbitmq:abcd1234@localhost:5672/"
    )

    async with connection:
        # Create a channel
        channel = await connection.channel()

        # Declare the exchange
        exchange = await channel.declare_exchange(
            "user_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Create the message
        message_body = {
            "event_type": "user_created",
            "username": user.username,
            "email": user.email,
            "created_at": str(user.created_at)
        }

        message = aio_pika.Message(
            body=json.dumps(message_body).encode(),
            content_type="application/json"
        )

        # Publish the message
        await exchange.publish(
            message,
            routing_key="user.created"
        )
