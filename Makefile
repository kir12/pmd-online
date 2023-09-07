d:
	docker build -t pmd-online .
dc:
	docker compose down
	docker compose up -d --build web 