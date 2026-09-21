.PHONY: test build run logs stop

test:
	pytest -q

build:
	docker build -t cicd-demo:local .

run:
	docker compose up --build -d

logs:
	docker compose logs -f app

stop:
	docker compose down
