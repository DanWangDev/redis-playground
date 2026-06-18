.PHONY: help install install-dev build test test-integration test-cov lint fmt clean cluster-start cluster-stop cluster-logs cluster-status exercise-% exercise-local-%

help: ## Show this help
	@echo "Redis Playground"
	@echo ""
	@echo "Setup:"
	@echo "  make install           Install dependencies"
	@echo "  make install-dev       Install with dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test              Run unit tests (fakeredis, no Docker)"
	@echo "  make test-integration  Run integration tests (real Redis, Docker required)"
	@echo "  make test-cov          Run unit tests with coverage report"
	@echo "  make lint              Ruff check"
	@echo "  make fmt               Ruff format"
	@echo ""
	@echo "Cluster:"
	@echo "  make cluster-start     Start Redis Stack (Docker)"
	@echo "  make cluster-stop      Stop Redis Stack"
	@echo "  make cluster-status    Check Redis health"
	@echo ""
	@echo "Exercises:"
	@echo "  make exercise-01       Run exercise 01 on real Redis"
	@echo "  make exercise-local-01 Run exercise 01 with fakeredis"
	@echo ""
	@echo "  Replace 01 with any exercise number 01-20"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -m "not integration"

test-integration:
	pytest tests/ -m integration -v

test-cov:
	pytest tests/ -m "not integration" --cov --cov-report=term --cov-report=html

lint:
	ruff check src/ tests/

fmt:
	ruff format src/ tests/
	ruff check --fix src/ tests/

cluster-start:
	docker compose up -d --wait
	@echo "Redis running on localhost:6379"
	@echo "RedisInsight UI: http://localhost:8001"

cluster-stop:
	docker compose down --volumes

cluster-logs:
	docker compose logs --tail=100

cluster-status:
	docker compose exec redis redis-cli -a playground ping

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache htmlcov .coverage coverage.xml

build:
	pip install -e ".[dev]"

exercise-%:
	python -m redis_playground.main --exercise $* --no-step

exercise-local-%:
	python -m redis_playground.main --exercise $* --local --no-step
