#!/usr/bin/env python3
"""
Produce synthetic telemetry messages to Kafka for testing.
"""
import json
import time
import random
from confluent_kafka import Producer
from src.common.config import KAFKA_BOOTSTRAP, KAFKA_TOPIC

p = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP})

def gen_message(car_id):
    return {
        "timestamp": int(time.time() * 1000),
        "car_id": car_id,
        "lap_number": random.randint(1, 50),
        "speed": random.random()*300,
        "throttle": random.random(),
        "brake": random.random(),
        "gear": random.randint(1, 8),
        "track_temp": random.random()*50.0
    }

if __name__ == "__main__":
    try:
        while True:
            msg = gen_message(car_id=f"CAR{random.randint(1,5)}")
            p.produce(KAFKA_TOPIC, json.dumps(msg).encode("utf-8"))
            p.flush()
            print("produced", msg)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("stopping")
