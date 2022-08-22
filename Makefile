format:
	isort src && black src

test:
	pytest src -n 4

check:
	black src --check && \
	isort src --check && \
    flake8 src && \
    mypy src

create_migrations:
	cd src && \
	alembic revision --autogenerate

migrate:
	cd src && \
	alembic upgrade head

env:
	cp .env.example .env

db:
	docker-compose up -d

db_down:
	docker-compose down
