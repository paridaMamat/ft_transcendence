all: 
	 docker compose -f ./docker-compose.yml build
	 docker compose -f ./docker-compose.yml up -d

down:
	docker compose down

clean:
	docker container stop web database 2> /dev/null || true;
	docker network rm ft_transcendence 2> /dev/null || true;

fclean: down
	docker system prune -af

re: fclean all

.PHONY: all up build fclean re