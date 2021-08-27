FROM pmallozzi/ltltools:web as build


ENV GIT_SSL_NO_VERIFY=1
RUN git clone https://github.com/pierg/crome.git --branch master --single-branch
WORKDIR /home/crome/web/frontend

RUN npm run deploy

FROM nginx:alpine
COPY --from=build /home/crome/web/frontend/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]