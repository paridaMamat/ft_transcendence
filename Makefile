all: 
	 mkdir -p postgresql/data/postgresql
	 docker compose -f ./docker-compose.yml build
	 docker compose -f ./docker-compose.yml up -d


clean:
	docker container stop backend frontend postgresql 2> /dev/null || true;
	docker network rm ft_transcendence 2> /dev/null || true;

fclean: clean
	rm -Rf postgresql/data/postgresql
	docker system prune -a

re: fclean all

.PHONY: all up build fclean re