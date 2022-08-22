format:
	poetry run isort src && poetry run black src

run:
	poetry run python src/main.py

test:
	poetry run pytest src -n 4

check:
	poetry run black src --check && \
	poetry run isort src --check && \
    poetry run flake8 src && \
    poetry run mypy src

create_migrations:
	cd src && \
	poetry run alembic revision --autogenerate

migrate:
	cd src && \
	poetry run alembic upgrade head

env:
	cp .env.example .env

db:
	docker-compose up -d

db_down:
	docker-compose down
