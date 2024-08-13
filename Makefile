config ?= compile

dev:
	docker-compose -f docker-compose.yaml up --build --remove-orphans


stop:
	docker-compose stop

logs:
	docker-compose logs -f --tail 50
weaviate:
	docker-compose -f weaviate.docker-compose.yaml up --build --remove-orphans -d
