# Real-time Telemetry Pipeline — Lap-Time & Strategy Prediction

Minimal end-to-end scaffold:
- Kafka consumer (Python)
- Preprocessing (Apache Arrow / Parquet)
- Model training (TensorFlow)
- Model export for TF Serving
- GraphQL API (FastAPI + Ariadne)
- Docker + Kubernetes manifests for deployment

## Prereqs
- Python 3.10+
- Docker & docker-compose
- Kubernetes (kubectl) if deploying on k8s
- Kafka cluster accessible (local dev: use Confluent or Bitnami images)

## Quickstart (local)
1. Install Python deps:
   ```bash
   pip install -r requirements.txt
