#!/usr/bin/env python3
"""
Kafka consumer: reads telemetry JSON messages and stores into newline-delimited JSON batches.
Simple robust example for local/dev.
"""
import os
import json
import time
from confluent_kafka import Consumer
from pathlib import Path
from src.common.config import KAFKA_BOOTSTRAP, KAFKA_TOPIC, CONSUMER_GROUP, RAW_OUTPUT_DIR, BATCH_SIZE

Path(RAW_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

c = Consumer({
    'bootstrap.servers': KAFKA_BOOTSTRAP,
    'group.id': CONSUMER_GROUP,
    'auto.offset.reset': 'earliest'
})

c.subscribe([KAFKA_TOPIC])
batch = []
counter = 0
file_index = 0

try:
    while True:
        msg = c.poll(timeout=1.0)
        if msg is None:
            # flush batch periodically
            if batch:
                fname = Path(RAW_OUTPUT_DIR) / f"batch_{int(time.time())}_{file_index}.ndjson"
                with open(fname, "w") as f:
                    for obj in batch:
                        f.write(json.dumps(obj) + "\n")
                print(f"wrote {len(batch)} messages -> {fname}")
                file_index += 1
                batch = []
            continue
        if msg.error():
            print("Consumer error:", msg.error())
            continue
        try:
            payload = msg.value().decode('utf-8')
            data = json.loads(payload)
            batch.append(data)
            counter += 1
            if len(batch) >= BATCH_SIZE:
                fname = Path(RAW_OUTPUT_DIR) / f"batch_{int(time.time())}_{file_index}.ndjson"
                with open(fname, "w") as f:
                    for obj in batch:
                        f.write(json.dumps(obj) + "\n")
                print(f"wrote {len(batch)} messages -> {fname}")
                file_index += 1
                batch = []
        except Exception as e:
            print("Failed to decode message:", e)
except KeyboardInterrupt:
    print("Shutting down consumer")
finally:
    c.close()
