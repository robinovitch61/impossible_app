# docker system prune -f
docker-compose stop
docker-compose rm -f
docker-compose pull
docker-compose build --no-cache
docker-compose up -d --force-recreate --remove-orphans