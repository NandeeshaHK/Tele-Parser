.PHONY: build up down test lint

build:
	docker build -t telemetry-pipeline:local .

up:
	docker-compose up --build

down:
	docker-compose down

lint:
	flake8 src || true
