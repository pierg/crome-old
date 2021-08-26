FROM node:14-slim

ENV GIT_SSL_NO_VERIFY=1
RUN git clone https://github.com/pierg/crome.git --branch master --single-branch
WORKDIR /home/crome/web/frontend

RUN npm run deploy


