FROM pmallozzi/crome:latest

WORKDIR /home/crome/web/frontend
RUN npm run install:clean
RUN npm run build

WORKDIR /home/crome

ENV PYTHONPATH "${PYTHONPATH}:/home/crome/src:/home/crome/casestudies:/home/crome/config"

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]
