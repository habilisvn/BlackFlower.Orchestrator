import json
import logging
from typing import Any
from datetime import datetime, timezone
from confluent_kafka import Producer  # type: ignore


class KafkaHandler(logging.Handler):
    """
    A custom logging handler that sends logs to Kafka
    """

    def __init__(
        self,
        kafka_config: dict[str, Any],
        topic: str = "application-logs",
        level: int = logging.ERROR
    ):
        """
        Initialize the Kafka handler

        Args:
            kafka_config: Kafka producer configuration
            topic: Kafka topic to send logs to
            level: Minimum logging level
        """
        super().__init__(level)
        self.topic = topic
        self.producer = Producer(kafka_config)  # type: ignore

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a record to Kafka

        Args:
            record: The log record to send
        """
        try:
            # Prepare the message
            message: dict[str, Any] = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "path": record.pathname,
                "line_number": record.lineno,
                "function": record.funcName,
            }

            # Add exception info if available
            if record.exc_info:
                message["exception"] = {
                    "type": str(record.exc_info[0]),
                    "value": str(record.exc_info[1]),
                    "traceback": self.format_traceback(record.exc_info[2])
                }

            # Add extra fields if available
            if hasattr(record, "request"):
                message["request"] = record.request  # type: ignore
            if hasattr(record, "error"):
                message["error"] = record.error  # type: ignore
            if hasattr(record, "errors"):
                message["errors"] = record.errors  # type: ignore

            # Send to Kafka
            self.producer.produce(  # type: ignore
                topic=self.topic,
                value=json.dumps(message).encode('utf-8'),
                callback=self._delivery_callback
            )
            # Flush to ensure the message is sent
            self.producer.flush()  # type: ignore

        except Exception as e:
            # Fallback to stderr if Kafka sending fails
            import sys
            print(f"Failed to send log to Kafka: {str(e)}", file=sys.stderr)

    def _delivery_callback(self, err: Any, msg: Any) -> None:
        """
        Callback for Kafka producer

        Args:
            err: Error if any
            msg: Message that was sent
        """
        if err:
            import sys
            print(f"Message delivery failed: {err}", file=sys.stderr)

    def format_traceback(self, tb: Any) -> list[str]:
        """
        Format a traceback into a list of strings

        Args:
            tb: Traceback object

        Returns:
            List of formatted traceback strings
        """
        import traceback
        return traceback.format_tb(tb)

    def close(self) -> None:
        """
        Close the handler and flush any remaining messages
        """
        self.producer.flush()  # type: ignore
        super().close()
