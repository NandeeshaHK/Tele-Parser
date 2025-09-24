import os

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "telemetry")
CONSUMER_GROUP = os.getenv("CONSUMER_GROUP", "telemetry-consumer")
RAW_OUTPUT_DIR = os.getenv("RAW_OUTPUT_DIR", "data/raw")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1000"))
PARQUET_OUTPUT_DIR = os.getenv("PARQUET_OUTPUT_DIR", "data/parquet")
SAVED_MODEL_DIR = os.getenv("SAVED_MODEL_DIR", "saved_model")
