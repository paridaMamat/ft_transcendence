DOCKER=backend
all: 
	 docker compose -f ./docker-compose.yml build
	 docker compose -f ./docker-compose.yml up -d
	 docker compose logs -f

down:
	docker-compose down --volumes --remove-orphans

clean:
	docker container stop backend database nginx 2> /dev/null || true;
	docker network rm ft_transcendence 2> /dev/null || true;

fclean: down
	docker system prune -af --volumes
	if [ "$$(docker volume ls -q)" != "" ]; then \
		docker volume rm $$(docker volume ls -q); \
	fi

re: fclean all

.PHONY: all up build fclean re
