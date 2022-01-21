docker-compose build base
docker push pmallozzi/crome:latest
docker-compose build web
docker push pmallozzi/crome:web
